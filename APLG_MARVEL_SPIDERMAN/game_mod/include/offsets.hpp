#pragma once
// ============================================================================
// offsets.hpp — Signatures de patterns et offsets pour Spider-Man Remastered
// ============================================================================
// Les patterns AOB (Array of Bytes) sont valables pour la version Steam
// (v1.812.1.0 Remastered). À mettre à jour si le jeu est patché.
//
// Format : pattern = suite d'octets, mask = 'x' = octet exact, '?' = wildcard
// ============================================================================

#include <cstdint>
#include <string_view>

namespace Offsets {

    // -------------------------------------------------------------------------
    // OnObjectiveCompleted
    // Appelée par le jeu chaque fois qu'un objectif de mission est validé.
    // Prototype (déduit) : void __fastcall OnObjectiveCompleted(void* ctx, uint32_t hash, int32_t flags)
    // -------------------------------------------------------------------------
    constexpr std::string_view PATTERN_OBJECTIVE_COMPLETED =
        "\x48\x89\x5C\x24\x00\x57\x48\x83\xEC\x00\x8B\xFA\x48\x8B\xD9";
    constexpr std::string_view MASK_OBJECTIVE_COMPLETED =
        "xxxx?xxxx?xxxxx";

    // -------------------------------------------------------------------------
    // HasSkill
    // Appelée pour vérifier si le joueur possède une compétence donnée.
    // Prototype (déduit) : bool __fastcall HasSkill(void* profile, uint32_t skillId)
    // -------------------------------------------------------------------------
    constexpr std::string_view PATTERN_HAS_SKILL =
        "\x48\x89\x5C\x24\x00\x48\x89\x74\x24\x00\x57\x48\x83\xEC\x20\x8B\xDA\x48\x8B\xF9";
    constexpr std::string_view MASK_HAS_SKILL =
        "xxxx?xxxx?xxxxxxxxxx";

    // -------------------------------------------------------------------------
    // Mapping : Hash d'objectif du jeu → Location ID Archipelago
    // -------------------------------------------------------------------------
    // Ces hashs sont les valeurs passées à OnObjectiveCompleted par le jeu.
    // Ils doivent être découverts en runtime via logs de la DLL.
    // Valeurs provisoires — à compléter au fur et à mesure des tests.
    // -------------------------------------------------------------------------
    // Exemple :
    //   static constexpr uint32_t HASH_BOSS_KINGPIN    = 0xAABBCCDD;
    //   static constexpr int64_t  LOC_BOSS_KINGPIN     = 8901001;

} // namespace Offsets
