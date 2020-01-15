from typing import Tuple
from easywindowswitcher.data_models import Window, Workspace, WorkspaceGrid
from easywindowswitcher.utils.service_helpers import get_command_output


class WMCtrl:
    def __init__(self):
        pass

    def test(self):
        system_config = get_command_output(["wmctrl", "-d"])
        workspace_grid, current_workspace = self._extract_system_config(system_config)

        index = workspace_grid.get_workspace_index(current_workspace)
        print(index)

    def test2(self):
        windows_config = get_command_output(["wmctrl", "-l", "-G", "-x"])

        print(self._extract_windows(windows_config))

    def _extract_system_config(self, system_config) -> Tuple[WorkspaceGrid, Workspace]:
        # Example system_config: "0  * DG: 17280x3240  VP: 5760,0  WA: 0,24 5760x1056  N/A"
        first_splits = system_config.split("DG:")[1].split("VP:")

        workspace_grid = WorkspaceGrid(raw_dimensions=first_splits[0].strip())
        current_workspace = Workspace(raw_dimensions=first_splits[1].split("WA:")[0].strip())

        return (workspace_grid, current_workspace)

    def _extract_windows(self, windows_config):
        # Can find the monitors in the current workspace by looking at the x and y offsets.
        # If x-offset isn't negative and y-offset is 24 (??), then the monitor is in the current workspace.

        # I believe the 24 y-offset is just due to things like window decorations and the global menu bar.
        # Can just look for the smallest y-offset value and use that as the baseline.

        # Additionally, looking at the x-offset tells us which monitor the window is on:
        # 0 = leftmost monitor, 1920 = center monitor, 3840 = rightmost monitor

        split_windows_config = windows_config.split("\n")
        return list(map(lambda window_config: Window(raw_config=window_config), split_windows_config))
