$ErrorActionPreference = "Stop"

$Source = Split-Path -Parent $MyInvocation.MyCommand.Path
$InstallDir = Join-Path $env:LOCALAPPDATA "StartWorkLauncher"
$Exe = Join-Path $InstallDir "StartWorkLauncher.exe"
$Desktop = [Environment]::GetFolderPath("Desktop")
$Shortcut = Join-Path $Desktop "StartWork Launcher.lnk"

New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null
Copy-Item -LiteralPath (Join-Path $Source "*") -Destination $InstallDir -Recurse -Force

$Shell = New-Object -ComObject WScript.Shell
$Link = $Shell.CreateShortcut($Shortcut)
$Link.TargetPath = $Exe
$Link.WorkingDirectory = $InstallDir
$Icon = Join-Path $InstallDir "StartWork.ico"
if (Test-Path -LiteralPath $Icon) {
    $Link.IconLocation = $Icon
}
$Link.Save()

Write-Host "Installed StartWork Launcher to $InstallDir"
Write-Host "Desktop shortcut created: $Shortcut"
