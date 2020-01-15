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
@log_command_args
def test() -> None:
    print(window_focuser_service._get_current_workspace_windows())
