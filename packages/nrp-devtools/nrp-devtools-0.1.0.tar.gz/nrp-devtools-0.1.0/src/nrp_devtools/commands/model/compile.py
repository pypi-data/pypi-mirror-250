import configparser
import json
import os
import re
import shutil
import venv
from pathlib import Path

import click
import yaml

from nrp_devtools.commands.pyproject import PyProject
from nrp_devtools.commands.utils import run_cmdline
from nrp_devtools.config import OARepoConfig
from nrp_devtools.config.model_config import ModelConfig


def model_compiler_venv_dir(config: OARepoConfig, model):
    venv_dir = (
        config.repository_dir / ".nrp" / f"oarepo-model-builder-{model.model_name}"
    )
    return venv_dir.resolve()


def install_model_compiler(config: OARepoConfig, *, model: ModelConfig):
    venv_dir = model_compiler_venv_dir(config, model)
    print("model builder venv dir", venv_dir)
    click.secho(f"Installing model compiler to {venv_dir}", fg="yellow")

    if venv_dir.exists():
        shutil.rmtree(venv_dir)

    venv_args = [str(venv_dir)]
    venv.main(venv_args)

    run_cmdline(
        venv_dir / "bin" / "pip",
        "install",
        "-U",
        "setuptools",
        "pip",
        "wheel",
    )

    run_cmdline(
        venv_dir / "bin" / "pip",
        "install",
        f"oarepo-model-builder",
    )

    with open(config.models_dir / model.model_config_file) as f:
        model_data = yaml.safe_load(f)

    # install plugins from model.yaml
    _install_plugins_from_model(model_data, venv_dir)

    # install plugins from included files
    uses = model_data.get("use") or []
    if not isinstance(uses, list):
        uses = [uses]

    for use in uses:
        if not use.startswith("."):
            # can not currently find plugins in uses
            # that are registered as entrypoints
            continue
        with open(config.models_dir / use) as f:
            used_data = yaml.safe_load(f)
            _install_plugins_from_model(used_data, venv_dir)

    click.secho(f"Model compiler installed to {venv_dir}", fg="green")


def _install_plugins_from_model(model_data, venv_dir):
    plugins = model_data.get("plugins", {}).get("packages", [])
    for package in plugins:
        run_cmdline(
            venv_dir / "bin" / "pip",
            "install",
            package,
        )


def compile_model_to_tempdir(config: OARepoConfig, *, model: ModelConfig, tempdir):
    click.secho(f"Compiling model {model.model_name} to {tempdir}", fg="yellow")
    venv_dir = model_compiler_venv_dir(config, model)
    run_cmdline(
        venv_dir / "bin" / "oarepo-compile-model",
        "-vvv",
        str(config.models_dir / model.model_config_file),
        "--output-directory",
        str(tempdir),
    )
    click.secho(
        f"Model {model.model_name} successfully compiled to {tempdir}", fg="green"
    )


def copy_compiled_model(config: OARepoConfig, *, model: ModelConfig, tempdir):
    click.secho(
        f"Copying compiled model {model.model_name} from {tempdir} to {model.model_package}",
        fg="yellow",
    )
    alembic_path = Path(_get_alembic_path(tempdir, model.model_package)).resolve()

    remove_all_files_in_directory(
        config.repository_dir / model.model_package, except_of=alembic_path
    )

    copy_all_files_but_keep_existing(
        Path(tempdir) / model.model_package, config.repository_dir / model.model_package
    )

    click.secho(
        f"Compiled model {model.model_name} successfully copied to {model.model_package}",
        fg="green",
    )


def _get_alembic_path(rootdir, package_name):
    model_file = Path(rootdir) / package_name / "models" / "records.json"

    with open(model_file) as f:
        model_data = json.load(f)

    return model_data["model"]["record-metadata"]["alembic"].replace(".", "/")


def remove_all_files_in_directory(directory: Path, except_of=None):
    if not directory.exists():
        return True

    remove_this_directory = True
    for path in directory.iterdir():
        if path.resolve() == except_of:
            remove_this_directory = False
            continue
        if path.is_file():
            path.unlink()
        else:
            remove_this_directory = (
                remove_all_files_in_directory(path) and remove_this_directory
            )
    if remove_this_directory:
        directory.rmdir()
    return remove_this_directory


def copy_all_files_but_keep_existing(src: Path, dst: Path):
    def non_overwriting_copy(src, dst, *, follow_symlinks=True):
        if Path(dst).exists():
            return
        shutil.copy2(src, dst, follow_symlinks=follow_symlinks)

    return shutil.copytree(
        src, dst, copy_function=non_overwriting_copy, dirs_exist_ok=True
    )


def add_requirements_and_entrypoints(
    config: OARepoConfig, *, model: ModelConfig, tempdir
):
    click.secho(
        f"Adding requirements and entrypoints from {model.model_name}", fg="yellow"
    )

    setup_cfg = Path(tempdir) / "setup.cfg"
    # load setup.cfg via configparser
    config_parser = configparser.ConfigParser()
    config_parser.read(setup_cfg)
    dependencies = config_parser["options"].get("install_requires", "").split("\n")
    test_depedencies = (
        config_parser["options.extras_require"].get("tests", "").split("\n")
    )
    entrypoints = {}
    for ep_name, ep_values in config_parser["options.entry_points"].items():
        entrypoints[ep_name] = ep_values.split("\n")

    pyproject = PyProject(config.repository_dir / "pyproject.toml")

    pyproject.add_dependencies(*dependencies)
    pyproject.add_optional_dependencies("tests", *test_depedencies)

    for ep_name, ep_values in entrypoints.items():
        for val in ep_values:
            if not val:
                continue
            val = [x.strip() for x in val.split("=")]
            pyproject.add_entry_point(ep_name, val[0], val[1])

    pyproject.save()

    click.secho(
        f"Requirements and entrypoint successfully copied from {model.model_name}",
        fg="green",
    )


def generate_alembic(config: OARepoConfig, *, model: ModelConfig):
    click.secho(f"Generating alembic for {model.model_name}", fg="yellow")
    alembic_path = config.repository_dir / _get_alembic_path(
        config.repository_dir, model.model_package
    )
    branch = model.model_name
    setup_alembic(config, branch, alembic_path, model)
    click.secho(f"Alembic for {model.model_name} successfully generated", fg="green")


def setup_alembic(
    config: OARepoConfig, branch: str, alembic_path: Path, model: ModelConfig
):
    filecount = len(
        [x for x in alembic_path.iterdir() if x.is_file() and x.name.endswith(".py")]
    )

    if filecount < 2:
        intialize_alembic(config, branch, alembic_path, model)
    else:
        update_alembic(config, branch, alembic_path)


def update_alembic(config: OARepoConfig, branch, alembic_path):
    # alembic has been initialized, update heads and generate
    files = [file_path.name for file_path in alembic_path.iterdir()]
    file_numbers = []
    for file in files:
        file_number_regex = re.findall(f"(?<={branch}_)\d+", file)
        if file_number_regex:
            file_numbers.append(int(file_number_regex[0]))
    new_file_number = max(file_numbers) + 1
    revision_message, file_revision_name_suffix = get_revision_names(
        "Nrp install revision."
    )
    run_cmdline(
        config.invenio_command, "alembic", "upgrade", "heads", cwd=config.repository_dir
    )

    new_revision = get_revision_number(
        run_cmdline(
            config.invenio_command,
            "alembic",
            "revision",
            revision_message,
            "-b",
            branch,
            grab_stdout=True,
            cwd=config.repository_dir,
        ),
        file_revision_name_suffix,
    )
    rewrite_revision_file(alembic_path, new_file_number, branch, new_revision)
    fix_sqlalchemy_utils(alembic_path)
    run_cmdline(
        config.invenio_command, "alembic", "upgrade", "heads", cwd=config.repository_dir
    )


def intialize_alembic(config, branch, alembic_path, model):
    # alembic has not been initialized yet ...
    run_cmdline(
        config.invenio_command,
        "alembic",
        "upgrade",
        "heads",
        cwd=config.repository_dir,
    )
    # create model branch
    revision_message, file_revision_name_suffix = get_revision_names(
        f"Create {branch} branch for {model.model_package}."
    )
    new_revision = get_revision_number(
        run_cmdline(
            config.invenio_command,
            "alembic",
            "revision",
            revision_message,
            "-b",
            branch,
            "-p",
            "dbdbc1b19cf2",
            "--empty",
            cwd=config.repository_dir,
            grab_stdout=True,
        ),
        file_revision_name_suffix,
    )
    rewrite_revision_file(alembic_path, "1", branch, new_revision)
    fix_sqlalchemy_utils(alembic_path)
    run_cmdline(
        config.invenio_command, "alembic", "upgrade", "heads", cwd=config.repository_dir
    )

    revision_message, file_revision_name_suffix = get_revision_names(
        "Initial revision."
    )
    new_revision = get_revision_number(
        run_cmdline(
            config.invenio_command,
            "alembic",
            "revision",
            revision_message,
            "-b",
            branch,
            cwd=config.repository_dir,
            grab_stdout=True,
        ),
        file_revision_name_suffix,
    )
    rewrite_revision_file(alembic_path, "2", branch, new_revision)
    # the link to down-revision is created correctly after alembic upgrade heads
    # on the corrected file, explicit rewrite of down-revision is not needed
    fix_sqlalchemy_utils(alembic_path)
    run_cmdline(
        config.invenio_command, "alembic", "upgrade", "heads", cwd=config.repository_dir
    )


def fix_sqlalchemy_utils(alembic_path):
    for fn in alembic_path.iterdir():
        if not fn.name.endswith(".py"):
            continue
        data = fn.read_text()

        empty_migration = '''
def upgrade():
"""Upgrade database."""
# ### commands auto generated by Alembic - please adjust! ###
pass
# ### end Alembic commands ###'''

        if re.sub(r"\s", "", empty_migration) in re.sub(r"\s", "", data):
            click.secho(f"Found empty migration in file {fn}, deleting it", fg="yellow")
            fn.unlink()
            continue

        modified = False
        if "import sqlalchemy_utils" not in data:
            data = "import sqlalchemy_utils\n" + data
            modified = True
        if "import sqlalchemy_utils.types" not in data:
            data = "import sqlalchemy_utils.types\n" + data
            modified = True
        if modified:
            fn.write_text(data)


def get_revision_number(stdout_str, file_suffix):
    mtch = re.search(f"(\w{{12}}){file_suffix}", stdout_str)
    if not mtch:
        raise ValueError("Revision number was not found in revision create stdout")
    return mtch.group(1)


def get_revision_names(revision_message):
    file_name = revision_message[0].lower() + revision_message[1:]
    file_name = "_" + file_name.replace(" ", "_")
    if file_name[-1] == ".":
        file_name = file_name[:-1]

    file_name = file_name[:30]  # there seems to be maximum length for the file name
    idx = file_name.rfind("_")
    file_name = file_name[:idx]  # and all words after it are cut
    return revision_message, file_name


def rewrite_revision_file(
    alembic_path, new_id_number, revision_id_prefix, current_revision_id
):
    files = list(alembic_path.iterdir())
    files_with_this_revision_id = [
        file_name for file_name in files if current_revision_id in str(file_name)
    ]

    if not files_with_this_revision_id:
        raise ValueError(
            "Alembic file rewrite couldn't find the generated revision file"
        )

    if len(files_with_this_revision_id) > 1:
        raise ValueError("More alembic files with the same revision number found")

    target_file = str(files_with_this_revision_id[0])
    new_id = f"{revision_id_prefix}_{new_id_number}"
    with open(target_file, "r") as f:
        file_text = f.read()
        file_text = file_text.replace(
            f"revision = '{current_revision_id}'", f"revision = '{new_id}'"
        )
    with open(target_file.replace(current_revision_id, new_id), "w") as f:
        f.write(file_text)
    os.remove(target_file)
