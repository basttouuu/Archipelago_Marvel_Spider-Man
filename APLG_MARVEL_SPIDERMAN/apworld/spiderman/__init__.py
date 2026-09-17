from worlds.AutoWorld import World, WebWorld
from BaseClasses import Region, ItemClassification
from .constants import GAME_NAME
from .items import ITEM_TABLE, SpiderManItem
from .locations import (
    SpiderManLocation,
    LOCATION_TABLE,
    MAIN_MISSIONS_TABLE,
    BACKPACKS_TABLE,
    OSCORP_STATIONS_TABLE,
    BASES_TABLE,
    PIGEONS_TABLE,
    TASKMASTER_TABLE,
)
from .options import SpiderManOptions
from .rules import set_rules


class SpiderManWeb(WebWorld):
    theme = "ice"
    tutorials = []


class SpiderManWorld(World):
    """
    Marvel's Spider-Man Remastered — Archipelago Randomizer.

    Jouez Spider-Man en recevant des gadgets, compétences et déblocages
    de quartier via le multiworld Archipelago. Chaque sac à dos collecté,
    boss vaincu ou base nettoyée peut être un check dans la pool partagée !
    """

    game: str = GAME_NAME
    web = SpiderManWeb()
    topology_present = True

    options_dataclass = SpiderManOptions
    options: SpiderManOptions  # type: ignore[assignment]

    # La table complète est toujours enregistrée pour que le serveur connaisse
    # tous les IDs possibles, même si certains ne sont pas générés selon les options.
    item_name_to_id = {name: data.code for name, data in ITEM_TABLE.items()}
    location_name_to_id = LOCATION_TABLE

    def _get_active_locations(self) -> dict:
        """Retourne la table des locations actives selon les options du joueur."""
        active: dict = dict(MAIN_MISSIONS_TABLE)

        if self.options.include_backpacks:
            active.update(BACKPACKS_TABLE)
        if self.options.include_oscorp_stations:
            active.update(OSCORP_STATIONS_TABLE)
        if self.options.include_bases:
            active.update(BASES_TABLE)
        if self.options.include_pigeons:
            active.update(PIGEONS_TABLE)
        if self.options.include_taskmaster:
            active.update(TASKMASTER_TABLE)

        return active

    def create_item(self, name: str) -> SpiderManItem:
        data = ITEM_TABLE[name]
        return SpiderManItem(name, data.classification, data.code, self.player)

    def create_regions(self):
        menu = Region("Menu", self.player, self.multiworld)
        manhattan = Region("Manhattan", self.player, self.multiworld)

        active_locations = self._get_active_locations()
        for loc_name, loc_id in active_locations.items():
            manhattan.locations.append(
                SpiderManLocation(self.player, loc_name, loc_id, manhattan)
            )

        menu.connect(manhattan)
        self.multiworld.regions += [menu, manhattan]

    def create_items(self):
        pool = []
        active_locations = self._get_active_locations()
        total_locations = len(active_locations)

        # 1. Ajouter les items de progression et utiles
        for name, data in ITEM_TABLE.items():
            if data.classification in (ItemClassification.progression, ItemClassification.useful):
                pool.append(self.create_item(name))

        # 2. Compléter avec des fillers jusqu'à atteindre le nombre de locations
        fillers = [
            "Backpack Token", "Landmark Token", "Research Token",
            "Base Token", "Crime Token", "Challenge Token",
        ]
        idx = 0
        while len(pool) < total_locations:
            pool.append(self.create_item(fillers[idx % len(fillers)]))
            idx += 1

        # 3. Si trop d'items prog/useful, tronquer proprement
        # (ne devrait pas arriver avec les valeurs actuelles, mais sécurité)
        self.multiworld.itempool += pool[:total_locations]

    def set_rules(self):
        set_rules(self, self.player)