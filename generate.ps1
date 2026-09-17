# =============================================================================
#  Spider-Man Remastered -- Generateur de Seed Archipelago
#  Usage :
#    .\generate.ps1
#    .\generate.ps1 spiderman_solo.yaml
# =============================================================================

param(
    [string]$YamlPath = "spiderman_solo.yaml"
)

$ErrorActionPreference = "Stop"

$rootDir    = $PSScriptRoot
$coreDir    = Join-Path $rootDir "archipelago_core"
$pythonExe  = Join-Path $coreDir "venv\Scripts\python.exe"
$apWorldSrc = Join-Path $rootDir "APLG_MARVEL_SPIDERMAN\apworld\spiderman"
$apWorldDst = Join-Path $coreDir "worlds\spiderman"
$playersDir = Join-Path $coreDir "Players"
$outputDir  = Join-Path $coreDir "output"

Write-Host ""
Write-Host "=======================================================" -ForegroundColor DarkCyan
Write-Host "   Spider-Man Remastered -- Generateur de Seed" -ForegroundColor Cyan
Write-Host "=======================================================" -ForegroundColor DarkCyan
Write-Host ""

# -----------------------------------------------------------------------------
# 1. Verification de l'environnement
# -----------------------------------------------------------------------------
Write-Host "[1/4] Verification de l'environnement..." -ForegroundColor Cyan

if (-not (Test-Path $pythonExe)) {
    Write-Host "      [ERREUR] Python venv introuvable dans : $pythonExe" -ForegroundColor Red
    Write-Host "      Assurez-vous que le venv est bien installe dans archipelago_core\venv\" -ForegroundColor Gray
    exit 1
}
Write-Host "      [OK] Python venv : $pythonExe" -ForegroundColor Green

# -----------------------------------------------------------------------------
# 2. Verification / Synchronisation du lien apworld
# -----------------------------------------------------------------------------
Write-Host ""
Write-Host "[2/4] Synchronisation de l'apworld Spider-Man..." -ForegroundColor Cyan

if (-not (Test-Path $apWorldDst)) {
    Write-Host "      Creation de la jonction worlds\spiderman..." -ForegroundColor Gray
    New-Item -ItemType Junction -Path $apWorldDst -Target $apWorldSrc | Out-Null
    Write-Host "      [OK] Jonction creee vers $apWorldSrc" -ForegroundColor Green
} else {
    $item = Get-Item $apWorldDst
    if ($item.LinkType -ne "Junction") {
        Write-Host "      Mise a jour de l'ancien dossier worlds\spiderman en jonction..." -ForegroundColor Gray
        Remove-Item -Recurse -Force $apWorldDst
        New-Item -ItemType Junction -Path $apWorldDst -Target $apWorldSrc | Out-Null
        Write-Host "      [OK] Jonction mise a jour" -ForegroundColor Green
    } else {
        Write-Host "      [OK] Jonction active vers apworld source" -ForegroundColor Green
    }
}

# -----------------------------------------------------------------------------
# 3. Preparation du fichier YAML du joueur
# -----------------------------------------------------------------------------
Write-Host ""
Write-Host "[3/4] Preparation du fichier joueur..." -ForegroundColor Cyan

# Resolution du chemin YAML
$resolvedYaml = $YamlPath
if (-not [System.IO.Path]::IsPathRooted($resolvedYaml)) {
    $resolvedYaml = Join-Path $rootDir $YamlPath
}

if (-not (Test-Path $resolvedYaml)) {
    # Fallback dans archipelago_core\Players
    $fallback = Join-Path $playersDir $YamlPath
    if (Test-Path $fallback) {
        $resolvedYaml = $fallback
    } else {
        Write-Host "      [ERREUR] Fichier YAML introuvable : $YamlPath" -ForegroundColor Red
        exit 1
    }
}

if (-not (Test-Path $playersDir)) {
    New-Item -ItemType Directory -Path $playersDir | Out-Null
}

# Dans Archipelago, chaque fichier dans Players\ cree un joueur multiworld.
# Pour une partie solo, on deplace les autres fichiers dans un sous-dossier '.disabled'
# que Generate.py ignore (car commence par un point).
$disabledDir = Join-Path $playersDir ".disabled"
if (-not (Test-Path $disabledDir)) {
    New-Item -ItemType Directory -Path $disabledDir | Out-Null
}

$targetLeaf = Split-Path $resolvedYaml -Leaf
$allFiles = Get-ChildItem -Path $playersDir -File
foreach ($f in $allFiles) {
    if ($f.Name -ne $targetLeaf) {
        Move-Item -Path $f.FullName -Destination (Join-Path $disabledDir $f.Name) -Force -ErrorAction SilentlyContinue
    }
}

$destYaml = Join-Path $playersDir $targetLeaf
if ($resolvedYaml -ne $destYaml) {
    Copy-Item -Path $resolvedYaml -Destination $destYaml -Force
}
Write-Host "      [OK] Profil joueur actif : $targetLeaf" -ForegroundColor Green

# -----------------------------------------------------------------------------
# 4. Generation de la seed
# -----------------------------------------------------------------------------
Write-Host ""
Write-Host "[4/4] Generation de la seed via Archipelago Generate.py..." -ForegroundColor Cyan

$timeBefore = Get-Date

# Lancement de Generate.py avec redirection d'entree pour ne pas bloquer sur 'Press enter to close'
cmd /c "echo. | `"$pythonExe`" `"$coreDir\Generate.py`" --player_files_path `"$playersDir`""

$newZips = Get-ChildItem -Path "$outputDir\*.zip" -ErrorAction SilentlyContinue |
           Where-Object { $_.LastWriteTime -ge $timeBefore } |
           Sort-Object LastWriteTime -Descending

if ($newZips) {
    $latest = $newZips | Select-Object -First 1
    Write-Host ""
    Write-Host "=======================================================" -ForegroundColor DarkGreen
    Write-Host "  Seed generee avec succes !" -ForegroundColor Green
    Write-Host "  Fichier : $($latest.Name)" -ForegroundColor White
    Write-Host ""
    Write-Host "  -> Vous pouvez maintenant lancer le jeu et les serveurs :" -ForegroundColor Green
    Write-Host "     .\run_all.ps1" -ForegroundColor Yellow
    Write-Host "=======================================================" -ForegroundColor DarkGreen
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "      [AVERT] La generation s'est terminee mais aucun nouveau .zip detecte dans $outputDir." -ForegroundColor Yellow
    Write-Host "      Verifiez les messages de Generate.py ci-dessus." -ForegroundColor Gray
    Write-Host ""
}
