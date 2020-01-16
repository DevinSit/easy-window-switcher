import math
from typing import Dict, List
from easywindowswitcher.data_models import Window
from easywindowswitcher.external_services import wmctrl

class WindowFocuser:
    def __init__(self):
        self.wmctrl = wmctrl.WMCtrl()

        self.workspace_grid, self.current_workspace = self.wmctrl.get_workspace_config()
        self.windows = self.wmctrl.get_windows_config()

    def focus_by_monitor_index(self, monitor_index: int) -> None:
        current_workspace_windows = self._get_current_workspace_windows()
        windows_by_monitor_index = self._index_windows_by_monitor(current_workspace_windows)

        if monitor_index in windows_by_monitor_index:
            self.wmctrl.focus_window_by_id(windows_by_monitor_index[monitor_index].id)

    def _get_current_workspace_windows(self) -> List[Window]:
        def in_workspace(window: Window) -> bool:
            # Can find the windows in the current workspace by looking at the x and y offsets.
            # If x-offset isn't negative, the x-offset doesn't exceed the total width of the workspace,
            # and the y-offset doesn't exceed the total height of the workspace,
            # then the window is in the current workspace.

            # Additionally, looking at the x-offset tells us which monitor the window is on:
            # 0 = leftmost monitor, 1920 = center monitor, 3840 = rightmost monitor

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
            index = math.floor(window.x_offset / self.workspace_grid.monitor_width)
            windows_by_monitor_index[index] = window

        return windows_by_monitor_index
