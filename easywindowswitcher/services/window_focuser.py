import logging
import math
from typing import Dict, List, Optional
from easywindowswitcher.data_models import Window
from easywindowswitcher.external_services import wmctrl

logger = logging.getLogger(__name__)

DIRECTION_LEFT = "left"
DIRECTION_RIGHT = "right"

DIRECTIONS = (DIRECTION_LEFT, DIRECTION_RIGHT)


class WindowFocuser:
    """
    Service that handles focusing onto windows using different metrics
    (e.g. absolute monitor position, relative direction, etc).
    """

    def __init__(self):
        self.wmctrl = wmctrl.WMCtrl()

    def setup(self):
        self.workspace_grid, self.current_workspace = self.wmctrl.get_workspace_config()
        self.windows = self.wmctrl.get_windows_config()

        self.current_workspace_windows = self._get_current_workspace_windows()
        self.current_windows_by_monitor_index = self._index_windows_by_monitor(self.current_workspace_windows)
        self.current_monitors_by_window_index = self._index_monitors_by_window(self.current_workspace_windows)

        self.current_focused_window_id = self.wmctrl.get_current_focused_window_id()
        self.current_monitor = self.current_monitors_by_window_index[self.current_focused_window_id]

    def focus_by_monitor_index(self, monitor_index: int) -> None:
        if monitor_index in self.current_windows_by_monitor_index:
            self.wmctrl.focus_window_by_id(self.current_windows_by_monitor_index[monitor_index][0])

    def focus_by_direction(self, direction: str) -> None:
        if direction in DIRECTIONS:
            window_to_focus = self._get_closest_window(direction)
            self.wmctrl.focus_window_by_id(window_to_focus)
        else:
            logger.info("Invalid direction: {}".format(direction))

    def _get_current_workspace_windows(self) -> List[Window]:
        def in_workspace(window: Window) -> bool:
            # Can find the windows in the current workspace by looking at the x and y offsets.
            # If x-offset isn't negative, the x-offset doesn't exceed the total width of the workspace,
            # and the y-offset doesn't exceed the total height of the workspace,
            # then the window is in the current workspace.

            # Additionally, looking at the x-offset tells us which monitor the window is on:
            # 0 = leftmost monitor, 1920 = center monitor, 3840 = rightmost monitor (for triple 1080p monitors)

            x_offset = window.x_offset
            y_offset = window.y_offset

            return (
                x_offset >= 0
                and x_offset < self.workspace_grid.monitor_width * self.workspace_grid.monitor_horizontal_count
                and y_offset >= 0
                and y_offset < self.workspace_grid.monitor_height * self.workspace_grid.monitor_vertical_count
            )

        return sorted(list(filter(in_workspace, self.windows)), key=lambda window: window.x_offset)

    def _index_windows_by_monitor(self, windows: List[Window]) -> Dict[int, List[int]]:
        windows_by_monitor_index = {}  # type: Dict[int, List[Window]]

        # Create the index of which windows are on which monitor
        for window in windows:
            index = self._calculate_which_monitor_window_is_on(window)
            windows_by_monitor_index.setdefault(index, [])

            windows_by_monitor_index[index].append(window)

        return {
            monitor_index: list(map(
                # Map the windows to just their IDs
                lambda window: window.id,
                # Sort the window lists by x-offset so that they are sorted left-to-right
                sorted(windows, key=lambda window: window.x_offset)
            ))
            for monitor_index, windows in windows_by_monitor_index.items()
        }

    def _index_monitors_by_window(self, windows: List[Window]) -> Dict[int, int]:
        return {window.id: self._calculate_which_monitor_window_is_on(window) for window in windows}

    def _calculate_which_monitor_window_is_on(self, window: Window) -> int:
        # We floor here because any x-offset value between the two edges of a monitor means that
        # the window is on the monitor. That is, anything from 1920 to 3839 (i.e. 1920 * 2 - 1)
        # means that the monitor is on the second monitor (index 1).
        # The division handles getting the actual index (i.e. 1920/1920 = 1 = second monitor).
        return math.floor(window.x_offset / self.workspace_grid.monitor_width)

    def _get_closest_window(self, direction: str) -> Optional[int]:
        current_monitor_windows = self.current_windows_by_monitor_index[self.current_monitor]
        current_window_position = current_monitor_windows.index(self.current_focused_window_id)

        closest_window = None

        if direction == DIRECTION_LEFT:
            if self._is_leftmost_window_on_current_monitor(current_monitor_windows, current_window_position):
                # The modulus operation wraps the monitor index back around if it goes negative.
                # i.e. (0 - 1) % 3 = 2
                left_monitor = (self.current_monitor - 1) % self.workspace_grid.monitor_horizontal_count
                closest_window = self.current_windows_by_monitor_index[left_monitor][-1]
            else:
                # Find the window on the current monitor that is just left of the current window
                closest_window = current_monitor_windows[current_window_position - 1]
        elif direction == DIRECTION_RIGHT:
            if self._is_rightmost_window_on_current_monitor(current_monitor_windows, current_window_position):
                right_monitor = (self.current_monitor + 1) % self.workspace_grid.monitor_horizontal_count
                closest_window = self.current_windows_by_monitor_index[right_monitor][0]
            else:
                # Find the window on the current monitor that is just right of the current window
                closest_window = current_monitor_windows[current_window_position + 1]

        return closest_window

    def _is_leftmost_window_on_current_monitor(
        self, current_monitor_windows: List[int], current_window_position: int
    ) -> bool:
        return len(current_monitor_windows) == 1 or current_window_position == 0

    def _is_rightmost_window_on_current_monitor(
        self, current_monitor_windows: List[int], current_window_position: int
    ) -> bool:
        return len(current_monitor_windows) == 1 or current_window_position == (len(current_monitor_windows) - 1)
