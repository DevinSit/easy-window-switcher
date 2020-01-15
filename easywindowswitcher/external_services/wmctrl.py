from typing import List, Tuple
from easywindowswitcher.data_models import Window, Workspace, WorkspaceGrid
from easywindowswitcher.utils.service_helpers import get_command_output


class WMCtrl:
    def __init__(self):
        pass

    def get_workspace_config(self) -> Tuple[WorkspaceGrid, Workspace]:
        workspace_config = get_command_output(["wmctrl", "-d"])
        return self._parse_system_config(workspace_config)

    def get_windows_config(self):
        windows_config = get_command_output(["wmctrl", "-l", "-G", "-x"])
        return self._parse_windows_config(windows_config)

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
