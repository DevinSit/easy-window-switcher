from typing import List, Tuple
from easywindowswitcher.utils.service_helpers import get_command_output

# These are assumptions about how the user's monitor environment is setup.
MONITOR_HORIZONTAL_COUNT = 3
MONITOR_VERTICAL_COUNT = 1
MONITOR_HEIGHT = 1080
MONITOR_WIDTH = 1920

WORKSPACE_HORIZONTAL_COUNT = 3
WORKSPACE_VERTICAL_COUNT = 3


class Workspace:
    def __init__(self, raw_dimensions: str = "", width: int = 0, height: int = 0) -> None:
        if raw_dimensions:
            self._process_raw_dimensions(raw_dimensions)
        else:
            # Note that Workspace dimensions represent the top-leftmost pixel of a workspace.
            # e.g. 0,0 is the first workspace, 5760,0 is the second workspace for 3 1920x1080 monitors, etc.
            self.width = width
            self.height = height

    def __repr__(self):
        return "{},{}".format(self.width, self.height)

    def _process_raw_dimensions(self, raw_dimensions: str) -> None:
        split_dimensions = raw_dimensions.split(",")

        self.width = int(split_dimensions[0])
        self.height = int(split_dimensions[1])


class WorkspaceGrid:
    def __init__(
        self,
        raw_dimensions: str = "",
        height: int = 0,
        width: int = 0,
        monitor_horizontal_count: int = MONITOR_HORIZONTAL_COUNT,
        monitor_vertical_count: int = MONITOR_VERTICAL_COUNT,
        monitor_height: int = MONITOR_HEIGHT,
        monitor_width: int = MONITOR_WIDTH,
        workspace_horizontal_count: int = WORKSPACE_HORIZONTAL_COUNT,
        workspace_vertical_count: int = WORKSPACE_VERTICAL_COUNT
    ) -> None:
        if raw_dimensions:
            self._process_raw_dimensions(raw_dimensions)
        else:
            self.height = height
            self.width = width

        self.monitor_horizontal_count = monitor_horizontal_count
        self.monitor_vertical_count = monitor_vertical_count
        self.monitor_height = monitor_height
        self.monitor_width = monitor_width

        self.workspace_horizontal_count = workspace_horizontal_count
        self.workspace_vertical_count = workspace_vertical_count

        self.workspace_indices = self._generate_workspace_indices(
            self.workspace_horizontal_count, self.workspace_vertical_count
        )

    def get_workspace_index(self, workspace: Workspace) -> int:
        # Workspaces, for our purposes, are indexed in order from left to right, top to bottom.
        # i.e. in a 3x3 grid, the top-leftmost workspace is 0, then the top-center workspace is 1, etc.

        # TODO: Remove
        # 0,      0       0
        # 5760    0       1
        # 11520   0       2
        # 0       1080    3
        # 5760    1080    4
        # 11520   1080    5
        # 0       2160    6
        # 5760    2160    7
        # 11520   2160    8

        horizontal_index = int(workspace.width / self.monitor_width / self.monitor_horizontal_count)
        vertical_index = int(workspace.height / self.monitor_height / self.monitor_vertical_count)

        return self.workspace_indices[vertical_index][horizontal_index]

    def __repr__(self):
        return "{}x{}".format(self.width, self.height)

    def _process_raw_dimensions(self, raw_dimensions: str) -> None:
        split_dimensions = raw_dimensions.split("x")

        self.height = int(split_dimensions[1])
        self.width = int(split_dimensions[0])

    def _generate_workspace_indices(self, horizontal_count: int, vertical_count: int) -> List[List[int]]:
        """
        Builds a 2D list to represent the grid of workspaces, where each cell is the index.

        For example, a 3x3 workspace grid would look like this:

            [[0, 1, 2],
             [3, 4, 5],
             [6, 7, 8]]
        """
        indices_grid = []  # type: List[List[int]]

        for i in range(vertical_count):
            indices_grid.append([])

            for j in range(horizontal_count):
                indices_grid[i].append((i * horizontal_count) + j)

        return indices_grid


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

        # Example: "0x05000006  0 1920 24   1920 1056 gnome-terminal-server.Gnome-terminal  devin-Desktop Terminal"
        # Column 1 is window ID (0x05000006)
        # Column 2 is the 'desktop index' (always 0 for our uses in Unity; can just ignore)
        # Column 3 is the x-offset (1920)
        # Column 4 is the y-offset (24)
        # Column 5 is the window height (1920)
        # Column 6 is the window width (1056)
        # Column 7 is the WM_CLASS property from the '-x' option (gnome-terminal-server.Gnome-terminal)
        # Everything after column 7 ('column' 8) is the title of the window

        return windows_config.split("\n")
