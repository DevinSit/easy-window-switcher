class Workspace:
    """
    Models the attributes (specifically, dimensions) of a single Workspace.
    Many Workspaces form a WorkspaceGrid.
    """

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
