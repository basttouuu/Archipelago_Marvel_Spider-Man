from BaseClasses import Item, ItemClassification
from typing import Dict, NamedTuple

SPIDERMAN_BASE_ID = 8900000

class SpiderManItemData(NamedTuple):
    code: int
    classification: ItemClassification

class SpiderManItem(Item):
    game: str = "Marvel's Spider-Man Remastered"

ITEM_TABLE: Dict[str, SpiderManItemData] = {
    # Gadgets de base & avancés
    "Web Shooter": SpiderManItemData(SPIDERMAN_BASE_ID + 1, ItemClassification.progression),
    "Impact Web": SpiderManItemData(SPIDERMAN_BASE_ID + 2, ItemClassification.progression),
    "Spider-Drone": SpiderManItemData(SPIDERMAN_BASE_ID + 3, ItemClassification.progression),
    "Electric Web": SpiderManItemData(SPIDERMAN_BASE_ID + 4, ItemClassification.progression),
    "Web Bomb": SpiderManItemData(SPIDERMAN_BASE_ID + 5, ItemClassification.progression),
    "Trip Mine": SpiderManItemData(SPIDERMAN_BASE_ID + 6, ItemClassification.useful),
    "Concussive Blast": SpiderManItemData(SPIDERMAN_BASE_ID + 7, ItemClassification.progression),
    "Suspension Matrix": SpiderManItemData(SPIDERMAN_BASE_ID + 8, ItemClassification.useful),

    # Capacités & Mobilité
    "Skill: Web Zip": SpiderManItemData(SPIDERMAN_BASE_ID + 20, ItemClassification.progression),
    "Skill: Point Launch Boost": SpiderManItemData(SPIDERMAN_BASE_ID + 21, ItemClassification.progression),
    "Skill: Quick Zip": SpiderManItemData(SPIDERMAN_BASE_ID + 22, ItemClassification.progression),
    "Skill: Charge Jump": SpiderManItemData(SPIDERMAN_BASE_ID + 23, ItemClassification.progression),
    "Skill: Air Dash": SpiderManItemData(SPIDERMAN_BASE_ID + 24, ItemClassification.progression),
    "Skill: Web Throw": SpiderManItemData(SPIDERMAN_BASE_ID + 25, ItemClassification.useful),
    "Skill: Perfect Dodge": SpiderManItemData(SPIDERMAN_BASE_ID + 26, ItemClassification.useful),

    # Clés d'accès & Déblocages de Quartiers
    "Surveillance Decryptor - Financial District": SpiderManItemData(SPIDERMAN_BASE_ID + 40, ItemClassification.progression),
    "Surveillance Decryptor - Chinatown": SpiderManItemData(SPIDERMAN_BASE_ID + 41, ItemClassification.progression),
    "Surveillance Decryptor - Greenwich": SpiderManItemData(SPIDERMAN_BASE_ID + 42, ItemClassification.progression),
    "Surveillance Decryptor - Hell's Kitchen": SpiderManItemData(SPIDERMAN_BASE_ID + 43, ItemClassification.progression),
    "Surveillance Decryptor - Midtown": SpiderManItemData(SPIDERMAN_BASE_ID + 44, ItemClassification.progression),
    "Surveillance Decryptor - Upper West Side": SpiderManItemData(SPIDERMAN_BASE_ID + 45, ItemClassification.progression),
    "Surveillance Decryptor - Central Park": SpiderManItemData(SPIDERMAN_BASE_ID + 46, ItemClassification.progression),
    "Surveillance Decryptor - Upper East Side": SpiderManItemData(SPIDERMAN_BASE_ID + 47, ItemClassification.progression),
    "Surveillance Decryptor - Harlem": SpiderManItemData(SPIDERMAN_BASE_ID + 48, ItemClassification.progression),

    # Pouvoirs de Tenue (Suit Powers)
    "Suit Power: Battle Focus": SpiderManItemData(SPIDERMAN_BASE_ID + 60, ItemClassification.useful),
    "Suit Power: Web Blossom": SpiderManItemData(SPIDERMAN_BASE_ID + 61, ItemClassification.useful),
    "Suit Power: Sound of Silence": SpiderManItemData(SPIDERMAN_BASE_ID + 62, ItemClassification.useful),
    "Suit Power: Holographic Clones": SpiderManItemData(SPIDERMAN_BASE_ID + 63, ItemClassification.useful),
    "Suit Power: Defense Shield": SpiderManItemData(SPIDERMAN_BASE_ID + 64, ItemClassification.useful),
    "Suit Power: Equalizer": SpiderManItemData(SPIDERMAN_BASE_ID + 65, ItemClassification.useful),
    "Suit Power: Resupply": SpiderManItemData(SPIDERMAN_BASE_ID + 66, ItemClassification.useful),

    # Jetons (Tokens / Fillers)
    "Backpack Token": SpiderManItemData(SPIDERMAN_BASE_ID + 80, ItemClassification.filler),
    "Landmark Token": SpiderManItemData(SPIDERMAN_BASE_ID + 81, ItemClassification.filler),
    "Research Token": SpiderManItemData(SPIDERMAN_BASE_ID + 82, ItemClassification.filler),
    "Base Token": SpiderManItemData(SPIDERMAN_BASE_ID + 83, ItemClassification.filler),
    "Crime Token": SpiderManItemData(SPIDERMAN_BASE_ID + 84, ItemClassification.filler),
    "Challenge Token": SpiderManItemData(SPIDERMAN_BASE_ID + 85, ItemClassification.filler),
}