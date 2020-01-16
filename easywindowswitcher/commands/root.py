import click
import logging
from easywindowswitcher.utils.command_helpers import log_command_args_factory
from easywindowswitcher.services import window_focuser


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"], max_content_width=180)
DOCSTRING = "A tool for enabling easyier window switching across multiple monitors. Upgrade your alt-tab!"

logger = logging.getLogger(__name__)
log_command_args = log_command_args_factory(logger, "Root '{}' args")

window_focuser_service = window_focuser.WindowFocuser()


@click.group(context_settings=CONTEXT_SETTINGS, help=DOCSTRING)
def root():
    window_focuser_service.setup()


@root.command()
@click.argument("index", type=int)
@log_command_args
def monitor(index: int) -> None:
    """
    Focuses onto the window on the monitor with given index.

    The index is 0 based and increases from left-to-right.
    """
    window_focuser_service.focus_by_monitor_index(index)
