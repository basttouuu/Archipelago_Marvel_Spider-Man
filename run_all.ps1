$ErrorActionPreference = "Stop"

$coreDir = "C:\Users\hugop\Documents\private\Archipelago\SP\archipelago_core"
$pythonExe = Join-Path $coreDir "venv\Scripts\python.exe"

# 1. Recherche automatique du dernier fichier zip généré dans output/
$latestZip = Get-ChildItem -Path (Join-Path $coreDir "output\*.zip") | Sort-Object LastWriteTime -Descending | Select-Object -First 1

if (-not $latestZip) {
    Write-Host "[ERREUR] Aucun fichier seed .zip trouvé dans $coreDir\output\" -ForegroundColor Red
    exit 1
}

Write-Host "[1/3] Démarrage du MultiServer avec la seed : $($latestZip.Name)..." -ForegroundColor Cyan

# 2. Lancement du serveur dans une fenêtre dédiée
$serverCommand = "cd '$coreDir'; & '$pythonExe' MultiServer.py '$($latestZip.FullName)'"
Start-Process powershell -ArgumentList "-NoExit", "-Command", $serverCommand

# Pause pour laisser le temps au socket 38281 de s'ouvrir
Start-Sleep -Seconds 2

Write-Host "[2/3] Démarrage du SpidermanClient..." -ForegroundColor Cyan

# 3. Lancement du client dans une seconde fenêtre dédiée
$clientCommand = "cd '$coreDir'; & '$pythonExe' SpidermanClient.py"
Start-Process powershell -ArgumentList "-NoExit", "-Command", $clientCommand

Write-Host "`n[3/3] Tout est prêt ! Tu peux maintenant démarrer Spider-Man.exe." -ForegroundColor Green
