#include "hooks.h"
#include "network.h"
#include "memory.h"
#include "../include/offsets.hpp"
#include <MinHook.h>
#include <iostream>
#include <unordered_map>
#include <unordered_set>
#include <cstdint>

// ---------------------------------------------------------------------------
// État global des items débloqués reçus d'Archipelago
// ---------------------------------------------------------------------------
static std::unordered_set<int64_t> s_unlockedItems;

// ---------------------------------------------------------------------------
// ITEM_LOOKUP : mapping complet ID Archipelago → identifiant interne du jeu
// Couvre TOUS les items définis dans items.py (29 entrées)
// ---------------------------------------------------------------------------
static const std::unordered_map<int64_t, const char*> ITEM_LOOKUP = {
    // Gadgets de base & avancés (BASE_ID + 1..8)
    {8900001, "item_gadget_web_shooter"},
    {8900002, "item_gadget_impact_web"},
    {8900003, "item_gadget_spider_drone"},
    {8900004, "item_gadget_electric_web"},
    {8900005, "item_gadget_web_bomb"},
    {8900006, "item_gadget_trip_mine"},
    {8900007, "item_gadget_concussive_blast"},
    {8900008, "item_gadget_suspension_matrix"},

    // Capacités & Mobilité (BASE_ID + 20..26)
    {8900020, "skill_web_zip"},
    {8900021, "skill_point_launch_boost"},
    {8900022, "skill_quick_zip"},
    {8900023, "skill_charge_jump"},
    {8900024, "skill_air_dash"},
    {8900025, "skill_web_throw"},
    {8900026, "skill_perfect_dodge"},

    // Surveillance Decryptors — Quartiers (BASE_ID + 40..48)
    {8900040, "key_surveillance_financial_district"},
    {8900041, "key_surveillance_chinatown"},
    {8900042, "key_surveillance_greenwich"},
    {8900043, "key_surveillance_hells_kitchen"},
    {8900044, "key_surveillance_midtown"},
    {8900045, "key_surveillance_upper_west_side"},
    {8900046, "key_surveillance_central_park"},
    {8900047, "key_surveillance_upper_east_side"},
    {8900048, "key_surveillance_harlem"},

    // Suit Powers (BASE_ID + 60..66)
    {8900060, "suit_power_battle_focus"},
    {8900061, "suit_power_web_blossom"},
    {8900062, "suit_power_sound_of_silence"},
    {8900063, "suit_power_holographic_clones"},
    {8900064, "suit_power_defense_shield"},
    {8900065, "suit_power_equalizer"},
    {8900066, "suit_power_resupply"},

    // Fillers/Tokens (BASE_ID + 80..85) — pas d'effet gameplay direct
    {8900080, "token_backpack"},
    {8900081, "token_landmark"},
    {8900082, "token_research"},
    {8900083, "token_base"},
    {8900084, "token_crime"},
    {8900085, "token_challenge"},
};

// ---------------------------------------------------------------------------
// OBJECTIVE_HASH_TO_LOCATION : mapping hash d'objectif → Location ID AP
//
// Les hashs sont découverts en runtime via les logs "[AP-Mod] Objectif complete".
// Compléter cette table au fur et à mesure des tests en jeu.
// La valeur 0 signifie "non encore mappé" — sera ignorée.
// ---------------------------------------------------------------------------
static const std::unordered_map<uint32_t, int64_t> OBJECTIVE_HASH_TO_LOCATION = {
    // Format : {hash_objectif_jeu, location_id_archipelago}
    // Ex : {0xAABBCCDD, 8901001},  // Boss: Wilson Fisk (Kingpin)
    //
    // TODO : remplir ces valeurs après observation des logs en jeu.
    // Pour l'instant on loggue tous les hashs inconnus pour les découvrir.
};

// ---------------------------------------------------------------------------
// Hooks
// ---------------------------------------------------------------------------

typedef void(__fastcall* tOnObjectiveCompleted)(void* pContext, uint32_t objectiveHash, int32_t rewardFlags);
static tOnObjectiveCompleted oOnObjectiveCompleted = nullptr;

void __fastcall hkOnObjectiveCompleted(void* pContext, uint32_t objectiveHash, int32_t rewardFlags) {
    auto it = OBJECTIVE_HASH_TO_LOCATION.find(objectiveHash);

    if (it != OBJECTIVE_HASH_TO_LOCATION.end()) {
        // Hash connu : envoyer directement le check Archipelago
        if (it->second != 0) {
            Network::SendLocationCheck(it->second);
            std::cout << "[AP-Mod] Check envoye : location " << it->second
                      << " (hash 0x" << std::hex << objectiveHash << std::dec << ")" << std::endl;
        }
    } else {
        // Hash inconnu : loguer pour permettre la découverte des valeurs
        std::cout << "[AP-Mod] Objectif inconnu — hash 0x" << std::hex << objectiveHash
                  << std::dec << " (ajouter dans OBJECTIVE_HASH_TO_LOCATION)" << std::endl;
    }

    // Appel de la fonction originale dans tous les cas
    oOnObjectiveCompleted(pContext, objectiveHash, rewardFlags);
}


typedef bool(__fastcall* tHasSkill)(void* pPlayerProfile, uint32_t skillId);
static tHasSkill oHasSkill = nullptr;

bool __fastcall hkHasSkill(void* pPlayerProfile, uint32_t skillId) {
    // L'ID AP pour une compétence est BASE_ID + skillId interne
    int64_t apId = 8900000 + static_cast<int64_t>(skillId);

    // Si cet AP-ID est dans la lookup et n'a pas été débloqué → bloquer
    if (ITEM_LOOKUP.count(apId) && !s_unlockedItems.count(apId)) {
        return false;
    }

    // Sinon, déléguer au comportement original du jeu
    return oHasSkill ? oHasSkill(pPlayerProfile, skillId) : true;
}


// ---------------------------------------------------------------------------
// Installation / désinstallation / application
// ---------------------------------------------------------------------------

namespace GameHooks {

    bool Install() {
        if (MH_Initialize() != MH_OK) {
            std::cout << "[AP-Mod] Erreur : MH_Initialize() a echoue." << std::endl;
            return false;
        }

        // Hook 1 : OnObjectiveCompleted
        uintptr_t fnObjectiveAddr = Memory::FindPattern(
            Offsets::PATTERN_OBJECTIVE_COMPLETED,
            Offsets::MASK_OBJECTIVE_COMPLETED
        );

        if (fnObjectiveAddr) {
            if (MH_CreateHook(
                    reinterpret_cast<void*>(fnObjectiveAddr),
                    &hkOnObjectiveCompleted,
                    reinterpret_cast<void**>(&oOnObjectiveCompleted)) == MH_OK) {
                MH_EnableHook(reinterpret_cast<void*>(fnObjectiveAddr));
                std::cout << "[AP-Mod] Hook objectifs installe a 0x"
                          << std::hex << fnObjectiveAddr << std::dec << std::endl;
            } else {
                std::cout << "[AP-Mod] Erreur : MH_CreateHook objectifs a echoue." << std::endl;
            }
        } else {
            std::cout << "[AP-Mod] Avertissement : pattern objectifs non trouve (mode passif)." << std::endl;
        }

        // Hook 2 : HasSkill
        uintptr_t fnSkillAddr = Memory::FindPattern(
            Offsets::PATTERN_HAS_SKILL,
            Offsets::MASK_HAS_SKILL
        );

        if (fnSkillAddr) {
            if (MH_CreateHook(
                    reinterpret_cast<void*>(fnSkillAddr),
                    &hkHasSkill,
                    reinterpret_cast<void**>(&oHasSkill)) == MH_OK) {
                MH_EnableHook(reinterpret_cast<void*>(fnSkillAddr));
                std::cout << "[AP-Mod] Hook competences installe a 0x"
                          << std::hex << fnSkillAddr << std::dec << std::endl;
            } else {
                std::cout << "[AP-Mod] Erreur : MH_CreateHook competences a echoue." << std::endl;
            }
        } else {
            std::cout << "[AP-Mod] Avertissement : pattern HasSkill non trouve." << std::endl;
        }

        return true;
    }

    void Uninstall() {
        MH_DisableHook(MH_ALL_HOOKS);
        MH_Uninitialize();
    }

    void ApplyItem(int64_t itemId) {
        s_unlockedItems.insert(itemId);

        auto it = ITEM_LOOKUP.find(itemId);
        if (it != ITEM_LOOKUP.end()) {
            std::cout << "[AP-Mod] Item debloque : " << it->second
                      << " (ID Archipelago: " << itemId << ")" << std::endl;
        } else {
            // ID non dans la lookup = token/filler, pas d'effet gameplay
            std::cout << "[AP-Mod] Filler/Token recu (ID: " << itemId << ") — pas d'effet gameplay." << std::endl;
        }
    }

} // namespace GameHooks
