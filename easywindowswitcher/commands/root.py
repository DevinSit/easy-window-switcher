import click
import logging
from easywindowswitcher.utils.command_helpers import log_command_args_factory
from easywindowswitcher.external_services import wmctrl
from easywindowswitcher.services import window_focuser

wmctrl_service = wmctrl.WMCtrl()
window_focuser_service = window_focuser.WindowFocuser()


logger = logging.getLogger(__name__)
log_command_args = log_command_args_factory(logger, "Root '{}' args")


@click.group()
def root():
    pass


@root.command()
@click.argument("index", type=int)
@log_command_args
def monitor(index: int) -> None:
    """
    Focuses onto the window on the monitor with given index.

    The index is 0 based and increases from left-to-right.
    """
    window_focuser_service.focus_by_monitor_index(index)
