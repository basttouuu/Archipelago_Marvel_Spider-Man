from worlds.generic.Rules import set_rule

def set_rules(world, player):
    # Boss Requirements (world.get_location prend uniquement le nom du lieu)
    set_rule(
        world.get_location("Boss: Shocker (Warehouse)"),
        lambda state: state.has("Web Shooter", player) and state.has("Skill: Web Zip", player)
    )

    set_rule(
        world.get_location("Boss: Martin Li (Mister Negative - Office)"),
        lambda state: state.has("Impact Web", player) or state.has("Electric Web", player)
    )

    set_rule(
        world.get_location("Boss: Electro & Vulture"),
        lambda state: state.has("Electric Web", player) and
                      state.has("Skill: Point Launch Boost", player) and
                      state.has("Web Shooter", player)
    )

    set_rule(
        world.get_location("Boss: Rhino & Scorpion"),
        lambda state: (state.has("Concussive Blast", player) or state.has("Web Bomb", player)) and
                      state.has("Skill: Web Throw", player)
    )

    # Condition de Victoire Finale : Doc Ock
    world.multiworld.completion_condition[player] = lambda state: (
        state.can_reach("Boss: Doctor Octopus (Climax)", "Location", player) and
        state.has("Impact Web", player) and
        state.has("Electric Web", player) and
        state.has("Web Bomb", player) and
        state.has("Skill: Point Launch Boost", player) and
        state.has("Skill: Web Zip", player)
    )