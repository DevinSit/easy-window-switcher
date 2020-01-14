import click  # noqa
from typing import List  # noqa
from . import root

groups = []  # type: List[click.Group]
commands = root.root.commands.values()
