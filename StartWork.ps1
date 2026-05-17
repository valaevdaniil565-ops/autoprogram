param(
    [string]$ConfigPath = (Join-Path $PSScriptRoot "apps.txt")
)

$ErrorActionPreference = "Continue"

function Write-Info {
    param([string]$Message)
    Write-Host "[StartWork] $Message"
}

if (-not (Test-Path -LiteralPath $ConfigPath)) {
    Write-Host "Config file not found: $ConfigPath" -ForegroundColor Red
    exit 1
}

$items = Get-Content -LiteralPath $ConfigPath |
    ForEach-Object { $_.Trim() } |
    Where-Object { $_ -and -not $_.StartsWith("#") }

if (-not $items) {
    Write-Host "No apps configured. Edit apps.txt and add one app, folder, file, or URL per line." -ForegroundColor Yellow
    exit 0
}

Write-Info "Launching $($items.Count) item(s)..."

foreach ($item in $items) {
    try {
        if ($item -match "^(https?://|mailto:)") {
            Write-Info "Opening URL: $item"
            Start-Process $item
            continue
        }

        if (Test-Path -LiteralPath $item) {
            Write-Info "Opening path: $item"
            Start-Process -FilePath $item
            continue
        }

        Write-Info "Starting command/app: $item"
        Start-Process -FilePath $item
    }
    catch {
        Write-Host "[StartWork] Failed to launch: $item" -ForegroundColor Red
        Write-Host "  $($_.Exception.Message)" -ForegroundColor DarkRed
    }
}

Write-Info "Done."
Start-Sleep -Seconds 2
