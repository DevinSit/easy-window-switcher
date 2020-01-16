class Window:
    """
    Models the attributes of a single window (on a monitor, in a workspace, in the workspace grid).
    Specifically, it cares about things like where the window is positioned relative to the current
    workspace (i.e. x and y offset) as well as the ID/title of the window.
    """

    def __init__(
        self,
        raw_config: str = "",
        id: str = "",
        x_offset: int = 0,
        y_offset: int = 0,
        height: int = 0,
        width: int = 0,
        window_class: str = "",
        title: str = ""
    ) -> None:
        """
        :param id: A string representation of the (hex) ID for the window.

        :param x_offset and y_offset:

            x and y offset are how windows (specifically, their top-left corner, not including window decoration)
            are positioned relative to the current workspace. Some examples (given a triple 1080p monitor setup):

            - An x,y offset of 0,0 would put the window on the left-most monitor.
            - An x,y offset of 0,24 also puts the window on the left-most monitor,
                but the y-offset has accounted for window decoration (this is what's most commonly seen).
            - An x,y offset of 1920,24 puts the window in the center monitor, because it is positioned 1920 pixels
                from the left-most edge of the workspace.

        :param height: The height of the window (in pixels).
        :param width: The width of the window (in pixels).
        :param window_class: The class of the window (e.g. "google-chrome.Google-chrome")
        :param title: The title of the window.
        """

        if raw_config:
            self._process_raw_config(raw_config)
        else:
            self.x_offset = x_offset
            self.y_offset = y_offset
            self.width = width
            self.window_class = window_class
            self.title = title

    def __repr__(self):
        return "ID: {}\nX Offset: {}\nY Offset: {}\nDimensions: {}x{}\nClass: {}\nTitle: {}".format(
            self.id, self.x_offset, self.y_offset, self.width, self.height, self.window_class, self.title
        )

    def _process_raw_config(self, raw_config: str) -> None:
        """
        Processes the raw string representation of the window config into
        all of the attributes needed for the Window instance.

        Example: "0x05000006  0 1920 24   1920 1056 gnome-terminal-server.Gnome-terminal  devin-Desktop Terminal"

        Column 0 is the window ID (0x05000006)
        Column 1 is the 'desktop index' (almost always 0 for our uses in Unity; can just ignore)
        Column 2 is the x-offset (1920)
        Column 3 is the y-offset (24)
        Column 4 is the window width (1920)
        Column 5 is the window height (1056)
        Column 6 is the WM_CLASS property from the '-x' option (gnome-terminal-server.Gnome-terminal)
        Column 7 is presumably just the hostname (devin-Desktop)
        Everything after column 7 is the title of the window (Terminal)
        """
        # Need to remove any empty strings that are left after splitting
        split_config = list(filter(None, raw_config.split(" ")))

        self.id = split_config[0]
        self.x_offset = int(split_config[2])
        self.y_offset = int(split_config[3])
        self.width = int(split_config[4])
        self.height = int(split_config[5])
        self.window_class = split_config[6]
        self.title = " ".join(split_config[8:])
