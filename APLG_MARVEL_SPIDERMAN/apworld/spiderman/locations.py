from BaseClasses import Location
from typing import Dict

SPIDERMAN_BASE_ID = 8900000

class SpiderManLocation(Location):
    game: str = "Marvel's Spider-Man Remastered"

LOCATION_TABLE: Dict[str, int] = {}

def _register(category_id: int, entries: list):
    for i, name in enumerate(entries):
        LOCATION_TABLE[name] = SPIDERMAN_BASE_ID + category_id + i

# 1. Quêtes Principales & Boss (1000+)
_register(1000, [
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
    "Side Boss: Taskmaster Defeated"
])

# 2. Sacs à dos - 55 emplacements (2000+)
_backpacks = [
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
    "Backpack: Harlem - Old Cellphone"
]
_register(2000, _backpacks)

# 3. Stations de Recherche Oscorp - 17 emplacements (3000+)
_register(3000, [
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
    "Oscorp Station: Central Park - Pigeon Vaccine"
])

# 4. Bases Ennemies - 16 emplacements (4000+)
_register(4000, [
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
    "Base: Prisoner Camp - Harlem"
])

# 5. Pigeons d'Howard - 12 emplacements (5000+)
_register(5000, [f"Howard's Pigeon #{i+1}" for i in range(12)])

# 6. Défis Taskmaster - 16 emplacements (6000+)
_register(6000, [
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
    "Taskmaster Challenge: Harlem - Stealth"
])