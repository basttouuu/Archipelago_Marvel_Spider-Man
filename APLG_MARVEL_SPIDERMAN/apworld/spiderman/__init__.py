from worlds.AutoWorld import World, WebWorld
from BaseClasses import Region, ItemClassification
from .items import ITEM_TABLE, SpiderManItem
from .locations import LOCATION_TABLE, SpiderManLocation
from .rules import set_rules

class SpiderManWeb(WebWorld):
    theme = "ice"

class SpiderManWorld(World):
    """
    Marvel's Spider-Man Remastered Archipelago implementation.
    """
    game: str = "Marvel's Spider-Man Remastered"
    web = SpiderManWeb()

    item_name_to_id = {name: data.code for name, data in ITEM_TABLE.items()}
    location_name_to_id = LOCATION_TABLE

    def create_item(self, name: str) -> SpiderManItem:
        data = ITEM_TABLE[name]
        return SpiderManItem(name, data.classification, data.code, self.player)

    def create_regions(self):
        menu = Region("Menu", self.player, self.multiworld)
        manhattan = Region("Manhattan", self.player, self.multiworld)

        for loc_name, loc_id in LOCATION_TABLE.items():
            manhattan.locations.append(SpiderManLocation(self.player, loc_name, loc_id, manhattan))

        menu.connect(manhattan)
        self.multiworld.regions += [menu, manhattan]

    def create_items(self):
        pool = []
        total_locations = len(LOCATION_TABLE)

        # 1. Progression & Utiles
        for name, data in ITEM_TABLE.items():
            if data.classification in (ItemClassification.progression, ItemClassification.useful):
                pool.append(self.create_item(name))

        # 2. Tokens / Fillers pour combler exactement le nombre d'emplacements
        fillers = [
            "Backpack Token", "Landmark Token", "Research Token",
            "Base Token", "Crime Token", "Challenge Token"
        ]
        idx = 0
        while len(pool) < total_locations:
            pool.append(self.create_item(fillers[idx % len(fillers)]))
            idx += 1

        self.multiworld.itempool += pool

    def set_rules(self):
        set_rules(self, self.player)