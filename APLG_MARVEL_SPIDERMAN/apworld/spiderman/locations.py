from BaseClasses import Location
from typing import Dict
from .constants import SPIDERMAN_BASE_ID, GAME_NAME


class SpiderManLocation(Location):
    game: str = GAME_NAME


# Plages réservées par catégorie : {category_id: max_entries_autorisées}
# La plage d'une catégorie est [BASE_ID + category_id, BASE_ID + category_id + max_entries - 1]
# La prochaine catégorie commence à category_id + 1000 → max 999 entrées par défaut.
_CATEGORY_MAX_ENTRIES: Dict[int, int] = {
    1000: 999,   # Missions principales & Boss
    2000: 999,   # Sacs à dos
    3000: 999,   # Stations Oscorp
    4000: 999,   # Bases ennemies
    5000: 999,   # Pigeons d'Howard
    6000: 999,   # Défis Taskmaster
}


def _build_table(category_id: int, entries: list) -> Dict[str, int]:
    """Construit une sous-table {nom: id} pour une catégorie donnée.

    Vérifie au moment de la construction que la catégorie ne dépasse pas
    sa plage allouée (définie dans _CATEGORY_MAX_ENTRIES).
    """
    max_entries = _CATEGORY_MAX_ENTRIES.get(category_id, 999)
    if len(entries) > max_entries:
        raise ValueError(
            f"[locations.py] Catégorie {category_id} : {len(entries)} entrées dépassent "
            f"la limite de {max_entries}. Risque de collision avec la catégorie suivante !"
        )
    return {name: SPIDERMAN_BASE_ID + category_id + i for i, name in enumerate(entries)}


# ---------------------------------------------------------------------------
# 1. Quêtes Principales & Boss (catégorie 1000)
# ---------------------------------------------------------------------------
MAIN_MISSIONS_TABLE: Dict[str, int] = _build_table(1000, [
    "Mission: Clearing the Way (Fisk Tower)",
    "Boss: Wilson Fisk (Kingpin)",
    "Mission: My OTHER Other Job",
    "Mission: Keeping the Peace",
    "Mission: Something Old, Something New",
    "Mission: Fisk Hideout Intro",
    "Mission: Landmarking",
    "Mission: For She's a Jolly Good Fellow",
    "Mission: Don't Touch the Art",
    "Mission: A Shocking Comeback",
    "Boss: Shocker (Warehouse)",
    "Mission: The Mask",
    "Mission: A Day to Remember",
    "Mission: Back to School",
    "Mission: Spider-Hack",
    "Mission: Uninvited Guests",
    "Mission: Strong Connections",
    "Mission: First Day",
    "Mission: Collision Course",
    "Mission: The One That Got Away",
    "Mission: Breakthrough",
    "Mission: Reflection",
    "Mission: Wheels within Wheels",
    "Mission: Straw, Meet Camel",
    "Mission: And the Award Goes To...",
    "Mission: Dual Purpose",
    "Mission: Hidden Agenda",
    "Boss: Martin Li (Mister Negative - Office)",
    "Mission: A Fresh Start",
    "Mission: Dinner Target",
    "Mission: Step Into My Parlor",
    "Mission: The Pitch",
    "Mission: Out of the Frying Pan...",
    "Mission: Into the Fire...",
    "Boss: Electro & Vulture",
    "Mission: Picking Up the Trail",
    "Boss: Rhino & Scorpion",
    "Mission: Heavy Swing",
    "Mission: Step into the Parlor...",
    "Mission: Heart of the Matter",
    "Boss: Mister Negative (Subway/Dimension)",
    "Mission: Pax in Bello",
    "Boss: Doctor Octopus (Climax)",
    "Side Boss: Tombstone",
    "Side Boss: Taskmaster Defeated",
])

# ---------------------------------------------------------------------------
# 2. Sacs à dos - 55 emplacements (catégorie 2000)
# ---------------------------------------------------------------------------
BACKPACKS_TABLE: Dict[str, int] = _build_table(2000, [
    # Financial District (5)
    "Backpack: Financial District - Wheat Penny",
    "Backpack: Financial District - Classic Web Shooter",
    "Backpack: Financial District - Spider-Signal",
    "Backpack: Financial District - Electrician Gloves",
    "Backpack: Financial District - Self-Defense Spray",
    # Chinatown (5)
    "Backpack: Chinatown - First Responder",
    "Backpack: Chinatown - Nightclub VIP Card",
    "Backpack: Chinatown - Drawing from a Kid",
    "Backpack: Chinatown - Broken Glasses",
    "Backpack: Chinatown - Biohazard Container",
    # Greenwich (6)
    "Backpack: Greenwich - Pizza Delivery Cap",
    "Backpack: Greenwich - Arm Webbing",
    "Backpack: Greenwich - Good Luck Charm",
    "Backpack: Greenwich - Promo Comic",
    "Backpack: Greenwich - Web Shooter Prototype",
    "Backpack: Greenwich - Small Figurine",
    # Hell's Kitchen (7)
    "Backpack: Hell's Kitchen - Old Glasses",
    "Backpack: Hell's Kitchen - Cracked Phone",
    "Backpack: Hell's Kitchen - Damaged Drone",
    "Backpack: Hell's Kitchen - Book",
    "Backpack: Hell's Kitchen - Daredevil Card",
    "Backpack: Hell's Kitchen - Flash Drive",
    "Backpack: Hell's Kitchen - Vial of Blood",
    # Midtown (11)
    "Backpack: Midtown - Knuckle Duster",
    "Backpack: Midtown - Spider-Tracer",
    "Backpack: Midtown - Rhino Fragment",
    "Backpack: Midtown - Shocker Fragment",
    "Backpack: Midtown - Science Trophy",
    "Backpack: Midtown - Rent Bill",
    "Backpack: Midtown - College Application",
    "Backpack: Midtown - Ticket Stub",
    "Backpack: Midtown - Apartment Key",
    "Backpack: Midtown - Press Pass",
    "Backpack: Midtown - Yuri Contact",
    # Upper West Side (5)
    "Backpack: Upper West Side - Bottle of Cologne",
    "Backpack: Upper West Side - Keychain",
    "Backpack: Upper West Side - Concussion Grenade Spec",
    "Backpack: Upper West Side - ESU ID Card",
    "Backpack: Upper West Side - Mini Cassette",
    # Central Park (4)
    "Backpack: Central Park - Portable Game Console",
    "Backpack: Central Park - Wrestling Flyer",
    "Backpack: Central Park - Locket",
    "Backpack: Central Park - Marshmallow Box",
    # Upper East Side (5)
    "Backpack: Upper East Side - Magnet",
    "Backpack: Upper East Side - Old Camera",
    "Backpack: Upper East Side - Sandy Jar",
    "Backpack: Upper East Side - Blank Badge",
    "Backpack: Upper East Side - Broken Syringe",
    # Harlem (7)
    "Backpack: Harlem - Spider-Signal Prototype",
    "Backpack: Harlem - Comic Book",
    "Backpack: Harlem - Spidey Button",
    "Backpack: Harlem - Broken Mask",
    "Backpack: Harlem - Track Trophy",
    "Backpack: Harlem - High School Diploma",
    "Backpack: Harlem - Old Cellphone",
])

# ---------------------------------------------------------------------------
# 3. Stations de Recherche Oscorp - 17 emplacements (catégorie 3000)
# ---------------------------------------------------------------------------
OSCORP_STATIONS_TABLE: Dict[str, int] = _build_table(3000, [
    "Oscorp Station: Chinatown - Bacteria Alert",
    "Oscorp Station: Chinatown - Under Pressure",
    "Oscorp Station: Greenwich - Chemical Leak",
    "Oscorp Station: Greenwich - Hidden Agenda",
    "Oscorp Station: Financial - Data On the Move",
    "Oscorp Station: Financial - Cell Tower Tracking",
    "Oscorp Station: Hell's Kitchen - Vaccine Hunt",
    "Oscorp Station: Hell's Kitchen - Port of Entry",
    "Oscorp Station: Midtown - Smog Alert",
    "Oscorp Station: Midtown - Rooftop Gondola",
    "Oscorp Station: Upper West Side - Dialing Up",
    "Oscorp Station: Upper West Side - Spider-Bot",
    "Oscorp Station: Upper East Side - Dive In",
    "Oscorp Station: Upper East Side - Sonic Wave",
    "Oscorp Station: Harlem - Ventilate",
    "Oscorp Station: Harlem - Viscometer",
    "Oscorp Station: Central Park - Pigeon Vaccine",
])

# ---------------------------------------------------------------------------
# 4. Bases Ennemies - 16 emplacements (catégorie 4000)
# ---------------------------------------------------------------------------
BASES_TABLE: Dict[str, int] = _build_table(4000, [
    # Fisk Hideouts
    "Base: Fisk Hideout - Financial District",
    "Base: Fisk Hideout - Greenwich",
    "Base: Fisk Hideout - Upper West Side",
    "Base: Fisk Hideout - Upper East Side",
    # Demon Warehouses
    "Base: Demon Warehouse - Chinatown",
    "Base: Demon Warehouse - Hell's Kitchen",
    "Base: Demon Warehouse - Upper East Side",
    "Base: Demon Warehouse - Harlem",
    # Sable Outposts
    "Base: Sable Outpost - Central Park",
    "Base: Sable Outpost - Midtown",
    "Base: Sable Outpost - Upper West Side",
    "Base: Sable Outpost - Financial District",
    # Prisoner Camps
    "Base: Prisoner Camp - Hell's Kitchen",
    "Base: Prisoner Camp - Chinatown",
    "Base: Prisoner Camp - Upper East Side",
    "Base: Prisoner Camp - Harlem",
])

# ---------------------------------------------------------------------------
# 5. Pigeons d'Howard - 12 emplacements (catégorie 5000)
# ---------------------------------------------------------------------------
PIGEONS_TABLE: Dict[str, int] = _build_table(5000, [
    f"Howard's Pigeon #{i + 1}" for i in range(12)
])

# ---------------------------------------------------------------------------
# 6. Défis Taskmaster - 16 emplacements (catégorie 6000)
# ---------------------------------------------------------------------------
TASKMASTER_TABLE: Dict[str, int] = _build_table(6000, [
    "Taskmaster Challenge: Midtown - Combat",
    "Taskmaster Challenge: Midtown - Stealth",
    "Taskmaster Challenge: Hell's Kitchen - Drone",
    "Taskmaster Challenge: Hell's Kitchen - Bomb",
    "Taskmaster Challenge: Financial - Drone",
    "Taskmaster Challenge: Financial - Bomb",
    "Taskmaster Challenge: Chinatown - Combat",
    "Taskmaster Challenge: Greenwich - Stealth",
    "Taskmaster Challenge: Central Park - Drone",
    "Taskmaster Challenge: Central Park - Bomb",
    "Taskmaster Challenge: Upper West Side - Stealth",
    "Taskmaster Challenge: Upper West Side - Combat",
    "Taskmaster Challenge: Upper East Side - Drone",
    "Taskmaster Challenge: Upper East Side - Bomb",
    "Taskmaster Challenge: Harlem - Combat",
    "Taskmaster Challenge: Harlem - Stealth",
])

# ---------------------------------------------------------------------------
# Table complète (toujours toutes les locations pour location_name_to_id)
# ---------------------------------------------------------------------------
LOCATION_TABLE: Dict[str, int] = {
    **MAIN_MISSIONS_TABLE,
    **BACKPACKS_TABLE,
    **OSCORP_STATIONS_TABLE,
    **BASES_TABLE,
    **PIGEONS_TABLE,
    **TASKMASTER_TABLE,
}


def _validate_location_tables() -> None:
    """Valide l'intégrité de toutes les tables de locations au chargement du module.

    Détecte :
    - Les noms de locations en double (même nom dans deux catégories différentes)
    - Les IDs numériques en collision (deux locations avec le même ID)

    Appelée une seule fois à l'import. Lève une AssertionError si un problème
    est trouvé, afin de catcher les erreurs dès le développement.
    """
    all_tables = {
        "MAIN_MISSIONS": MAIN_MISSIONS_TABLE,
        "BACKPACKS":     BACKPACKS_TABLE,
        "OSCORP":        OSCORP_STATIONS_TABLE,
        "BASES":         BASES_TABLE,
        "PIGEONS":       PIGEONS_TABLE,
        "TASKMASTER":    TASKMASTER_TABLE,
    }

    seen_names: Dict[str, str] = {}   # nom → nom_de_table
    seen_ids: Dict[int, str] = {}     # id  → nom_de_table
    errors: list = []

    for table_name, table in all_tables.items():
        for loc_name, loc_id in table.items():
            if loc_name in seen_names:
                errors.append(
                    f"  Nom en double : '{loc_name}' dans '{table_name}' ET '{seen_names[loc_name]}'"
                )
            else:
                seen_names[loc_name] = table_name

            if loc_id in seen_ids:
                errors.append(
                    f"  ID en collision : {loc_id} utilisé par '{loc_name}' ({table_name})"
                    f" ET par '{seen_ids[loc_id]}'"
                )
            else:
                seen_ids[loc_id] = loc_name

    if errors:
        raise AssertionError(
            "[locations.py] Problèmes d'intégrité détectés dans les tables de locations :\n"
            + "\n".join(errors)
        )


# Validation exécutée une seule fois à l'import du module
_validate_location_tables()