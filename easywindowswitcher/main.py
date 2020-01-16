import click
from typing import Sequence, Union
from easywindowswitcher.commands import groups, root_group
from easywindowswitcher.utils.logger import create_logger


VERSION = "0.0.1"

logger = create_logger()  # noqa: Create the root logger for submodules to use


def construct_cli(cli: click.Group, groups: Sequence[Union[click.Command, click.Group]]) -> click.Group:
    cli = click.version_option(version=VERSION)(cli)

    for group in groups:
        cli.add_command(group)

    return cli


cli = construct_cli(root_group, groups)


if __name__ == "__main__":
    cli()
