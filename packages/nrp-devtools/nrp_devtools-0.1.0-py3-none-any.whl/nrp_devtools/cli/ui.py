import json

import click

from ..commands.ui.create import (
    create_model_ui,
    create_page_ui,
    register_model_ui,
    register_page_ui,
)
from ..commands.utils import make_step
from ..config import OARepoConfig
from ..config.ui_config import UIConfig
from .base import command_sequence, nrp_command


@nrp_command.group(name="ui")
def ui_group():
    """
    UI management commands.
    """


"""
nrp ui pages create <ui-name> <ui-endpoint>
```

The `ui-endpoint` is the endpoint of the root for pages, for example
`/docs` or `/search`. The `ui-name` is the name of the collection of pages,
such as `docs` or `search`.

If `ui-endpoint` is not specified, it will be the same as
`ui-name` with '/' prepended.
"""


@ui_group.group(name="pages")
def pages_group():
    """
    UI pages management commands.
    """


@pages_group.command(
    name="create",
    help="""Create a new UI pages collection. 
    The ui-name is the name of the collection of pages, such as docs or search,
    ui-endpoint is the url path of the pages' root, for example /docs or /search. 
    If not specified, it will be the same as ui-name with '/' prepended.
    """,
)
@click.argument("ui-name")
@click.argument(
    "ui-endpoint",
    required=False,
)
@command_sequence()
def create_pages(config: OARepoConfig, ui_name, ui_endpoint, **kwargs):
    """
    Create a new UI pages collection.
    """
    ui_name = ui_name.replace("-", "_")
    ui_endpoint = ui_endpoint or ("/" + ui_name.replace("_", "-"))
    if not ui_endpoint.startswith("/"):
        ui_endpoint = "/" + ui_endpoint

    if config.get_ui(ui_name, default=None):
        click.secho(f"UI {ui_name} already exists", fg="red", err=True)
        return

    def set_ui_configuration(config: OARepoConfig, *args, **kwargs):
        config.add_ui(UIConfig(name=ui_name, endpoint=ui_endpoint))

    return (
        set_ui_configuration,
        make_step(create_page_ui, ui_name=ui_name),
        make_step(register_page_ui, ui_name=ui_name),
    )


@ui_group.group(name="model")
def model_group():
    """
    UI model management commands
    """


@model_group.command(
    name="create",
    help="""Create a new UI for metadata model. 
    The model-name is the name of the model, such as documents or records,
    ui-name is the name of the ui (default is the same as model-name).
    ui-endpoint, if not passed, is taken from the model's resource-config, 
    field base-html-url.
    """,
)
@click.argument("model-name")
@click.argument("ui-name", required=False)
@click.argument(
    "ui-endpoint",
    required=False,
)
@command_sequence()
def create_model(config: OARepoConfig, model_name, ui_name, ui_endpoint, **kwargs):
    """
    Create a new UI model.
    """
    if not ui_name:
        ui_name = model_name

    ui_name = ui_name.replace("-", "_")

    if config.get_ui(ui_name, default=None):
        click.secho(f"UI {ui_name} already exists", fg="red", err=True)
        return

    def set_ui_configuration(config: OARepoConfig, *args, **kwargs):
        nonlocal ui_endpoint

        model = config.get_model(model_name)

        model_data = json.loads(
            (
                config.repository_dir / model.model_package / "models" / "records.json"
            ).read_text()
        )
        api_service = model_data["model"]["service-config"]["service-id"]
        ui_serializer_class = model_data["model"]["json-serializer"]["class"]
        if not ui_endpoint:
            ui_endpoint = model_data["model"]["resource-config"]["base-html-url"]

        config.add_ui(
            UIConfig(
                name=ui_name,
                endpoint=ui_endpoint,
                model=model_name,
                api_service=api_service,
                ui_serializer_class=ui_serializer_class,
            )
        )

    return (
        set_ui_configuration,
        make_step(create_model_ui, ui_name=ui_name),
        make_step(register_model_ui, ui_name=ui_name),
    )
