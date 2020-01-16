import math
from typing import Dict, List
from easywindowswitcher.data_models import Window
from easywindowswitcher.external_services import wmctrl


class WindowFocuser:
    """
    Service that handles focusing onto windows using different metrics
    (e.g. absolute monitor position, relative direction, etc).
    """

    def __init__(self):
        self.wmctrl = wmctrl.WMCtrl()

        self.workspace_grid, self.current_workspace = self.wmctrl.get_workspace_config()
        self.windows = self.wmctrl.get_windows_config()

    def focus_by_monitor_index(self, monitor_index: int) -> None:
        current_workspace_windows = self._get_current_workspace_windows()
        windows_by_monitor_index = self._index_windows_by_monitor(current_workspace_windows)

        if monitor_index in windows_by_monitor_index:
            self.wmctrl.focus_window_by_id(windows_by_monitor_index[monitor_index][0].id)

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

    def _index_windows_by_monitor(self, windows: List[Window]) -> Dict[int, List[Window]]:
        windows_by_monitor_index = {}  # type: Dict[int, List[Window]]

        for window in windows:
            # We floor here because any x-offset value between the two edges of a monitor means that
            # the window is on the monitor. That is, anything from 1920 to 3839 (i.e. 1920 * 2 - 1)
            # means that the monitor is on the second monitor (index 1).
            # The division handles getting the actual index (i.e. 1920/1920 = 1 = second monitor).
            index = math.floor(window.x_offset / self.workspace_grid.monitor_width)
            windows_by_monitor_index.setdefault(index, [])

            windows_by_monitor_index[index].append(window)

        return windows_by_monitor_index
