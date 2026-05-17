# StartWork Launcher

Version: `1.3.3`

StartWork Launcher is a small Windows app for launching a saved set of work apps, folders, files, and websites.

## Features

- Dark Tkinter interface.
- Multiple launch profiles.
- Add apps, folders, files, and links from the interface.
- Launch a selected item or a full profile.
- First-run wizard.
- Import and export profiles.
- Windows startup toggle.
- Keyboard shortcuts.
- Profile icons.
- Steam-like profile picker.
- Custom profile avatars.
- Detected app library for browsers, Telegram, Steam, VS Code, and Windows tools.
- Language selector with English, Russian, Chinese, Spanish, German, French, Japanese, and Korean.
- Built-in update checker.
- PowerShell fallback launcher for `apps.txt`.

## Run

For regular users, download the ready archive:

```text
release/StartWorkLauncher-1.3.3.zip
```

Unzip it and run:

```text
StartWorkLauncher.exe
```

The exe build does not require Python.

## Hotkeys

- `Ctrl+Enter`: launch current profile.
- `Ctrl+N`: create profile.
- `Ctrl+I`: import profile.
- `Ctrl+E`: export profile.
- `Delete`: remove selected item.
- `F5`: save profile.

## Run From Source

This project is Python source code, not a compiled `.exe`.

The other user must have Python 3 installed on Windows. During installation, enable:

```text
Add python.exe to PATH
```

Use:

```bat
LaunchStartWork.cmd
```

Or run the GUI directly:

```bat
pythonw StartWorkApp.pyw
```

## Profiles

Profiles are stored in the `profiles` folder as `.txt` files. The default profile is `Work`.

Each non-empty line is one item to launch. Lines starting with `#` are comments.

## Common Problem

If nothing happens after double-clicking the launcher, Python is probably missing or unavailable in `PATH`.

Install Python 3 from:

https://www.python.org/downloads/

Then run `LaunchStartWork.cmd` again.
