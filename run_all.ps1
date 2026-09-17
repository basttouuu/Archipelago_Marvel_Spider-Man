# =============================================================================
#  Spider-Man Remastered -- Archipelago Launcher
#  Usage : .\run_all.ps1
#
#  Ce script fait 3 choses dans l'ordre :
#    1. Trouver la derniere seed .zip generee dans archipelago_core\output\
#    2. Demarrer le serveur Archipelago (MultiServer.py)
#    3. Demarrer le client Spider-Man (SpidermanClient.py)
#
#  Prerequis :
#    - Avoir genere une seed via le script generate.ps1 (ou manuellement)
#    - Avoir installe le venv Archipelago dans archipelago_core\venv\
# =============================================================================

$ErrorActionPreference = "Stop"

# ---------------------------------------------------------------------------
# CONFIGURATION
# Modifier ces variables si vos chemins sont differents.
# ---------------------------------------------------------------------------
$rootDir      = if ($PSScriptRoot) { $PSScriptRoot } else { (Get-Location).Path }
$coreDir      = Join-Path $rootDir "archipelago_core"
$pythonExe    = Join-Path $coreDir "venv\Scripts\python.exe"
$outputDir    = Join-Path $coreDir "output"
# Le client doit tourner DEPUIS archipelago_core\ pour que 'from CommonClient import ...'
# se resolve. On copie donc la source a chaque lancement (voir ETAPE 3).
$clientSrc    = Join-Path $rootDir "APLG_MARVEL_SPIDERMAN\client\SpidermanClient.py"
$clientDst    = Join-Path $coreDir "SpidermanClient.py"
$apServerPort = 38281   # Port du serveur Archipelago (defaut : 38281)
$ipcPort      = 51234   # Port WebSocket local DLL <-> Client (defaut : 51234)
$maxWaitSecs  = 15      # Secondes max a attendre que le serveur demarre

# ---------------------------------------------------------------------------
# HEADER
# ---------------------------------------------------------------------------
Write-Host ""
Write-Host "=======================================================" -ForegroundColor DarkCyan
Write-Host "   Spider-Man Remastered -- Archipelago Launcher" -ForegroundColor Cyan
Write-Host "=======================================================" -ForegroundColor DarkCyan
Write-Host ""


# ---------------------------------------------------------------------------
# ETAPE 0 : Verification de l'environnement Python
# ---------------------------------------------------------------------------
Write-Host "[0/3] Verification de l'environnement..." -ForegroundColor Cyan

if (-not (Test-Path $pythonExe)) {
    Write-Host "      [ERREUR] Python venv introuvable : $pythonExe" -ForegroundColor Red
    Write-Host ""
    Write-Host "  Pour creer le venv, executez dans $coreDir :" -ForegroundColor Gray
    Write-Host "    python -m venv venv" -ForegroundColor Gray
    Write-Host "    venv\Scripts\pip install -r requirements.txt" -ForegroundColor Gray
    Write-Host ""
    exit 1
}
Write-Host "      [OK] Python venv : $pythonExe" -ForegroundColor Green

# Verifie tout de suite ce dont l'ETAPE 3 aura besoin : echouer ici evite de
# laisser une fenetre MultiServer orpheline derriere nous.
if (-not (Test-Path $clientSrc)) {
    Write-Host "      [ERREUR] Client introuvable : $clientSrc" -ForegroundColor Red
    Write-Host "               Verifiez que le depot est complet." -ForegroundColor Gray
    exit 1
}
Write-Host "      [OK] Source du client : $clientSrc" -ForegroundColor Green

# aiohttp n'est pas une dependance d'Archipelago : sans lui le client meurt sur
# un ImportError dans une fenetre separee, ce qui est difficile a diagnostiquer.
& $pythonExe -c "import aiohttp" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "      [ERREUR] aiohttp manquant dans le venv Archipelago." -ForegroundColor Red
    Write-Host "               Installez-le avec :" -ForegroundColor Gray
    Write-Host "                 & '$pythonExe' -m pip install aiohttp" -ForegroundColor Gray
    exit 1
}
Write-Host "      [OK] aiohttp present dans le venv" -ForegroundColor Green


# ---------------------------------------------------------------------------
# ETAPE 1 : Trouver la derniere seed
# ---------------------------------------------------------------------------
Write-Host ""
Write-Host "[1/3] Recherche de la derniere seed dans output\..." -ForegroundColor Cyan

$allZips = Get-ChildItem -Path "$outputDir\*.zip" -ErrorAction SilentlyContinue |
           Sort-Object LastWriteTime -Descending

if (-not $allZips) {
    Write-Host "      [ERREUR] Aucun fichier .zip trouve dans : $outputDir" -ForegroundColor Red
    Write-Host ""
    Write-Host "  Generez d'abord une seed avec :" -ForegroundColor Gray
    Write-Host "    .\generate.ps1" -ForegroundColor Gray
    Write-Host "  ou manuellement depuis archipelago_core\ :" -ForegroundColor Gray
    Write-Host "    venv\Scripts\python.exe Generate.py" -ForegroundColor Gray
    Write-Host ""
    exit 1
}

$latestZip = $allZips | Select-Object -First 1
$seedAge   = [int]((Get-Date) - $latestZip.LastWriteTime).TotalMinutes

Write-Host "      [OK] Seed : $($latestZip.Name)" -ForegroundColor Green
Write-Host "           (il y a $seedAge minutes)" -ForegroundColor Gray

if ($seedAge -gt 60) {
    Write-Host "      [AVERT] Cette seed date de plus d'une heure. Est-ce bien la bonne ?" -ForegroundColor Yellow
}


# ---------------------------------------------------------------------------
# ETAPE 2 : Demarrer le serveur Archipelago
# ---------------------------------------------------------------------------
Write-Host ""
Write-Host "[2/3] Demarrage du serveur Archipelago (port $apServerPort)..." -ForegroundColor Cyan

$serverCmd = "cd '$coreDir'; & '$pythonExe' MultiServer.py '$($latestZip.FullName)'"
Start-Process powershell -ArgumentList "-NoExit", "-Command", $serverCmd

# Attente active que le port soit accessible
Write-Host "      Attente du port $apServerPort..." -ForegroundColor Gray

$portOpen = $false
for ($i = 1; $i -le $maxWaitSecs; $i++) {
    Start-Sleep -Seconds 1
    $test = Test-NetConnection -ComputerName "127.0.0.1" -Port $apServerPort `
            -WarningAction SilentlyContinue -ErrorAction SilentlyContinue
    if ($test.TcpTestSucceeded) {
        $portOpen = $true
        break
    }
}

if ($portOpen) {
    Write-Host "      [OK] Serveur pret sur le port $apServerPort (${i}s)" -ForegroundColor Green
} else {
    Write-Host "      [AVERT] Port $apServerPort pas encore ouvert apres ${maxWaitSecs}s." -ForegroundColor Yellow
    Write-Host "              Le client demarrera quand meme et reessaiera." -ForegroundColor Gray
}


# ---------------------------------------------------------------------------
# ETAPE 3 : Demarrer le client Spider-Man
# ---------------------------------------------------------------------------
Write-Host ""
Write-Host "[3/3] Demarrage du SpidermanClient (IPC port $ipcPort)..." -ForegroundColor Cyan

# Le client importe CommonClient depuis le core Archipelago : il doit donc etre
# execute depuis $coreDir, sinon l'import echoue. On synchronise la copie a
# chaque lancement pour que les modifications de client\SpidermanClient.py
# soient toujours prises en compte.
Copy-Item -Path $clientSrc -Destination $clientDst -Force
Write-Host "      [OK] Client synchronise vers $clientDst" -ForegroundColor Green
Write-Host "           (relancez ce script apres toute modification du client)" -ForegroundColor Gray

$clientCmd = "cd '$coreDir'; & '$pythonExe' SpidermanClient.py"
Start-Process powershell -ArgumentList "-NoExit", "-Command", $clientCmd

Write-Host "      [OK] Client lance" -ForegroundColor Green


# ---------------------------------------------------------------------------
# INSTRUCTIONS FINALES
# ---------------------------------------------------------------------------
Write-Host ""
Write-Host "=======================================================" -ForegroundColor DarkGreen
Write-Host "  Tout est pret !" -ForegroundColor Green
Write-Host ""
Write-Host "  -> Lancez maintenant Spider-Man Remastered.exe" -ForegroundColor Green
Write-Host ""
Write-Host "  La console du jeu doit afficher :" -ForegroundColor White
Write-Host "    [AP-Mod] Connecte au client Python !" -ForegroundColor Gray
Write-Host ""
Write-Host "  Si ce message n'apparait pas :" -ForegroundColor White
Write-Host "    - Verifiez que dxgi.dll est dans le dossier du jeu" -ForegroundColor Gray
Write-Host "    - Verifiez que le client Python est bien connecte" -ForegroundColor Gray
Write-Host "=======================================================" -ForegroundColor DarkGreen
Write-Host ""
