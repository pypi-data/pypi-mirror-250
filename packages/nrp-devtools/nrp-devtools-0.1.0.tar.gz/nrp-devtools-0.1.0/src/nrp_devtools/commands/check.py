import sys

import click


def check_failed(message):
    click.secho(message, fg="red", err=True)
    sys.exit(1)
