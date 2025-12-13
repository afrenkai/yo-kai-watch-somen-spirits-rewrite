from typing import Dict, List, Any
import random


class BattleEngine:
    """
    Handles all battle logic, turn processing, damage calculations, etc.
    Based on the original battleCLIENT.js logic but server-side
    """
    
    def __init__(self, team1: List[Dict], team2: List[Dict]):
        self.team1 = team1  # Player 1's team
        self.team2 = team2  # Player 2's team
        self.turn = 0
        self.current_phase = "action_select"  # action_select, resolution, end
        
        self.state = {
            'team1': self._initialize_team(team1),
            'team2': self._initialize_team(team2),
            'turn': 0,
            'log': [],
            'weather': None,
            'field_effects': []
        }
        
        self.pending_actions = {
            'player1': None,
            'player2': None
        }
    
    def _initialize_team(self, team: List[Dict]) -> List[Dict]:
        battle_team = []
        for yokai in team:
            battle_yokai = {
                **yokai,
                'current_hp': yokai['hp'],
                'current_soul': 0,
                'status_effects': [],
                'stat_modifiers': {
                    'str': 0,
                    'spr': 0,
                    'def': 0,
                    'spd': 0
                },
                'is_fainted': False
            }
            battle_team.append(battle_yokai)
        return battle_team
    
    def get_state(self) -> Dict[str, Any]:
        return {
            'team1': self.state['team1'],
            'team2': self.state['team2'],
            'turn': self.state['turn'],
            'phase': self.current_phase,
            'log': self.state['log'][-10:]  # Last 10 log entries
        }
    
    def process_action(self, player_num: int, action: Dict) -> Dict[str, Any]:
        """
        Process a player's action
        action = {
            'type': 'attack' | 'technique' | 'inspirit' | 'soultimate' | 'item' | 'switch',
            'yokai_index': int,
            'target_index': int,
            'move_id': int (if applicable)
        }
        """
        player_key = f'player{player_num}'
        self.pending_actions[player_key] = action
        
        if self.pending_actions['player1'] and self.pending_actions['player2']:
            return self._resolve_turn()
        
        return {
            'status': 'waiting',
            'message': 'Waiting for opponent action'
        }
    
    def _resolve_turn(self) -> Dict[str, Any]:
        self.turn += 1
        self.state['turn'] = self.turn
        
        action1 = self.pending_actions['player1']
        action2 = self.pending_actions['player2']
        
        yokai1 = self.state['team1'][action1['yokai_index']]
        yokai2 = self.state['team2'][action2['yokai_index']]
        
        speed1 = self._calculate_stat(yokai1, 'spd')
        speed2 = self._calculate_stat(yokai2, 'spd')
        
        actions = []
        if speed1 >= speed2:
            actions = [(1, action1, yokai1), (2, action2, yokai2)]
        else:
            actions = [(2, action2, yokai2), (1, action1, yokai1)]
        
        results = []
        
        for player_num, action, yokai in actions:
            if yokai['is_fainted']:
                continue
            
            result = self._execute_action(player_num, action, yokai)
            results.append(result)
            
            self.state['log'].append({
                'turn': self.turn,
                'player': player_num,
                'action': action,
                'result': result
            })
        
        self._update_soul_meters()
        
        self.pending_actions = {'player1': None, 'player2': None}
        
        return {
            'status': 'resolved',
            'turn': self.turn,
            'results': results,
            'state': self.get_state()
        }
    
    def _execute_action(self, player_num: int, action: Dict, attacker: Dict) -> Dict[str, Any]:
        action_type = action['type']
        target_team = self.state['team2'] if player_num == 1 else self.state['team1']
        target = target_team[action['target_index']]
        
        if action_type == 'attack':
            return self._execute_attack(attacker, target, action.get('move_id'))
        elif action_type == 'technique':
            return self._execute_technique(attacker, target, action.get('move_id'))
        elif action_type == 'inspirit':
            return self._execute_inspirit(attacker, target, action.get('move_id'))
        elif action_type == 'soultimate':
            return self._execute_soultimate(attacker, target, action.get('move_id'))
        
        return {'success': False, 'message': 'Unknown action type'}
    
    def _execute_attack(self, attacker: Dict, target: Dict, attack_id: int) -> Dict[str, Any]:
        # TODO: Load attack data from database
        base_power = 40
        
        attack_stat = self._calculate_stat(attacker, 'str')
        defense_stat = self._calculate_stat(target, 'def')
        
        damage = int((base_power * attack_stat / defense_stat) * random.uniform(0.85, 1.0))
        
        target['current_hp'] = max(0, target['current_hp'] - damage)
        
        if target['current_hp'] == 0:
            target['is_fainted'] = True
        
        return {
            'success': True,
            'type': 'attack',
            'damage': damage,
            'target_remaining_hp': target['current_hp'],
            'target_fainted': target['is_fainted']
        }
    
    def _execute_technique(self, attacker: Dict, target: Dict, technique_id: int) -> Dict[str, Any]:
        # TODO: Implement technique logic with element effectiveness
        # TODO: Load technique data from database
        base_power = 60
        
        spirit_stat = self._calculate_stat(attacker, 'spr')
        defense_stat = self._calculate_stat(target, 'def')
        
        damage = int((base_power * spirit_stat / defense_stat) * random.uniform(0.85, 1.0))
        target['current_hp'] = max(0, target['current_hp'] - damage)
        
        if target['current_hp'] == 0:
            target['is_fainted'] = True
        
        return {
            'success': True,
            'type': 'technique',
            'damage': damage,
            'target_remaining_hp': target['current_hp'],
            'target_fainted': target['is_fainted']
        }
    
    def _execute_inspirit(self, attacker: Dict, target: Dict, inspirit_id: int) -> Dict[str, Any]:
        """Execute an inspirit"""
        # TODO: Implement inspirit effects
        return {
            'success': True,
            'type': 'inspirit',
            'effect': 'status_applied'
        }
    
    def _execute_soultimate(self, attacker: Dict, target: Dict, soultimate_id: int) -> Dict[str, Any]:
        if attacker['current_soul'] < 100:
            return {
                'success': False,
                'message': 'Not enough soul energy'
            }
        
        # TODO: Implement soultimate logic
        base_power = 100
        
        spirit_stat = self._calculate_stat(attacker, 'spr')
        defense_stat = self._calculate_stat(target, 'def')
        
        damage = int((base_power * spirit_stat / defense_stat) * 1.5)
        target['current_hp'] = max(0, target['current_hp'] - damage)
        
        attacker['current_soul'] = 0
        
        if target['current_hp'] == 0:
            target['is_fainted'] = True
        
        return {
            'success': True,
            'type': 'soultimate',
            'damage': damage,
            'target_remaining_hp': target['current_hp'],
            'target_fainted': target['is_fainted']
        }
    
    def _calculate_stat(self, yokai: Dict, stat: str) -> int:
        base_stat = yokai.get(f'{stat}_stat', 100)
        modifier = yokai['stat_modifiers'].get(stat, 0)
        
        # Modifier stages: -6 to +6 like in mons, would need to read some of the yogon sheets to make sure this is how this works
        multiplier = max(0.25, min(4.0, 1.0 + (modifier * 0.5)))
        
        return int(base_stat * multiplier)
    
    def _update_soul_meters(self):
        """Update soul meters for all yokai"""
        for team in [self.state['team1'], self.state['team2']]:
            for yokai in team:
                if not yokai['is_fainted']:
                    # Gain soul each turn
                    yokai['current_soul'] = min(100, yokai['current_soul'] + 10)
    
    def is_battle_over(self) -> bool:
        team1_alive = any(not y['is_fainted'] for y in self.state['team1'])
        team2_alive = any(not y['is_fainted'] for y in self.state['team2'])
        
        return not (team1_alive and team2_alive)
    
    def get_winner(self) -> int:
        team1_alive = any(not y['is_fainted'] for y in self.state['team1'])
        team2_alive = any(not y['is_fainted'] for y in self.state['team2'])
        
        if team1_alive and not team2_alive:
            return 1
        elif team2_alive and not team1_alive:
            return 2
        else:
            return 0  # Draw lol
