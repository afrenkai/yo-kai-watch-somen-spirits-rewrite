"""
Test script to compare Python and JavaScript damage calculation behavior
"""
import json
import random
from damage_calc import get_attack_damage, calculate_hits_to_ko


def test_damage_calculation():
    """Test damage calculation with dummy data matching JS logic"""
    
    # Set seed for reproducible random numbers
    random.seed(42)
    
    # Dummy attacker stats
    attacker_str = 120
    attacker_spr = 85
    
    # Dummy defender stats
    defender_def = 70
    defender_hp = 250
    
    # Dummy defender yokai data with elemental resistances
    defender_data = {
        'name': 'Test Defender',
        'hp': 250,
        'fire_res': 0.5,   # 50% damage from fire (resistant)
        'water_res': 1.0,  # 100% damage from water (neutral)
        'lightning_res': 1.5,  # 150% damage from lightning (weak)
        'earth_res': 1.0,
        'wind_res': 1.0,
        'ice_res': 1.0
    }
    
    # Attitude boosts
    attitude_str_boost = 10
    attitude_spr_boost = 5
    attitude_def_boost = 8
    
    print("=" * 80)
    print("DAMAGE CALCULATION COMPARISON TEST")
    print("=" * 80)
    print("\nAttacker Stats:")
    print(f"  STR: {attacker_str} (+ {attitude_str_boost} attitude) = {attacker_str + attitude_str_boost}")
    print(f"  SPR: {attacker_spr} (+ {attitude_spr_boost} attitude) = {attacker_spr + attitude_spr_boost}")
    print("\nDefender Stats:")
    print(f"  DEF: {defender_def} (+ {attitude_def_boost} attitude) = {defender_def + attitude_def_boost}")
    print(f"  HP: {defender_hp}")
    print("\n" + "=" * 80)
    
    # Test Case 1: Physical Attack (Type 1)
    print("\n[TEST 1] Physical Attack (Type 1)")
    print("-" * 80)
    attack_data_physical = {
        'name': 'Bonk',
        'bp': 50,
        'Lv10_power': 50,
        'hits': 2,
        'N_Hits': 2
    }
    print(f"Attack: {attack_data_physical['name']}")
    print(f"Base Power: {attack_data_physical['bp']}")
    print(f"Hits: {attack_data_physical['hits']}")
    
    # Test normal hit
    random.seed(42)
    result = get_attack_damage(
        attack_data=attack_data_physical,
        attacker_str=attacker_str,
        attacker_spr=attacker_spr,
        defender_data=defender_data,
        defender_def=defender_def,
        defender_hp=defender_hp,
        attack_type=1,
        is_defending=False,
        is_crit=False,
        is_moxie=False,
        attitude_str_boost=attitude_str_boost,
        attitude_spr_boost=attitude_spr_boost,
        attitude_def_boost=attitude_def_boost
    )
    
    print(f"\nNormal Hit:")
    print(f"  Raw Damage: {result['raw_damage']}")
    print(f"  Final Damage: {result['damage']}")
    print(f"  Hits to KO: {result['hits_to_ko']}")
    print(f"  Random Multiplier: {result['multipliers']['random']}")
    print(f"\n  Expected Calculation:")
    print(f"    Attack Stat Used: {result['stats_used']['attack_stat']}")
    print(f"    Power: {result['stats_used']['power']}")
    print(f"    Defence: {result['stats_used']['defence']}")
    print(f"    Formula: ({result['stats_used']['attack_stat']}/2 + {result['stats_used']['power']}/2 - {result['stats_used']['defence']}/4)")
    print(f"    Raw = {result['raw_damage']}")
    print(f"    Final = {result['raw_damage']} * {result['multipliers']['random']} = {result['damage']}")
    
    # Test with defending
    random.seed(42)
    result_defending = get_attack_damage(
        attack_data=attack_data_physical,
        attacker_str=attacker_str,
        attacker_spr=attacker_spr,
        defender_data=defender_data,
        defender_def=defender_def,
        defender_hp=defender_hp,
        attack_type=1,
        is_defending=True,
        attitude_str_boost=attitude_str_boost,
        attitude_spr_boost=attitude_spr_boost,
        attitude_def_boost=attitude_def_boost
    )
    print(f"\nWith Defending:")
    print(f"  Final Damage: {result_defending['damage']} (should be ~50% of normal)")
    print(f"  Defence Multiplier: {result_defending['multipliers']['defence']}")
    
    # Test with crit
    random.seed(42)
    result_crit = get_attack_damage(
        attack_data=attack_data_physical,
        attacker_str=attacker_str,
        attacker_spr=attacker_spr,
        defender_data=defender_data,
        defender_def=defender_def,
        defender_hp=defender_hp,
        attack_type=1,
        is_crit=True,
        attitude_str_boost=attitude_str_boost,
        attitude_spr_boost=attitude_spr_boost,
        attitude_def_boost=attitude_def_boost
    )
    print(f"\nWith Critical Hit:")
    print(f"  Final Damage: {result_crit['damage']}")
    print(f"  Crit Multiplier: {result_crit['multipliers']['crit']}")
    print(f"  Defence Used: {result_crit['stats_used']['defence']} (should be 0)")
    
    # Test Case 2: Technique (Type 2) - Fire Element
    print("\n" + "=" * 80)
    print("\n[TEST 2] Fire Technique (Type 2)")
    print("-" * 80)
    technique_data_fire = {
        'name': 'Blaze',
        'bp': 60,
        'Lv10_power': 60,
        'hits': 1,
        'Element': 'fire',
        'attribute': 'fire'
    }
    print(f"Technique: {technique_data_fire['name']}")
    print(f"Base Power: {technique_data_fire['bp']}")
    print(f"Element: {technique_data_fire['Element']}")
    print(f"Defender Fire Resistance: {defender_data['fire_res']} (50% damage - resistant)")
    
    random.seed(42)
    result_fire = get_attack_damage(
        attack_data=technique_data_fire,
        attacker_str=attacker_str,
        attacker_spr=attacker_spr,
        defender_data=defender_data,
        defender_def=defender_def,
        defender_hp=defender_hp,
        attack_type=2,
        attitude_str_boost=attitude_str_boost,
        attitude_spr_boost=attitude_spr_boost,
        attitude_def_boost=attitude_def_boost
    )
    
    print(f"\nFire Technique vs Resistant Defender:")
    print(f"  Raw Damage: {result_fire['raw_damage']}")
    print(f"  Final Damage: {result_fire['damage']}")
    print(f"  Elemental Modifier: {result_fire['multipliers']['elemental']}")
    print(f"  Attack Stat Used (SPR): {result_fire['stats_used']['attack_stat']}")
    
    # Test Case 3: Technique - Lightning Element (weakness)
    print("\n" + "-" * 80)
    technique_data_lightning = {
        'name': 'Thunder Bolt',
        'bp': 60,
        'Lv10_power': 60,
        'hits': 1,
        'Element': 'lightning',
        'attribute': 'lightning'
    }
    print(f"\nTechnique: {technique_data_lightning['name']}")
    print(f"Element: {technique_data_lightning['Element']}")
    print(f"Defender Lightning Resistance: {defender_data['lightning_res']} (150% damage - weak)")
    
    random.seed(42)
    result_lightning = get_attack_damage(
        attack_data=technique_data_lightning,
        attacker_str=attacker_str,
        attacker_spr=attacker_spr,
        defender_data=defender_data,
        defender_def=defender_def,
        defender_hp=defender_hp,
        attack_type=2,
        attitude_str_boost=attitude_str_boost,
        attitude_spr_boost=attitude_spr_boost,
        attitude_def_boost=attitude_def_boost
    )
    
    print(f"\nLightning Technique vs Weak Defender:")
    print(f"  Raw Damage: {result_lightning['raw_damage']}")
    print(f"  Final Damage: {result_lightning['damage']}")
    print(f"  Elemental Modifier: {result_lightning['multipliers']['elemental']}")
    
    # Test Case 4: Soultimate (Type 3) - Physical
    print("\n" + "=" * 80)
    print("\n[TEST 3] Physical Soultimate (Type 3)")
    print("-" * 80)
    soultimate_data_physical = {
        'name': 'Paws of Fury',
        'bp': 80,
        'Lv10_power': 80,
        'hits': 5,
        'N_Hits': 5,
        'element_type': None
    }
    print(f"Soultimate: {soultimate_data_physical['name']}")
    print(f"Base Power: {soultimate_data_physical['bp']}")
    print(f"Hits: {soultimate_data_physical['hits']}")
    
    random.seed(42)
    result_soul_phys = get_attack_damage(
        attack_data=soultimate_data_physical,
        attacker_str=attacker_str,
        attacker_spr=attacker_spr,
        defender_data=defender_data,
        defender_def=defender_def,
        defender_hp=defender_hp,
        attack_type=3,
        is_moxie=False,
        attitude_str_boost=attitude_str_boost,
        attitude_spr_boost=attitude_spr_boost,
        attitude_def_boost=attitude_def_boost
    )
    
    print(f"\nNormal (No Moxie):")
    print(f"  Raw Damage: {result_soul_phys['raw_damage']}")
    print(f"  Final Damage: {result_soul_phys['damage']}")
    print(f"  Attack Stat Used (STR): {result_soul_phys['stats_used']['attack_stat']}")
    
    random.seed(42)
    result_soul_moxie = get_attack_damage(
        attack_data=soultimate_data_physical,
        attacker_str=attacker_str,
        attacker_spr=attacker_spr,
        defender_data=defender_data,
        defender_def=defender_def,
        defender_hp=defender_hp,
        attack_type=3,
        is_moxie=True,
        attitude_str_boost=attitude_str_boost,
        attitude_spr_boost=attitude_spr_boost,
        attitude_def_boost=attitude_def_boost
    )
    
    print(f"\nWith Moxie:")
    print(f"  Final Damage: {result_soul_moxie['damage']} (should be 2x normal)")
    print(f"  Moxie Multiplier: {result_soul_moxie['multipliers']['moxie']}")
    
    # Test Case 5: Soultimate (Type 3) - Elemental (uses SPR)
    print("\n" + "-" * 80)
    soultimate_data_elemental = {
        'name': 'Inferno',
        'bp': 80,
        'Lv10_power': 80,
        'hits': 3,
        'N_Hits': 3,
        'element_type': 'fire',
        'Element': 'fire'
    }
    print(f"\nSoultimate: {soultimate_data_elemental['name']}")
    print(f"Element: {soultimate_data_elemental['element_type']}")
    print(f"Defender Fire Resistance: {defender_data['fire_res']}")
    
    random.seed(42)
    result_soul_elem = get_attack_damage(
        attack_data=soultimate_data_elemental,
        attacker_str=attacker_str,
        attacker_spr=attacker_spr,
        defender_data=defender_data,
        defender_def=defender_def,
        defender_hp=defender_hp,
        attack_type=3,
        is_moxie=False,
        attitude_str_boost=attitude_str_boost,
        attitude_spr_boost=attitude_spr_boost,
        attitude_def_boost=attitude_def_boost
    )
    
    print(f"\nElemental Soultimate (Fire):")
    print(f"  Raw Damage: {result_soul_elem['raw_damage']}")
    print(f"  Final Damage: {result_soul_elem['damage']}")
    print(f"  Attack Stat Used (SPR): {result_soul_elem['stats_used']['attack_stat']}")
    print(f"  Elemental Modifier: {result_soul_elem['multipliers']['elemental']}")
    
    # Test Case 6: Edge case - Low damage
    print("\n" + "=" * 80)
    print("\n[TEST 4] Edge Case - Minimum Damage")
    print("-" * 80)
    weak_attack = {
        'name': 'Weak Bonk',
        'bp': 5,
        'Lv10_power': 5,
        'hits': 1,
        'N_Hits': 1
    }
    
    random.seed(42)
    result_weak = get_attack_damage(
        attack_data=weak_attack,
        attacker_str=30,  # Very low STR
        attacker_spr=20,
        defender_data=defender_data,
        defender_def=80,  # High DEF
        defender_hp=defender_hp,
        attack_type=1,
        attitude_str_boost=0,
        attitude_spr_boost=0,
        attitude_def_boost=0
    )
    
    print(f"Weak Attack (STR=30, Power=5) vs High Defense (DEF=80):")
    print(f"  Raw Damage: {result_weak['raw_damage']} (should be minimum 1)")
    print(f"  Final Damage: {result_weak['damage']}")
    
    print("\n" + "=" * 80)
    print("\nJavaScript Equivalent Calculations:")
    print("=" * 80)
    print("""
For comparison, the JavaScript formulas are:

1. Physical Attack (Type 1):
   - ChosenAttackStat = AttackerSTR + Attitude.STR_Boost
   - RawDamage = (ChosenAttackStat/2 + Power/2 - Defence/4)
   - Damage = RawDamage * RandMulti * DefenceMulti

2. Technique (Type 2):
   - ChosenAttackStat = AttackerSPR + Attitude.SPR_Boost
   - ElementalResistance = yokaiData[Element]
   - RawDamage = (ChosenAttackStat/2 + Power/2 - Defence/4)
   - Damage = RawDamage * RandMulti * DefenceMulti * ElementalResistance

3. Soultimate (Type 3):
   - If has element: ChosenAttackStat = AttackerSPR + Attitude.SPR_Boost
   - Else: ChosenAttackStat = AttackerSTR + Attitude.STR_Boost
   - RawDamage = (ChosenAttackStat/2 + Power/2 - Defence/4)
   - Damage = RawDamage * RandMulti * DefenceMulti * ElementalResistance * Crit * MoxieMulti

Where:
   - DefenceMulti = 0.5 if defending, else 1.0
   - Crit = 1.25 if critical, else 1.0 (also sets Defence = 0)
   - MoxieMulti = 2.0 if Moxie active on Soultimate, else 1.0
   - RandMulti = random float between 0.9 and 1.1
   - If RawDamage < 1, then RawDamage = 1
    """)
    
    print("\n" + "=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)
    print("\nTo verify against JavaScript:")
    print("1. Use the same random seed/multiplier values")
    print("2. Compare raw damage calculations first")
    print("3. Then compare final damage with all multipliers")
    print("4. The formulas should match exactly")


if __name__ == "__main__":
    test_damage_calculation()
