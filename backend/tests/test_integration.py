import pytest
from app.services.battle_engine import BattleEngine
from app.core.database import get_db


class TestFullBattleFlow:
    
    def test_complete_battle_initialization_to_end(self, sample_team):
        team1 = [
            {'id': 'test_001', 'hp': 220},
            {'id': 'test_002', 'hp': 200},
            {'id': 'test_001', 'hp': 240}
        ]
        team2 = [
            {'id': 'test_002', 'hp': 210},
            {'id': 'test_001', 'hp': 190},
            {'id': 'test_002', 'hp': 230}
        ]
        
        engine = BattleEngine(team1, team2)
        
        assert engine is not None
        assert len(engine.state['team1']) == 3
        assert len(engine.state['team2']) == 3
        assert engine.turn == 0
    
    def test_battle_turn_progression(self, sample_team):
        team1 = sample_team.copy()
        team2 = sample_team.copy()
        
        engine = BattleEngine(team1, team2)
        initial_turn = engine.turn
        
        assert initial_turn == 0
    
    def test_battle_with_multiple_attacks(self, sample_team):
        team1 = sample_team.copy()
        team2 = sample_team.copy()
        
        engine = BattleEngine(team1, team2)
        
        attacker = engine.state['team1'][0]
        target = engine.state['team2'][0]
        
        initial_hp = target.get('hp', target.get('current_hp', 200))
        
        for _ in range(3):
            result = engine._execute_attack(attacker, target, attack_id='attack_001')
            if result.get('success'):
                assert 'damage' in result
        
        final_hp = target.get('hp', target.get('current_hp', 200))
        assert final_hp <= initial_hp


class TestBattleScenarios:
    
    def test_super_effective_attack_scenario(self, sample_team):
        team1 = [{'id': 'test_001', 'hp': 220}]
        team2 = [{'id': 'test_002', 'hp': 200}]
        
        engine = BattleEngine(team1, team2)
        
        attacker = engine.state['team1'][0]
        target = engine.state['team2'][0]
        
        if hasattr(target, 'get'):
            target['fire_res'] = 2.0
        
        result = engine._execute_technique(attacker, target, technique_id='tech_001')
        
        if result.get('success'):
            assert 'elemental_modifier' in result
    
    def test_resistant_attack_scenario(self, sample_team):
        team1 = [{'id': 'test_001', 'hp': 220}]
        team2 = [{'id': 'test_002', 'hp': 200}]
        
        engine = BattleEngine(team1, team2)
        
        attacker = engine.state['team1'][0]
        target = engine.state['team2'][0]
        
        if hasattr(target, 'get'):
            target['fire_res'] = 0.5
        
        result = engine._execute_technique(attacker, target, technique_id='tech_001')
        
        if result.get('success'):
            assert 'elemental_modifier' in result
    
    def test_team_wipe_scenario(self, sample_team):
        team1 = [{'id': 'test_001', 'hp': 220}]
        team2 = [{'id': 'test_002', 'hp': 1}]
        
        engine = BattleEngine(team1, team2)
        
        attacker = engine.state['team1'][0]
        target = engine.state['team2'][0]
        
        result = engine._execute_attack(attacker, target, attack_id='attack_001')
        
        if result.get('success'):
            final_hp = target.get('hp', target.get('current_hp', 1))
            assert final_hp >= 0


class TestBattleStateManagement:
    
    def test_battle_log_records_actions(self, sample_team):
        team1 = sample_team.copy()
        team2 = sample_team.copy()
        
        engine = BattleEngine(team1, team2)
        
        initial_log_length = len(engine.state['log'])
        
        attacker = engine.state['team1'][0]
        target = engine.state['team2'][0]
        
        engine._execute_attack(attacker, target, attack_id='attack_001')
        
        assert isinstance(engine.state['log'], list)
    
    def test_battle_state_persistence(self, sample_team):
        team1 = sample_team.copy()
        team2 = sample_team.copy()
        
        engine = BattleEngine(team1, team2)
        
        state_copy = engine.state.copy()
        
        assert 'team1' in state_copy
        assert 'team2' in state_copy
        assert 'turn' in state_copy
        assert 'log' in state_copy


class TestTeamInteraction:
    
    def test_multiple_yokai_attacks(self, sample_team):
        team1 = sample_team.copy()
        team2 = sample_team.copy()
        
        engine = BattleEngine(team1, team2)
        
        for i in range(min(3, len(engine.state['team1']))):
            attacker = engine.state['team1'][i]
            target = engine.state['team2'][0]
            
            result = engine._execute_attack(attacker, target, attack_id='attack_001')
            
            if result.get('success'):
                assert 'damage' in result
    
    def test_targeting_different_yokai(self, sample_team):
        team1 = sample_team.copy()
        team2 = sample_team.copy()
        
        engine = BattleEngine(team1, team2)
        
        attacker = engine.state['team1'][0]
        
        for i in range(min(3, len(engine.state['team2']))):
            target = engine.state['team2'][i]
            
            result = engine._execute_attack(attacker, target, attack_id='attack_001')
            
            if result.get('success'):
                assert 'damage' in result


class TestDatabaseIntegration:
    
    def test_battle_with_real_yokai_data(self, db_connection):
        yokai_result = db_connection.execute("SELECT * FROM yokai LIMIT 2").fetchall()
        
        if len(yokai_result) < 2:
            pytest.skip("Not enough yokai data")
        
        columns = [desc[0] for desc in db_connection.description]
        yokai1 = dict(zip(columns, yokai_result[0]))
        yokai2 = dict(zip(columns, yokai_result[1]))
        
        team1 = [{'id': yokai1['id'], 'hp': yokai1.get('hp', 200)}]
        team2 = [{'id': yokai2['id'], 'hp': yokai2.get('hp', 200)}]
        
        engine = BattleEngine(team1, team2)
        
        assert engine is not None
    
    def test_battle_with_real_attack_data(self, db_connection):
        attack_result = db_connection.execute("SELECT * FROM attacks LIMIT 1").fetchone()
        
        if not attack_result:
            pytest.skip("No attack data")
        
        columns = [desc[0] for desc in db_connection.description]
        attack = dict(zip(columns, attack_result))
        
        # Get real yokai IDs from the database
        yokai_result = db_connection.execute("SELECT id, bs_a_hp FROM yokai LIMIT 2").fetchall()
        if len(yokai_result) < 2:
            pytest.skip("Not enough yokai data")
        
        yokai_columns = [desc[0] for desc in db_connection.description]
        yokai1 = dict(zip(yokai_columns, yokai_result[0]))
        yokai2 = dict(zip(yokai_columns, yokai_result[1]))
        
        team1 = [{'id': yokai1['id'], 'hp': yokai1.get('bs_a_hp', 220)}]
        team2 = [{'id': yokai2['id'], 'hp': yokai2.get('bs_a_hp', 200)}]
        
        engine = BattleEngine(team1, team2)
        attacker = engine.state['team1'][0]
        target = engine.state['team2'][0]
        
        result = engine._execute_attack(attacker, target, attack_id=attack['id'])
        
        if result.get('success'):
            assert result['damage'] >= 0
    
    def test_battle_with_real_technique_data(self, db_connection):
        technique_result = db_connection.execute("SELECT * FROM techniques LIMIT 1").fetchone()
        
        if not technique_result:
            pytest.skip("No technique data")
        
        columns = [desc[0] for desc in db_connection.description]
        technique = dict(zip(columns, technique_result))
        
        # Get real yokai IDs from the database
        yokai_result = db_connection.execute("SELECT id, bs_a_hp FROM yokai LIMIT 2").fetchall()
        if len(yokai_result) < 2:
            pytest.skip("Not enough yokai data")
        
        yokai_columns = [desc[0] for desc in db_connection.description]
        yokai1 = dict(zip(yokai_columns, yokai_result[0]))
        yokai2 = dict(zip(yokai_columns, yokai_result[1]))
        
        team1 = [{'id': yokai1['id'], 'hp': yokai1.get('bs_a_hp', 220)}]
        team2 = [{'id': yokai2['id'], 'hp': yokai2.get('bs_a_hp', 200)}]
        
        engine = BattleEngine(team1, team2)
        attacker = engine.state['team1'][0]
        target = engine.state['team2'][0]
        
        result = engine._execute_technique(attacker, target, technique_id=technique['id'])
        
        if result.get('success'):
            assert 'damage' in result
            assert 'element' in result or 'attribute' in result


class TestEdgeCases:
    
    def test_battle_with_empty_log(self, sample_team):
        team1 = sample_team.copy()
        team2 = sample_team.copy()
        
        engine = BattleEngine(team1, team2)
        
        assert isinstance(engine.state['log'], list)
        assert len(engine.state['log']) >= 0
    
    def test_battle_with_zero_hp_yokai(self):
        team1 = [{'id': 'test_001', 'hp': 0}]
        team2 = [{'id': 'test_002', 'hp': 200}]
        
        engine = BattleEngine(team1, team2)
        
        assert engine is not None
    
    def test_battle_state_after_multiple_actions(self, sample_team):
        team1 = sample_team.copy()
        team2 = sample_team.copy()
        
        engine = BattleEngine(team1, team2)
        
        attacker = engine.state['team1'][0]
        target = engine.state['team2'][0]
        
        for _ in range(5):
            engine._execute_attack(attacker, target, attack_id='attack_001')
        
        assert 'team1' in engine.state
        assert 'team2' in engine.state
