# Marvel's Spider-Man Remastered — Archipelago Randomizer

> Intégration du jeu **Marvel's Spider-Man Remastered** (PC/Steam) dans le système de randomisation [Archipelago](https://archipelago.gg/).

---

## Vue d'ensemble

Ce mod transforme Spider-Man Remastered en participant d'un **multiworld Archipelago**.  
Les gadgets, compétences et déblocages de quartier sont mélangés dans la pool partagée, et chaque check (sac à dos, boss, base ennemie…) peut contenir un item appartenant à n'importe quel autre joueur du multiworld.

### Architecture

```
┌──────────────────────┐        WebSocket (38281)       ┌────────────────────────────┐
│  Archipelago Server  │ ◄─────────────────────────────► │   SpidermanClient.py       │
│  (MultiServer.py)    │                                  │   (client Python)          │
└──────────────────────┘                                  └────────────┬───────────────┘
                                                                       │  WebSocket local (51234)
                                                          ┌────────────▼───────────────┐
                                                          │  dxgi.dll (mod C++)        │
                                                          │  injecté dans le jeu       │
                                                          │  via proxy DXGI            │
                                                          └────────────────────────────┘
```

### Fonctionnement

1. **`dxgi.dll`** est placée dans le dossier du jeu et chargée automatiquement au démarrage (technique du proxy DXGI).
2. La DLL hook les fonctions internes du jeu pour :
   - Détecter les objectifs complétés et envoyer des **checks** au client Python
   - Bloquer les compétences/gadgets non débloqués par Archipelago (`HasSkill` hook)
3. **`SpidermanClient.py`** fait le pont entre la DLL et le serveur Archipelago.

---

## Structure du projet

```
APLG_MARVEL_SPIDERMAN/
├── apworld/
│   └── spiderman/          # APWorld Archipelago (Python)
│       ├── __init__.py     # Monde principal (génération, règles)
│       ├── constants.py    # Constantes partagées (BASE_ID)
│       ├── items.py        # Table des items randomisés
│       ├── locations.py    # Table de tous les emplacements de check
│       ├── options.py      # Options de configuration (YAML seed)
│       └── rules.py        # Règles de logique d'accès
├── client/
│   ├── SpidermanClient.py  # Client Archipelago autonome
│   ├── config.json         # Configuration par défaut
│   └── requirements.txt    # Dépendances Python (aiohttp)
├── game_mod/               # Mod C++ (DLL injectée dans le jeu)
│   ├── src/
│   │   ├── dllmain.cpp     # Point d'entrée DLL + initialisation
│   │   ├── proxy_dxgi.cpp  # Proxy DXGI pour injection automatique
│   │   ├── hooks.cpp       # Hooks MinHook (objectifs, compétences)
│   │   ├── network.cpp     # Client WebSocket IXWebSocket
│   │   └── memory.cpp      # Scan mémoire (pattern scanning)
│   ├── include/
│   │   └── offsets.hpp     # Patterns AOB et constantes de mémoire
│   ├── CMakeLists.txt      # Build CMake
│   └── vcpkg.json          # Dépendances vcpkg
└── docs/                   # Documentation additionnelle
```

---

## Prérequis

### Client Python
- Python 3.10+
- [Archipelago](https://github.com/ArchipelagoMW/Archipelago) installé (pour `MultiServer.py` et le core client)
- `pip install aiohttp`

### Build de la DLL (développeurs)
- Visual Studio 2022 (MSVC C++20)
- [CMake](https://cmake.org/) ≥ 3.20
- [vcpkg](https://github.com/microsoft/vcpkg) avec les packages :
  - `nlohmann-json`
  - `ixwebsocket`
  - `minhook`

---

## Installation

### 1. Installer l'APWorld

```bash
# Compresser le dossier apworld/spiderman/ en .apworld
cd apworld
zip -r spiderman.apworld spiderman/

# Copier dans le dossier worlds d'Archipelago
copy spiderman.apworld <archipelago_dir>\worlds\
```

### 2. Générer une seed

Créez un fichier `spiderman.yaml` :

```yaml
name: VotreNom
game: "Marvel's Spider-Man Remastered"
"Marvel's Spider-Man Remastered":
  goal: defeat_doc_ock
  include_backpacks: true
  include_pigeons: true
  include_taskmaster: true
  include_oscorp_stations: true
  include_bases: true
```

Puis générez :
```bash
python Generate.py --player_files spiderman.yaml
```

### 3. Installer la DLL

```bash
# Copier dxgi.dll dans le dossier du jeu
copy game_mod\build\Release\dxgi.dll "C:\...\Marvel's Spider-Man Remastered\"
```

### 4. Démarrer

Utilisez le script `run_all.ps1` à la racine du projet :
```powershell
.\run_all.ps1
```

Ce script :
1. Trouve automatiquement le dernier fichier `.zip` de seed dans `archipelago_core/output/`
2. Démarre le `MultiServer.py` dans une fenêtre dédiée
3. Démarre le `SpidermanClient.py` dans une seconde fenêtre

Lancez ensuite le jeu. La console de la DLL devrait afficher :  
`[AP-Mod] Connecte au client Python !`

---

## Options de randomisation

| Option | Valeurs | Description |
|--------|---------|-------------|
| `goal` | `defeat_doc_ock` / `all_main_missions` | Condition de victoire |
| `include_backpacks` | `true` / `false` | 55 sacs à dos comme checks |
| `include_pigeons` | `true` / `false` | 12 pigeons d'Howard |
| `include_taskmaster` | `true` / `false` | 16 défis Taskmaster |
| `include_oscorp_stations` | `true` / `false` | 17 stations Oscorp |
| `include_bases` | `true` / `false` | 16 bases ennemies |

---

## Items randomisés

| Catégorie | Exemples |
|-----------|---------|
| Gadgets | Web Shooter, Impact Web, Electric Web, Spider-Drone… |
| Compétences | Web Zip, Air Dash, Perfect Dodge, Point Launch Boost… |
| Déblocages quartiers | Surveillance Decryptors (Financial District, Chinatown…) |
| Suit Powers | Battle Focus, Web Blossom, Holographic Clones… |
| Fillers | Backpack Token, Research Token, Challenge Token… |

---

## Développement — Découverte des hashs d'objectifs

La DLL logue **tous les hashs d'objectifs inconnus** dans la console. Pour mapper un objectif :

1. Lancer le jeu avec la DLL installée
2. Compléter la mission/boss souhaité
3. Copier le hash affiché : `[AP-Mod] Objectif inconnu — hash 0xAABBCCDD`
4. Ajouter dans `game_mod/src/hooks.cpp` dans `OBJECTIVE_HASH_TO_LOCATION` :
   ```cpp
   {0xAABBCCDD, 8901001},  // Boss: Wilson Fisk (Kingpin)
   ```
5. Rebuilder la DLL

---

## Crédits

- [Archipelago](https://archipelago.gg/) — Framework multiworld open source
- [MinHook](https://github.com/TsudaKageyu/minhook) — Library de hooking x64
- [IXWebSocket](https://github.com/machinezone/IXWebSocket) — Client WebSocket C++
- [nlohmann/json](https://github.com/nlohmann/json) — JSON pour C++
