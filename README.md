# StartWork Launcher

Version: `1.0.0`

StartWork Launcher is a small Windows app for launching a saved set of work apps, folders, files, and websites.

## Features

- Dark Tkinter interface.
- Multiple launch profiles.
- Add apps, folders, files, and links from the interface.
- Launch a selected item or a full profile.
- PowerShell fallback launcher for `apps.txt`.

## Run

Use:

```bat
LaunchStartWork.cmd
```

Or run the GUI directly:

```bat
pythonw StartWorkApp.pyw
```

## Profiles

Profiles are stored in the `profiles` folder as `.txt` files. The default profile is `Работа`.

Each non-empty line is one item to launch. Lines starting with `#` are comments.
