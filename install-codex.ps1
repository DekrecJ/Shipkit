$ErrorActionPreference = "Stop"
Push-Location $PSScriptRoot
try {
    if (Get-Command py -ErrorAction SilentlyContinue) {
        py -3 -m pip install --upgrade .
        py -3 -m shipkit install codex
        py -3 -m shipkit doctor
    }
    elseif (Get-Command python -ErrorAction SilentlyContinue) {
        python -m pip install --upgrade .
        python -m shipkit install codex
        python -m shipkit doctor
    }
    else {
        throw "Python 3.10+ was not found. Install Python, then run this script again."
    }

    Write-Host ""
    Write-Host "ShipKit installation finished. Restart Codex before testing a new chat." -ForegroundColor Green
}
finally {
    Pop-Location
}
