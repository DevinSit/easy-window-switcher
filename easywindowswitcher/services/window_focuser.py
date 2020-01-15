from typing import List
from easywindowswitcher.data_models import Window
from easywindowswitcher.external_services import wmctrl

class WindowFocuser:
    def __init__(self):
        self.wmctrl = wmctrl.WMCtrl()

        self.workspace_grid, self.current_workspace = self.wmctrl.get_workspace_config()
        self.windows = self.wmctrl.get_windows_config()

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
                and y_offset < self.workspace_grid.monitor_height * self.workspace_grid.monitor_vertical_count
            )

        return list(filter(in_workspace, self.windows))
