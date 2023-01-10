# Welcome to Easy Window Switcher!

`easywindowswitcher` is a small (Python) script for enabling X window users to more easily change focus between windows that are spread across multiple monitors.

**Upgrade your alt-tab!**

Note: `easywindowswitcher` has only been tested in Ubuntu 16.04 under Unity. Your mileage may vary.

## Why did I build Easy Window Switcher?

Because my desktop runs quad monitors and I got so dang tired of having to change between `alt-tab` and `alt-tilde` to target the correct Chrome window.

Not to mention how `alt-tab` handles switching to the last focused window and sometimes focuses onto the wrong window on the wrong monitor.

As such, I decided that it'd be easier to just write a script to be able to **switch focus** to either the **closest left or right window**, or to focus onto the window of a **particular monitor**.

The result is `easywindowswitcher`!

## Dependencies

- Python 3
- `wmctrl` (install using e.g. `sudo apt-get install wmctrl`)
- `xdotool` (install using e.g. `sudo apt-get install xdotool`)

## Installation

Currently `easywindowswitcher` is only available to be installed from source. It will (maybe) be eventually published as a `pip` package.

Thankfully, installing from source isn't too hard!

### From Source

```
git clone git@github.com:DevinSit/easy-window-switcher.git
cd easy-window-switcher
make install
```

## Usage

`easywindowswitcher` is currently pretty small and, as such, supports just two modes of easy window switching: relative direction and absolute monitor position.

### Relative Direction

Switch focus to the closest left or right window:

```
easywindowswitcher direction left
easywindowswitcher direction right
```

### Absolute Monitor Position

Switch focus to the window on the given monitor (indexed from left-to-right, starting at 0):

```
# Monitor 0 would be the left-most monitor
easywindowswitcher monitor 0

# Monitor 1 would be the monitor to the right of the left-most monitor (i.e. monitor 0)
easywindowswitcher monitor 1
```

### Keyboard Shortcuts

Obviously calling `easywindowswitcher` commands directly from a command line isn't exactly the most optimal way to use it. Binding some preset commands to some keyboard shortcuts is much more effective!

Since I'm a `vim` aficionado, might I suggest `ctrl+super+alt+[h/l]` for `easywindowswitcher direction [left/right]`?

And for the absolute monitor positions, I quite like `ctrl+alt+[1/2/3]` for `easywindowswitcher monitor [0/1/2]`.

But you do you!

### :warning: Caveat - Monitor Configuration

`easywindowswitcher` is currently configured to only work with my personal monitor configuration, which is two 1080p monitors stack vertically, followed by a 3440x1440 ultrawide in the center, and a 2560x1440 monitor on right that's in portrait.

If your setup just happens to be the same, then you're in luck! Otherwise, see below for how to customize the code to work with your setup.

#### Customization

1. Go into `easywindowswitcher/data_models/workspace_grid.py` and adjust the `WORKSPACE_HEIGHT` and `WORKSPACE_WIDTH` constants according to the comment in the file explaining how they work.
2. Go into `easywindowswitcher/services/window_focuser.py` and adjust the `NUMBER_OF_MONITORS` constant.
3. Still in `window_focuser.py`, adjust the logic of `_calculate_which_monitor_window_is_on` so that it correctly indexes your monitor setup from left-to-right, top-to-bottom (or whatever you want).

## Roadmap

While GitHub issues are used for public-facing requests, bug reports, etc, a separate **Trello board** is what I personally use to organize what is currently being worked on and what is coming in the future.

It can be found [here](https://trello.com/b/P3DgZTJv/easy-window-switcher).

## Contributing

I don't really expect anyone else to actually contribute to this (tiny) project. On the off chance that you _do_, feel free to open an issue or a pull request. I'll gladly take a look and see if I can help you out!

## Authors

- **Devin Sit**

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.
