class Window:
    def __init__(
        self,
        raw_config: str = "",
        id: int = 0,
        x_offset: int = 0,
        y_offset: int = 0,
        height: int = 0,
        width: int = 0,
        window_class: str = "",
        title: str = ""
    ) -> None:
        if raw_config:
            self._process_raw_config(raw_config)
        else:
            self.x_offset = x_offset
            self.y_offset = y_offset
            self.width = width
            self.window_class = window_class
            self.title = title

    def __repr__(self):
        return "\n\nID: {}\nX Offset: {}\nY Offset: {}\nDimensions: {}x{}\nClass: {}\nTitle: {}".format(
            self.id, self.x_offset, self.y_offset, self.width, self.height, self.window_class, self.title
        )

    def _process_raw_config(self, raw_config: str) -> None:
        # Example: "0x05000006  0 1920 24   1920 1056 gnome-terminal-server.Gnome-terminal  devin-Desktop Terminal"
        #
        # Column 0 is window ID (0x05000006)
        # Column 1 is the 'desktop index' (always 0 for our uses in Unity; can just ignore)
        # Column 2 is the x-offset (1920)
        # Column 3 is the y-offset (24)
        # Column 4 is the window width (1920)
        # Column 5 is the window height (1056)
        # Column 6 is the WM_CLASS property from the '-x' option (gnome-terminal-server.Gnome-terminal)
        # Column 7 is presumably just the hostname (devin-Desktop)
        # Everything after column 7 is the title of the window

        # Need to remove any empty strings that are left after splitting
        split_config = list(filter(None, raw_config.split(" ")))

        self.id = split_config[0]
        self.x_offset = split_config[2]
        self.y_offset = split_config[3]
        self.width = split_config[4]
        self.height = split_config[5]
        self.window_class = split_config[6]
        self.title = " ".join(split_config[8:])
