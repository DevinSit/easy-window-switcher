from typing import List, Tuple
from easywindowswitcher.data_models import Window, Workspace, WorkspaceGrid
from easywindowswitcher.utils.service_helpers import get_command_output, call_command


class WMCtrl:
    """
    'wmctrl' (i.e. window manager control? window management controller?) is a
    command line utility for reading information about the current state of a
    desktop environment's workspaces and windows.

    This class wraps the command line calls to this utility and exposes the
    information in a more useful format.
    """

    def __init__(self):
        pass

    def get_workspace_config(self) -> Tuple[WorkspaceGrid, Workspace]:
        workspace_config = get_command_output(["wmctrl", "-d"])
        return self._parse_system_config(workspace_config)

    def get_windows_config(self):
        windows_config = get_command_output(["wmctrl", "-l", "-G", "-x"])
        return self._parse_windows_config(windows_config)

    def get_current_focused_window_id(self) -> int:
        # Note: Unlike `wmctrl`, `xdotool` returns window IDs in decimal, instead of in hex.
        return int(get_command_output(["xdotool", "getwindowfocus"]))

    def focus_window_by_id(self, window_id: int) -> None:
        call_command(["wmctrl", "-i", "-a", str(window_id)])

    def _parse_system_config(self, system_config) -> Tuple[WorkspaceGrid, Workspace]:
        # Example system_config: "0  * DG: 17280x3240  VP: 5760,0  WA: 0,24 5760x1056  N/A"
        first_splits = system_config.split("DG:")[1].split("VP:")

        workspace_grid = WorkspaceGrid(raw_dimensions=first_splits[0].strip())
        current_workspace = Workspace(raw_dimensions=first_splits[1].split("WA:")[0].strip())

        return (workspace_grid, current_workspace)

    def _parse_windows_config(self, windows_config) -> List[Window]:
        split_windows_config = windows_config.split("\n")
        windows = []

        for window_config in split_windows_config:
            window = Window(raw_config=window_config)

            # Any 'window' that doesn't have a window_class isn't a window (e.g. unity-launcher).
            # Any window where the y-offset is actually 0 means that it doesn't have
            # any window decoration and is therefore not a window (e.g. Nautilus).
            # Additionally, I don't think I've seen a negative y-offset value for a legit window,
            # so we can shortcut that logic.
            if window.window_class != "N/A" and window.y_offset > 0:
                windows.append(window)

        return windows
