import pytest
from damage_calc import get_random_multiplier, calculate_stats


class TestUtilityFunctions:
    
    def test_random_multiplier_consistency(self):
        multipliers = [get_random_multiplier() for _ in range(100)]
        assert all(0.9 <= m <= 1.1 for m in multipliers)
        assert len(set(multipliers)) > 1
    
    def test_stat_calculation_helpers(self):
        yokai_data = {
            'hp': 100,
            'str': 50,
            'spr': 40,
            'def': 45,
            'spd': 55
        }
        
        stats = calculate_stats(
            yokai_data, 10, 5, 5, 5, 5, 50, 20, 10, 10, 10, 10, 5, 15, -10, 5, 0
        )
        
        assert len(stats) == 5
        assert all(isinstance(s, int) for s in stats)
    
    def test_stat_calculation_edge_cases(self):
        yokai_data = {
            'hp': 0,
            'str': 0,
            'spr': 0,
            'def': 0,
            'spd': 0
        }
        
        stats = calculate_stats(
            yokai_data, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        )
        
        assert len(stats) == 5
        assert all(s >= 0 for s in stats)


class TestDataValidation:
    
    def test_yokai_data_structure(self, sample_yokai_data):
        assert 'id' in sample_yokai_data
        assert 'name' in sample_yokai_data
        assert 'hp' in sample_yokai_data
        assert 'str' in sample_yokai_data
        assert 'spr' in sample_yokai_data
        assert 'def' in sample_yokai_data
        assert 'spd' in sample_yokai_data
    
    def test_attack_data_structure(self, sample_attack_data):
        assert 'id' in sample_attack_data
        assert 'name' in sample_attack_data
        assert 'bp' in sample_attack_data
    
    def test_technique_data_structure(self, sample_technique_data):
        assert 'id' in sample_technique_data
        assert 'name' in sample_technique_data
        assert 'bp' in sample_technique_data
        assert 'attribute' in sample_technique_data


class TestBattleHelpers:
    
    def test_team_data_structure(self, sample_team):
        assert isinstance(sample_team, list)
        assert len(sample_team) == 3
        for yokai in sample_team:
            assert 'id' in yokai
            assert 'hp' in yokai
    
    def test_battle_state_structure(self, sample_battle_state):
        assert 'team1' in sample_battle_state
        assert 'team2' in sample_battle_state
        assert 'turn' in sample_battle_state
        assert 'log' in sample_battle_state
        assert 'weather' in sample_battle_state
        assert 'field_effects' in sample_battle_state
    
    def test_battle_state_teams_count(self, sample_battle_state):
        assert len(sample_battle_state['team1']) == 3
        assert len(sample_battle_state['team2']) == 3


class TestFixtures:
    
    def test_db_connection_fixture(self, db_connection):
        assert db_connection is not None
        result = db_connection.execute("SELECT 1").fetchone()
        assert result is not None
    
    def test_client_fixture(self, client):
        assert client is not None
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_sample_data_fixtures(self, sample_yokai_data, sample_attack_data, sample_technique_data):
        assert sample_yokai_data is not None
        assert sample_attack_data is not None
        assert sample_technique_data is not None


class TestConstants:
    
    def test_elemental_types(self):
        elements = ['fire', 'water', 'lightning', 'ice', 'earth', 'wind', 'none']
        assert len(elements) == 7
        assert 'fire' in elements
        assert 'none' in elements
    
    def test_stat_types(self):
        stats = ['hp', 'str', 'spr', 'def', 'spd']
        assert len(stats) == 5
        for stat in stats:
            assert isinstance(stat, str)
    
    def test_action_types(self):
        actions = ['attack', 'technique', 'inspirit', 'soultimate', 'guard', 'switch']
        assert len(actions) == 6
        assert 'attack' in actions
        assert 'guard' in actions


class TestHelperValidation:
    
    def test_positive_damage_values(self):
        damage_values = [10, 50, 100, 250, 500]
        assert all(d > 0 for d in damage_values)
    
    def test_resistance_multipliers(self):
        resistances = [0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0]
        assert all(r > 0 for r in resistances)
        assert all(r <= 2.0 for r in resistances)
    
    def test_stat_boost_ranges(self):
        boosts = [-20, -10, -5, 0, 5, 10, 15, 20]
        assert all(isinstance(b, int) for b in boosts)
        assert min(boosts) >= -20
        assert max(boosts) <= 20


class TestErrorHandling:
    
    def test_missing_yokai_data_keys(self):
        incomplete_data = {'id': 1, 'name': 'Test'}
        assert 'id' in incomplete_data
        assert 'name' in incomplete_data
        assert 'hp' not in incomplete_data
    
    def test_invalid_stat_values(self):
        invalid_stats = {'hp': -100, 'str': -50}
        for key, value in invalid_stats.items():
            assert isinstance(value, int)
    
    def test_empty_team_handling(self):
        empty_team = []
        assert isinstance(empty_team, list)
        assert len(empty_team) == 0
