"""
Options de configuration Archipelago pour Marvel's Spider-Man Remastered.
Ces options apparaissent dans le fichier YAML de génération de seed.
"""

from Options import Choice, Toggle, PerGameCommonOptions
from dataclasses import dataclass


class Goal(Choice):
    """Définit la condition de victoire.

    - defeat_doc_ock : Vaincre le Docteur Octopus (fin de la campagne principale).
    - all_main_missions : Compléter toutes les missions principales.
    """
    display_name = "Objectif de victoire"
    option_defeat_doc_ock = 0
    option_all_main_missions = 1
    default = 0


class IncludeBackpacks(Toggle):
    """Inclure les 55 sacs à dos comme emplacements de check."""
    display_name = "Inclure les sacs à dos"
    default = 1


class IncludePigeons(Toggle):
    """Inclure les 12 pigeons d'Howard comme emplacements de check."""
    display_name = "Inclure les pigeons d'Howard"
    default = 1


class IncludeTaskmaster(Toggle):
    """Inclure les 16 défis Taskmaster comme emplacements de check."""
    display_name = "Inclure les défis Taskmaster"
    default = 1


class IncludeOscorpStations(Toggle):
    """Inclure les 17 stations de recherche Oscorp comme emplacements de check."""
    display_name = "Inclure les stations Oscorp"
    default = 1


class IncludeBases(Toggle):
    """Inclure les 16 bases ennemies comme emplacements de check."""
    display_name = "Inclure les bases ennemies"
    default = 1


@dataclass
class SpiderManOptions(PerGameCommonOptions):
    goal: Goal
    include_backpacks: IncludeBackpacks
    include_pigeons: IncludePigeons
    include_taskmaster: IncludeTaskmaster
    include_oscorp_stations: IncludeOscorpStations
    include_bases: IncludeBases
