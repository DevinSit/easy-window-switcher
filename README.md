# Relative Window Switcher

Idea: Create a script to enable focusing on a window on a specific monitor. This way I could create shortcut keys to invoke it for each of my three monitors. I want this because alt-tab is kinda annoying when multiple of the same windows are in the same workspace.

I'm thinking ctrl+alt+1/2/3 as the shortcut.

# Implementation

- wmctrl seems to be the tool for this
- Instead of working off the actual workspaces by number, it represents them using a single large pane of 'desktop' space (i.e. something like 17280x3240, because 17280=1920*3*3 (3 monitors of width, 3 workspaces wide) and 3240 = 1080*3*1 (1 monitor of height, 3 workspaces heigh)
- As such, something like wmctrl -o works by specifying coordinates in this pane (see https://askubuntu.com/questions/41093/is-there-a-command-to-go-a-specific-workspace for more in depth explanation)
- Can use wmctrl -d to get the coordinates for the current pane after the VP: section (VP = ViewPort)
- Can then use wmctrl -lG to get the complete list of all windows with their coordinates
- Can then use the current coordinates to filter the list of windows to only those in the current viewport/workspace
- Can then focus based on which window is on which monitor

# Other References

- https://superuser.com/questions/142945/bash-command-to-focus-a-specific-window
- https://askubuntu.com/questions/408372/which-are-the-windows-that-are-in-the-current-workspace
- https://askubuntu.com/questions/31240/how-to-shift-applications-from-workspace-1-to-2-using-command

# Idea Extension

- Can also use this to allow relative focus switching, i.e. to focus to the window to the left or right.
- I'm thinking ctrl+super+alt+h/l would work as the shortcut.)
