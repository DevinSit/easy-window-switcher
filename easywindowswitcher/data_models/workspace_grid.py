from typing import List
from .workspace import Workspace

# These are assumptions about how the user's workspaces are setup (based on their monitors).
#
# For example, three horizontally-aligned 1920x1080 monitors would have a single workspace dimension of:
#
# WORKSPACE_HEIGHT = 1 x 1080
# WORKSPACE_WIDTH = 3 x 1920
#
# For the values below, they are calculated using a quad-monitor setup that looks like this:
#
# [1920x1080]
#               [3440x1440]     [1440x2560]
# [1920x1080]
#
# That is, two vertically stacked 1080p monitors on the left, with a 3440x1440 ultrawide in the middle,
# and a portrait 2560x1440 monitor on the right.
#
# With this setup, these values are calculated as follows:
#
# WORKSPACE_HEIGHT = 2560 (aka the max height of all the monitors)
# WORKSPACE_WIDTH = 1920 + 3440 + 1440
WORKSPACE_HEIGHT = 2560
WORKSPACE_WIDTH = 6800

WORKSPACE_HORIZONTAL_COUNT = 3
WORKSPACE_VERTICAL_COUNT = 3


class WorkspaceGrid:
    """
    Models the attributes of the whole workspace grid for a windowed desktop environment.
    This includes things like how many workspaces exist, in what layout, with how many monitors, etc.
    """

    def __init__(
        self,
        raw_dimensions: str = "",
        height: int = 0,
        width: int = 0,
        workspace_height: int = WORKSPACE_HEIGHT,
        workspace_width: int = WORKSPACE_WIDTH,
        workspace_horizontal_count: int = WORKSPACE_HORIZONTAL_COUNT,
        workspace_vertical_count: int = WORKSPACE_VERTICAL_COUNT,
    ) -> None:
        if raw_dimensions:
            self._process_raw_dimensions(raw_dimensions)
        else:
            self.height = height
            self.width = width

        self.workspace_height = workspace_height
        self.workspace_width = workspace_width

        self.workspace_horizontal_count = workspace_horizontal_count
        self.workspace_vertical_count = workspace_vertical_count

        self.workspace_indices = self._generate_workspace_indices(
            self.workspace_horizontal_count, self.workspace_vertical_count
        )

    def get_workspace_index(self, workspace: Workspace) -> int:
        """
        Gets the index of the given workspace within the whole workspace grid.

        Workspaces, for our purposes, are indexed in order from left to right, top to bottom.
        i.e. in a 3x3 grid, the top-leftmost workspace is 0, then the top-center workspace is 1, etc

        Example using a 3x3 grid with three horizontally-aligned 1920x1080 monitors:

        X         Y       Index
        0,        0       0
        5760      0       1
        11520     0       2
        0         1080    3
        5760      1080    4
        11520     1080    5
        0         2160    6
        5760      2160    7
        11520     2160    8
        """

        horizontal_index = int(workspace.width / self.workspace_width)
        vertical_index = int(workspace.height / self.workspace_height)

        return self.workspace_indices[vertical_index][horizontal_index]

    def __repr__(self):
        return "{}x{}".format(self.width, self.height)

    def _process_raw_dimensions(self, raw_dimensions: str) -> None:
        split_dimensions = raw_dimensions.split("x")

        self.height = int(split_dimensions[1])
        self.width = int(split_dimensions[0])

    def _generate_workspace_indices(
        self, horizontal_count: int, vertical_count: int
    ) -> List[List[int]]:
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
