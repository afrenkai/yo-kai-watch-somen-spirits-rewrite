import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.battle_engine import BattleEngine
from app.core.database import get_db


def test_damage_calculations():    
    print("BATTLE DAMAGE CALCULATION TEST")
    
    with get_db() as db:
        yokai_result = db.execute("SELECT * FROM yokai LIMIT 2").fetchall()
        if not yokai_result:
            print("ERROR: No yokai found in database!")
            return
        
        columns = [desc[0] for desc in db.description]
        yokai1 = dict(zip(columns, yokai_result[0]))
        yokai2 = dict(zip(columns, yokai_result[1]))
    
    print(f"\nAttacker: {yokai1['name']}")
    print(f"  HP: {yokai1['bs_b_hp']}")
    print(f"  STR: {yokai1['bs_b_str']}")
    print(f"  SPR: {yokai1['bs_b_spr']}")
    print(f"  DEF: {yokai1['bs_b_def']}")
    print(f"  SPD: {yokai1['bs_b_spd']}")
    
    print(f"\nDefender: {yokai2['name']}")
    print(f"  HP: {yokai2['bs_b_hp']}")
    print(f"  STR: {yokai2['bs_b_str']}")
    print(f"  SPR: {yokai2['bs_b_spr']}")
    print(f"  DEF: {yokai2['bs_b_def']}")
    print(f"  SPD: {yokai2['bs_b_spd']}")
    
    team1 = [yokai1]
    team2 = [yokai2]
    
    engine = BattleEngine(team1, team2)

    print("BATTLE INITIALIZED")

    
    state = engine.get_state()
    print(f"\nTeam 1 HP: {state['team1'][0]['current_hp']}/{state['team1'][0]['max_hp']}")
    print(f"Team 2 HP: {state['team2'][0]['current_hp']}/{state['team2'][0]['max_hp']}")
    

    print("TEST 1: Physical Attack")

    if yokai1.get('attack_id'):
        action1 = {
            'type': 'attack',
            'yokai_index': 0,
            'target_index': 0,
            'move_id': yokai1['attack_id']
        }
        
        action2 = {
            'type': 'attack',
            'yokai_index': 0,
            'target_index': 0,
            'move_id': yokai2.get('attack_id', yokai1['attack_id'])
        }
        
        print(f"\n{yokai1['name']} attacks {yokai2['name']}!")
        
        engine.process_action(1, action1)
        result = engine.process_action(2, action2)
        
        if result['status'] == 'resolved':
            for r in result['results']:
                if r['success']:
                    print(f"\nAttack: {r['attack_name']}")
                    print(f"  Damage: {r['damage']}")
                    print(f"  Hits: {r['hits']}")
                    print(f"  Critical: {r.get('is_crit', False)}")
                    if 'damage_breakdown' in r:
                        breakdown = r['damage_breakdown']
                        print(f"  Multipliers:")
                        for mult_name, mult_val in breakdown['multipliers'].items():
                            print(f"    {mult_name}: {mult_val:.2f}")
                    print(f"  Target HP: {r['target_remaining_hp']}")
    else:
        print("Yokai 1 has no attack_id, skipping attack test. THIS IS BAD")
  
    print("TEST 2: Technique")

    
    if yokai1.get('technique_id'):
        action1 = {
            'type': 'technique',
            'yokai_index': 0,
            'target_index': 0,
            'move_id': yokai1['technique_id']
        }
        
        action2 = {
            'type': 'attack',
            'yokai_index': 0,
            'target_index': 0,
            'move_id': yokai2.get('attack_id', yokai1.get('attack_id'))
        }
        
        print(f"\n{yokai1['name']} uses technique on {yokai2['name']}!")
        
        engine.process_action(1, action1)
        result = engine.process_action(2, action2)
        
        if result['status'] == 'resolved':
            for r in result['results']:
                if r['success'] and r['type'] == 'technique':
                    print(f"\n Technique: {r['technique_name']}")
                    print(f"  Damage: {r['damage']}")
                    print(f"  Element: {r.get('element', 'None')}")
                    print(f"  Critical: {r.get('is_crit', False)}")
                    print(f"  Elemental Modifier: {r.get('elemental_modifier', 1.0):.2f}")
                    if 'damage_breakdown' in r:
                        breakdown = r['damage_breakdown']
                        print(f"  Multipliers:")
                        for mult_name, mult_val in breakdown['multipliers'].items():
                            print(f"    {mult_name}: {mult_val:.2f}")
                    print(f"  Target HP: {r['target_remaining_hp']}")
    else:
        print("Yokai 1 has no technique_id, skipping technique test")
    

    print("FINAL STATE")
    
    final_state = engine.get_state()
    print(f"\nTeam 1 HP: {final_state['team1'][0]['current_hp']}/{final_state['team1'][0]['max_hp']}")
    print(f"Team 2 HP: {final_state['team2'][0]['current_hp']}/{final_state['team2'][0]['max_hp']}")
    
    print("\n All damage calculation tests completed!")


if __name__ == "__main__":
    test_damage_calculations()
