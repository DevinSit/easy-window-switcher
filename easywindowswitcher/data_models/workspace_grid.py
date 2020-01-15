from typing import List
from .workspace import Workspace

# These are assumptions about how the user's monitor environment is setup.
MONITOR_HORIZONTAL_COUNT = 3
MONITOR_VERTICAL_COUNT = 1
MONITOR_HEIGHT = 1080
MONITOR_WIDTH = 1920

WORKSPACE_HORIZONTAL_COUNT = 3
WORKSPACE_VERTICAL_COUNT = 3


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
