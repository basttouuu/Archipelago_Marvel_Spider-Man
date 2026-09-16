#include "hooks.h"
#include "network.h"
#include "memory.h"
#include <MinHook.h>
#include <iostream>
#include <unordered_map>
#include <unordered_set>
#include <cstdint>

static std::unordered_set<int64_t> s_unlockedItems;

static const std::unordered_map<int64_t, const char*> ITEM_LOOKUP = {
    {8900001, "item_gadget_web_shooter"},
    {8900002, "item_gadget_impact_web"},
    {8900003, "item_gadget_spider_drone"},
    {8900004, "item_gadget_electric_web"},
    {8900005, "item_gadget_web_bomb"},
    {8900007, "item_gadget_concussive_blast"},
    {8900020, "skill_web_zip"},
    {8900021, "skill_point_launch_boost"},
    {8900025, "skill_web_throw"}
};

typedef void(__fastcall* tOnObjectiveCompleted)(void* pContext, uint32_t objectiveHash, int32_t rewardFlags);
static tOnObjectiveCompleted oOnObjectiveCompleted = nullptr;

void __fastcall hkOnObjectiveCompleted(void* pContext, uint32_t objectiveHash, int32_t rewardFlags) {
    std::cout << "[AP-Mod] Objectif complete : Hash = 0x" 
              << std::hex << objectiveHash << std::dec << std::endl;

    int64_t apLocationId = 8901000 + (objectiveHash % 100);
    Network::SendLocationCheck(apLocationId);

    oOnObjectiveCompleted(pContext, objectiveHash, rewardFlags);
}

typedef bool(__fastcall* tHasSkill)(void* pPlayerProfile, uint32_t skillId);
static tHasSkill oHasSkill = nullptr;

bool __fastcall hkHasSkill(void* pPlayerProfile, uint32_t skillId) {
    int64_t apId = 8900000 + skillId;

    if (ITEM_LOOKUP.find(apId) != ITEM_LOOKUP.end()) {
        if (s_unlockedItems.find(apId) == s_unlockedItems.end()) {
            return false;
        }
    }

    if (oHasSkill) {
        return oHasSkill(pPlayerProfile, skillId);
    }
    return true;
}

namespace GameHooks {
    bool Install() {
        if (MH_Initialize() != MH_OK) return false;

        uintptr_t fnObjectiveAddr = Memory::FindPattern(
            "\x48\x89\x5C\x24\x00\x57\x48\x83\xEC\x00\x8B\xFA\x48\x8B\xD9", 
            "xxxx?xxxx?xxxxx"
        );

        if (fnObjectiveAddr) {
            if (MH_CreateHook(reinterpret_cast<void*>(fnObjectiveAddr), 
                              &hkOnObjectiveCompleted, 
                              reinterpret_cast<void**>(&oOnObjectiveCompleted)) == MH_OK) {
                MH_EnableHook(reinterpret_cast<void*>(fnObjectiveAddr));
                std::cout << "[AP-Mod] Hook objectifs pose avec succes a 0x" << std::hex << fnObjectiveAddr << std::dec << std::endl;
            }
        } else {
            std::cout << "[AP-Mod] Mode passif (pattern objectifs non detecte)" << std::endl;
        }

        uintptr_t fnSkillAddr = Memory::FindPattern(
            "\x48\x89\x5C\x24\x00\x48\x89\x74\x24\x00\x57\x48\x83\xEC\x20\x8B\xDA\x48\x8B\xF9",
            "xxxx?xxxx?xxxxxxxxx"
        );

        if (fnSkillAddr) {
            if (MH_CreateHook(reinterpret_cast<void*>(fnSkillAddr),
                              &hkHasSkill,
                              reinterpret_cast<void**>(&oHasSkill)) == MH_OK) {
                MH_EnableHook(reinterpret_cast<void*>(fnSkillAddr));
                std::cout << "[AP-Mod] Hook competences pose avec succes a 0x" << std::hex << fnSkillAddr << std::dec << std::endl;
            }
        } else {
            std::cout << "[AP-Mod] Hook competences en attente de signature dynamique" << std::endl;
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
            std::cout << "[AP-Mod] DEVERROUILLAGE ITEM / COMPETENCE : " << it->second 
                      << " (ID: " << itemId << ")" << std::endl;
        } else {
            std::cout << "[AP-Mod] Token/Filler ID: " << itemId << std::endl;
        }
    }
}
