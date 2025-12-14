import pytest
from damage_calc import (
    get_random_multiplier,
    calculate_stats,
    get_attack_damage,
    calculate_hits_to_ko
)


class TestRandomMultiplier:
    
    def test_random_multiplier_range(self):
        for _ in range(100):
            multiplier = get_random_multiplier()
            assert 0.9 <= multiplier <= 1.1
    
    def test_random_multiplier_type(self):
        multiplier = get_random_multiplier()
        assert isinstance(multiplier, float)
    
    def test_random_multiplier_precision(self):
        multiplier = get_random_multiplier()
        assert round(multiplier, 2) == multiplier


class TestCalculateStats:
    
    def test_calculate_stats_base_values(self):
        yokai_data = {
            'hp': 100,
            'str': 50,
            'spr': 40,
            'def': 45,
            'spd': 55
        }
        hp, str_stat, spr, def_stat, spd = calculate_stats(
            yokai_data, 0, 0, 0, 0, 0, 50, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        )
        assert hp == 100
        assert str_stat == 50
        assert spr == 40
        assert def_stat == 45
        assert spd == 55
    
    def test_calculate_stats_with_ivs(self):
        yokai_data = {
            'hp': 100,
            'str': 50,
            'spr': 40,
            'def': 45,
            'spd': 55
        }
        hp, str_stat, spr, def_stat, spd = calculate_stats(
            yokai_data, 10, 5, 5, 5, 5, 50, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        )
        assert hp == 110
        assert str_stat == 55
        assert spr == 45
    
    def test_calculate_stats_with_gym(self):
        yokai_data = {
            'hp': 100,
            'str': 50,
            'spr': 40,
            'def': 45,
            'spd': 55
        }
        hp, str_stat, spr, def_stat, spd = calculate_stats(
            yokai_data, 0, 0, 0, 0, 0, 50, 20, 10, 10, 10, 10, 0, 0, 0, 0, 0
        )
        assert hp == 120
        assert str_stat == 60
        assert spr == 50
    
    def test_calculate_stats_with_attitude_boost(self):
        yokai_data = {
            'hp': 100,
            'str': 50,
            'spr': 40,
            'def': 45,
            'spd': 55
        }
        hp, str_stat, spr, def_stat, spd = calculate_stats(
            yokai_data, 0, 0, 0, 0, 0, 50, 0, 0, 0, 0, 0, 5, 15, -10, 5, 0
        )
        assert hp == 105
        assert str_stat == 65
        assert spr == 30
    
    def test_calculate_stats_all_bonuses(self):
        yokai_data = {
            'hp': 100,
            'str': 50,
            'spr': 40,
            'def': 45,
            'spd': 55
        }
        hp, str_stat, spr, def_stat, spd = calculate_stats(
            yokai_data, 10, 5, 5, 5, 5, 50, 20, 10, 10, 10, 10, 5, 15, -10, 5, 0
        )
        assert hp == 135
        assert str_stat == 80
        assert spr == 45


class TestGetAttackDamage:
    
    def test_physical_attack_basic_damage(self):
        attack_data = {'bp': 60, 'hits': 1}
        defender_data = {'fire_res': 1.0, 'water_res': 1.0, 'lightning_res': 1.0}
        
        result = get_attack_damage(
            attack_data,
            attacker_str=80,
            attacker_spr=75,
            defender_data=defender_data,
            defender_def=70,
            defender_hp=220,
            attack_type=1
        )
        
        assert 'damage' in result
        assert 'hits_to_ko' in result
        assert result['damage'] > 0
    
    def test_technique_damage_with_attribute(self):
        technique_data = {'bp': 80, 'attribute': 'fire'}
        defender_data = {'fire_res': 1.0, 'water_res': 1.0, 'lightning_res': 1.0}
        
        result = get_attack_damage(
            technique_data,
            attacker_str=80,
            attacker_spr=90,
            defender_data=defender_data,
            defender_def=70,
            defender_hp=220,
            attack_type=2
        )
        
        assert result['damage'] > 0
    
    def test_soultimate_damage(self):
        soultimate_data = {'bp': 120, 'attribute': 'fire'}
        defender_data = {'fire_res': 1.0, 'water_res': 1.0, 'lightning_res': 1.0}
        
        result = get_attack_damage(
            soultimate_data,
            attacker_str=80,
            attacker_spr=100,
            defender_data=defender_data,
            defender_def=70,
            defender_hp=220,
            attack_type=3
        )
        
        assert result['damage'] > 0
    
    def test_critical_hit_multiplier(self):
        attack_data = {'bp': 60, 'hits': 1}
        defender_data = {'fire_res': 1.0, 'water_res': 1.0, 'lightning_res': 1.0}
        
        normal_result = get_attack_damage(
            attack_data,
            attacker_str=80,
            attacker_spr=75,
            defender_data=defender_data,
            defender_def=70,
            defender_hp=220,
            attack_type=1,
            is_crit=False
        )
        
        crit_result = get_attack_damage(
            attack_data,
            attacker_str=80,
            attacker_spr=75,
            defender_data=defender_data,
            defender_def=70,
            defender_hp=220,
            attack_type=1,
            is_crit=True
        )
        
        assert crit_result['damage'] > normal_result['damage']
    
    def test_defending_reduces_damage(self):
        attack_data = {'bp': 60, 'hits': 1}
        defender_data = {'fire_res': 1.0, 'water_res': 1.0, 'lightning_res': 1.0}
        
        normal_result = get_attack_damage(
            attack_data,
            attacker_str=80,
            attacker_spr=75,
            defender_data=defender_data,
            defender_def=70,
            defender_hp=220,
            attack_type=1,
            is_defending=False
        )
        
        defending_result = get_attack_damage(
            attack_data,
            attacker_str=80,
            attacker_spr=75,
            defender_data=defender_data,
            defender_def=70,
            defender_hp=220,
            attack_type=1,
            is_defending=True
        )
        
        assert defending_result['damage'] < normal_result['damage']
    
    def test_elemental_weakness_increases_damage(self):
        technique_data = {'bp': 80, 'attribute': 'fire'}
        neutral_defender = {'fire_res': 1.0, 'water_res': 1.0, 'lightning_res': 1.0}
        weak_defender = {'fire_res': 2.0, 'water_res': 1.0, 'lightning_res': 1.0}
        
        neutral_result = get_attack_damage(
            technique_data,
            attacker_str=80,
            attacker_spr=90,
            defender_data=neutral_defender,
            defender_def=70,
            defender_hp=220,
            attack_type=2
        )
        
        weak_result = get_attack_damage(
            technique_data,
            attacker_str=80,
            attacker_spr=90,
            defender_data=weak_defender,
            defender_def=70,
            defender_hp=220,
            attack_type=2
        )
        
        assert weak_result['damage'] > neutral_result['damage']
    
    def test_elemental_resistance_reduces_damage(self):
        technique_data = {'bp': 80, 'attribute': 'fire'}
        neutral_defender = {'fire_res': 1.0, 'water_res': 1.0, 'lightning_res': 1.0}
        resistant_defender = {'fire_res': 0.5, 'water_res': 1.0, 'lightning_res': 1.0}
        
        neutral_result = get_attack_damage(
            technique_data,
            attacker_str=80,
            attacker_spr=90,
            defender_data=neutral_defender,
            defender_def=70,
            defender_hp=220,
            attack_type=2
        )
        
        resistant_result = get_attack_damage(
            technique_data,
            attacker_str=80,
            attacker_spr=90,
            defender_data=resistant_defender,
            defender_def=70,
            defender_hp=220,
            attack_type=2
        )
        
        assert resistant_result['damage'] < neutral_result['damage']
    
    def test_multi_hit_attack(self):
        attack_data = {'bp': 40, 'hits': 3, 'N_Hits': 3}
        defender_data = {'fire_res': 1.0, 'water_res': 1.0, 'lightning_res': 1.0}
        
        result = get_attack_damage(
            attack_data,
            attacker_str=80,
            attacker_spr=75,
            defender_data=defender_data,
            defender_def=70,
            defender_hp=220,
            attack_type=1
        )
        
        assert result['damage'] > 0
    
    def test_attitude_bonuses_affect_damage(self):
        attack_data = {'bp': 60, 'hits': 1}
        defender_data = {'fire_res': 1.0, 'water_res': 1.0, 'lightning_res': 1.0}
        
        normal_result = get_attack_damage(
            attack_data,
            attacker_str=80,
            attacker_spr=75,
            defender_data=defender_data,
            defender_def=70,
            defender_hp=220,
            attack_type=1,
            attitude_str_boost=0
        )
        
        boosted_result = get_attack_damage(
            attack_data,
            attacker_str=80,
            attacker_spr=75,
            defender_data=defender_data,
            defender_def=70,
            defender_hp=220,
            attack_type=1,
            attitude_str_boost=20
        )
        
        assert boosted_result['damage'] > normal_result['damage']


class TestCalculateHitsToKO:
    
    def test_hits_to_ko_calculation(self):
        result = calculate_hits_to_ko(50, 220)
        assert result > 0
        assert isinstance(result, int)
    
    def test_hits_to_ko_high_damage(self):
        result = calculate_hits_to_ko(200, 220)
        assert result <= 2
    
    def test_hits_to_ko_low_damage(self):
        result = calculate_hits_to_ko(10, 220)
        assert result >= 20
    
    def test_hits_to_ko_exact_ko(self):
        result = calculate_hits_to_ko(220, 220)
        assert result == 1
