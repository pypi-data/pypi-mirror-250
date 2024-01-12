import click
from pytimedinput import timedInput

from .runner import Runner
from nrp_devtools.config import OARepoConfig


def show_menu(server: bool, ui: bool, development_mode: bool):
    click.secho("")
    click.secho("")
    if development_mode:
        click.secho("Development server is running", fg="green")
    else:
        click.secho("Production server is running", fg="yellow")
    click.secho("")
    click.secho("=======================================")
    click.secho("")
    if server:
        click.secho("1 or server     - restart python server", fg="green")
    if ui and development_mode:
        click.secho("2 or ui         - restart webpack server", fg="green")

    click.secho("0 or stop       - stop the server (Ctrl-C also works)", fg="red")
    click.secho("")
    click.secho("")


def run_develop_controller(
    config: OARepoConfig, runner: Runner, server=True, ui=True, development_mode=False
):
    while True:
        show_menu(server, ui, development_mode)
        (choice, timed_out) = timedInput(prompt="Your choice: ", timeout=60)
        if timed_out:
            continue
        choice = choice.strip()
        print("Got choice", choice)
        if choice in ("0", "stop"):
            runner.stop()
            break
        elif choice in ("1", "server"):
            runner.restart_python_server(development_mode=development_mode)
        elif choice in ("2", "ui"):
            runner.restart_webpack_server()
