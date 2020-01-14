import click
import logging
from easywindowswitcher.utils.command_helpers import log_command_args_factory


logger = logging.getLogger(__name__)
log_command_args = log_command_args_factory(logger, "Root '{}' args")


@click.group()
def root():
    pass


@root.command()
@log_command_args
def test() -> None:
    print("Easy Window Switcher!")
