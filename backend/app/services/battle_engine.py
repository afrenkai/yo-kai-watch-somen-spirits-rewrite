from typing import Dict, List, Any, Optional
import random
import math
from app.core.database import get_db
from damage_calc import (
    get_attack_damage,
    get_random_multiplier,
    calculate_stats,
    calculate_hits_to_ko
)


class BattleEngine:
    """
    Handles all battle logic, turn processing, damage calculations, etc.
    Based on the original battleCLIENT.js logic but server-side
    """
    
    def __init__(self, team1: List[Dict], team2: List[Dict]):
        self.team1 = team1
        self.team2 = team2
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
    
    def _get_attack_data(self, attack_id: int) -> Optional[Dict[str, Any]]:
        with get_db() as db:
            result = db.execute(
                "SELECT * FROM attacks WHERE id = ?",
                [attack_id]
            ).fetchone()
            
            if result:
                columns = [desc[0] for desc in db.description]
                return dict(zip(columns, result))
            return None
    
    def _get_technique_data(self, technique_id: int) -> Optional[Dict[str, Any]]:
        with get_db() as db:
            result = db.execute(
                "SELECT * FROM techniques WHERE id = ?",
                [technique_id]
            ).fetchone()
            
            if result:
                columns = [desc[0] for desc in db.description]
                return dict(zip(columns, result))
            return None
    
    def _get_inspirit_data(self, inspirit_id: int) -> Optional[Dict[str, Any]]:
        with get_db() as db:
            result = db.execute(
                "SELECT * FROM inspirit WHERE id = ?",
                [inspirit_id]
            ).fetchone()
            
            if result:
                columns = [desc[0] for desc in db.description]
                return dict(zip(columns, result))
            return None
    
    def _get_soultimate_data(self, soultimate_id: int) -> Optional[Dict[str, Any]]:
        with get_db() as db:
            result = db.execute(
                "SELECT * FROM soultimate WHERE id = ?",
                [soultimate_id]
            ).fetchone()
            
            if result:
                columns = [desc[0] for desc in db.description]
                return dict(zip(columns, result))
            return None
    
    def _get_yokai_data(self, yokai_id: int) -> Optional[Dict[str, Any]]:
        with get_db() as db:
            # Try to fetch by id first, then by code if id doesn't work, artifact from mixed schemas that needs to be fixed
            # TODO: revisit
            result = db.execute(
                "SELECT * FROM yokai WHERE id = ?",
                [yokai_id]
            ).fetchone()
            
            if result:
                columns = [desc[0] for desc in db.description]
                return dict(zip(columns, result))
            return None
    
    def _calculate_elemental_modifier(self, attacker_attribute: str, target: Dict) -> float:
        if not attacker_attribute or attacker_attribute == 'none':
            return 1.0
        
        resistance_map = {
            'fire': 'fire_res',
            'water': 'water_res',
            'lightning': 'lightning_res',
            'earth': 'earth_res',
            'wind': 'wind_res',
            'ice': 'ice_res'
        }
        
        res_key = resistance_map.get(attacker_attribute.lower())
        if res_key and res_key in target:
            return target[res_key]
        
        return 1.0
    
    def _initialize_team(self, team: List[Dict]) -> List[Dict]:
        battle_team = []
        for yokai in team:
            if 'id' in yokai or len(yokai) < 5:
                full_yokai_data = self._get_yokai_data(yokai['id'])
                if full_yokai_data:
                    yokai = full_yokai_data
            
            # Get IVs, gym stats (EVs), and attitude boosts from yokai data or defaults
            hp_iv = yokai.get('hp_iv', 0)
            str_iv = yokai.get('str_iv', 0)
            spr_iv = yokai.get('spr_iv', 0)
            def_iv = yokai.get('def_iv', 0)
            spd_iv = yokai.get('spd_iv', 0)
            
            hp_gym = yokai.get('hp_gym', 0)
            str_gym = yokai.get('str_gym', 0)
            spr_gym = yokai.get('spr_gym', 0)
            def_gym = yokai.get('def_gym', 0)
            spd_gym = yokai.get('spd_gym', 0)
            
            hp_boost = yokai.get('attitude_hp_boost', 0)
            str_boost = yokai.get('attitude_str_boost', 0)
            spr_boost = yokai.get('attitude_spr_boost', 0)
            def_boost = yokai.get('attitude_def_boost', 0)
            spd_boost = yokai.get('attitude_spd_boost', 0)
            
            level = yokai.get('level', 50)  # Default level 50
            
            # Calculate final stats using damage_calc module
            # Note: This requires yokai_data to have base stats
            # For now, use the stats directly if they exist, otherwise calculate
            if 'bs_b_hp' in yokai:  # Using Battle Stats B (max level stats)
                final_hp = yokai['bs_b_hp'] + hp_iv + hp_gym + hp_boost
                final_str = yokai['bs_b_str'] + str_iv + str_gym + str_boost
                final_spr = yokai['bs_b_spr'] + spr_iv + spr_gym + spr_boost
                final_def = yokai['bs_b_def'] + def_iv + def_gym + def_boost
                final_spd = yokai['bs_b_spd'] + spd_iv + spd_gym + spd_boost
            else:
                # Fallback to default stats
                final_hp = yokai.get('hp', 100)
                final_str = yokai.get('str', 50)
                final_spr = yokai.get('spr', 50)
                final_def = yokai.get('def', 50)
                final_spd = yokai.get('spd', 50)
            
            battle_yokai = {
                **yokai,
                'max_hp': final_hp,
                'current_hp': final_hp,
                'str_stat': final_str,
                'spr_stat': final_spr,
                'def_stat': final_def,
                'spd_stat': final_spd,
                'current_soul': 0,
                'status_effects': [],
                'stat_modifiers': {
                    'str': 0,
                    'spr': 0,
                    'def': 0,
                    'spd': 0
                },
                'is_fainted': False,
                'attitude_str_boost': str_boost,
                'attitude_spr_boost': spr_boost,
                'attitude_def_boost': def_boost,
                'attitude_spd_boost': spd_boost
            }
            battle_team.append(battle_yokai)
        return battle_team
    
    def get_state(self) -> Dict[str, Any]:
        return {
            'team1': self.state['team1'],
            'team2': self.state['team2'],
            'turn': self.state['turn'],
            'phase': self.current_phase,
            'log': self.state['log'][-10:]
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
        attack_data = self._get_attack_data(attack_id)
        
        if not attack_data:
            return {
                'success': False,
                'message': f'Attack {attack_id} not found in database'
            }
        
        # Get attacker stats
        attacker_str = self._calculate_stat(attacker, 'str')
        attacker_spr = self._calculate_stat(attacker, 'spr')
        
        # Get defender stats
        defender_def = self._calculate_stat(target, 'def')
        defender_hp = target['current_hp']
        
        # Check if defending
        is_defending = 'guarding' in target.get('status_effects', [])
        
        # Check for critical hit (5% chance)
        is_crit = random.random() < 0.05
        
        # Get attitude bonuses (default to 0 if not present)
        attitude_str_boost = attacker.get('attitude_str_boost', 0)
        attitude_spr_boost = attacker.get('attitude_spr_boost', 0)
        attitude_def_boost = target.get('attitude_def_boost', 0)
        
        # Calculate damage using damage_calc module
        damage_result = get_attack_damage(
            attack_data=attack_data,
            attacker_str=attacker_str,
            attacker_spr=attacker_spr,
            defender_data=target,
            defender_def=defender_def,
            defender_hp=defender_hp,
            attack_type=1,  # 1 = Physical Attack
            is_defending=is_defending,
            is_crit=is_crit,
            is_moxie=False,
            attitude_str_boost=attitude_str_boost,
            attitude_spr_boost=attitude_spr_boost,
            attitude_def_boost=attitude_def_boost
        )
        
        total_damage = damage_result['damage']
        hits = damage_result['stats_used']['hit_amount']
        
        # Apply damage to target
        target['current_hp'] = max(0, target['current_hp'] - total_damage)
        
        if target['current_hp'] == 0:
            target['is_fainted'] = True
        
        return {
            'success': True,
            'type': 'attack',
            'attack_name': attack_data.get('command', 'Unknown Attack'),
            'damage': total_damage,
            'hits': hits,
            'is_crit': is_crit,
            'damage_breakdown': damage_result,
            'target_remaining_hp': target['current_hp'],
            'target_fainted': target['is_fainted']
        }
    
    def _execute_technique(self, attacker: Dict, target: Dict, technique_id: int) -> Dict[str, Any]:
        """Execute a technique using the damage calc logic"""
        technique_data = self._get_technique_data(technique_id)
        
        if not technique_data:
            return {
                'success': False,
                'message': f'Technique {technique_id} not found in database'
            }
        
        # Get attacker stats
        attacker_str = self._calculate_stat(attacker, 'str')
        attacker_spr = self._calculate_stat(attacker, 'spr')
        
        # Get defender stats
        defender_def = self._calculate_stat(target, 'def')
        defender_hp = target['current_hp']
        
        # Check if defending
        is_defending = 'guarding' in target.get('status_effects', [])
        
        # Check for critical hit (5% chance)
        is_crit = random.random() < 0.05
        
        # Get attitude bonuses
        attitude_str_boost = attacker.get('attitude_str_boost', 0)
        attitude_spr_boost = attacker.get('attitude_spr_boost', 0)
        attitude_def_boost = target.get('attitude_def_boost', 0)
        
        # Calculate damage using damage_calc module
        damage_result = get_attack_damage(
            attack_data=technique_data,
            attacker_str=attacker_str,
            attacker_spr=attacker_spr,
            defender_data=target,
            defender_def=defender_def,
            defender_hp=defender_hp,
            attack_type=2,  # 2 = Technique
            is_defending=is_defending,
            is_crit=is_crit,
            is_moxie=False,
            attitude_str_boost=attitude_str_boost,
            attitude_spr_boost=attitude_spr_boost,
            attitude_def_boost=attitude_def_boost
        )
        
        total_damage = damage_result['damage']
        
        # Apply damage to target
        target['current_hp'] = max(0, target['current_hp'] - total_damage)
        
        if target['current_hp'] == 0:
            target['is_fainted'] = True
        
        return {
            'success': True,
            'type': 'technique',
            'technique_name': technique_data.get('command', 'Unknown Technique'),
            'damage': total_damage,
            'is_crit': is_crit,
            'element': technique_data.get('element'),
            'elemental_modifier': damage_result['multipliers']['elemental'],
            'damage_breakdown': damage_result,
            'target_remaining_hp': target['current_hp'],
            'target_fainted': target['is_fainted']
        }
    
    def _execute_inspirit(self, attacker: Dict, target: Dict, inspirit_id: int) -> Dict[str, Any]:
        """Execute an inspirit using data from database"""
        # Get inspirit data from database
        inspirit_data = self._get_inspirit_data(inspirit_id)
        
        if not inspirit_data:
            return {
                'success': False,
                'message': f'Inspirit {inspirit_id} not found in database'
            }
        
        effect_type = inspirit_data['effect_type']
        tags = inspirit_data['tags']
        
        # Parse tags to determine the specific effect
        # Tags could be like: "STR-", "DEF+", "confusion", "drain", etc.
        effects_applied = []
        
        # Handle stat modification inspirits
        stat_modifiers = {
            'STR-': ('str', -1),
            'STR+': ('str', 1),
            'strUp': ('str', 1),
            'strDown': ('str', -1),
            'DEF-': ('def', -1),
            'DEF+': ('def', 1),
            'defUp': ('def', 1),
            'defDown': ('def', -1),
            'SPR-': ('spr', -1),
            'SPR+': ('spr', 1),
            'sprUp': ('spr', 1),
            'sprDown': ('spr', -1),
            'SPD-': ('spd', -1),
            'SPD+': ('spd', 1),
            'spdUp': ('spd', 1),
            'spdDown': ('spd', -1),
        }
        
        # Handle allUp and allDown special tags
        if 'allUp' in tags:
            for stat in ['str', 'spr', 'def', 'spd']:
                target['stat_modifiers'][stat] += 1
                target['stat_modifiers'][stat] = max(-6, min(6, target['stat_modifiers'][stat]))
            effects_applied.append('all stats increased')
        elif 'allDown' in tags:
            for stat in ['str', 'spr', 'def', 'spd']:
                target['stat_modifiers'][stat] -= 1
                target['stat_modifiers'][stat] = max(-6, min(6, target['stat_modifiers'][stat]))
            effects_applied.append('all stats decreased')
        else:
            # Handle individual stat modifications
            for tag_key, (stat, modifier) in stat_modifiers.items():
                if tag_key in tags:
                    target['stat_modifiers'][stat] += modifier
                    # Clamp stat modifiers between -6 and +6
                    target['stat_modifiers'][stat] = max(-6, min(6, target['stat_modifiers'][stat]))
                    effects_applied.append(f'{stat} {"increased" if modifier > 0 else "decreased"}')
        
        # Handle status effect inspirits
        if 'confusion' in tags.lower():
            target['status_effects'].append({
                'type': 'confusion',
                'duration': 3,
                'turns_remaining': 3
            })
            effects_applied.append('confusion')
        
        if 'drain' in tags.lower():
            # Drain effect - could restore HP to attacker
            drain_amount = int(target['hp'] * 0.1)  # 10% of max HP
            target['current_hp'] = max(0, target['current_hp'] - drain_amount)
            attacker['current_hp'] = min(attacker['hp'], attacker['current_hp'] + drain_amount)
            effects_applied.append(f'drained {drain_amount} HP')
        
        if 'seal' in tags.lower():
            target['status_effects'].append({
                'type': 'seal',
                'duration': 2,
                'turns_remaining': 2
            })
            effects_applied.append('sealed')
        
        return {
            'success': True,
            'type': 'inspirit',
            'inspirit_name': inspirit_data['name'],
            'effect_type': effect_type,
            'effects_applied': effects_applied,
            'target_remaining_hp': target['current_hp']
        }
    
    def _execute_soultimate(self, attacker: Dict, target: Dict, soultimate_id: int) -> Dict[str, Any]:
        """Execute a soultimate using the damage calc logic"""
        if attacker['current_soul'] < 100:
            return {
                'success': False,
                'message': 'Not enough soul energy'
            }
        
        soultimate_data = self._get_soultimate_data(soultimate_id)
        
        if not soultimate_data:
            return {
                'success': False,
                'message': f'Soultimate {soultimate_id} not found in database'
            }
        
        # Get attacker stats
        attacker_str = self._calculate_stat(attacker, 'str')
        attacker_spr = self._calculate_stat(attacker, 'spr')
        
        # Get defender stats
        defender_def = self._calculate_stat(target, 'def')
        defender_hp = target['current_hp']
        
        # Check if defending
        is_defending = 'guarding' in target.get('status_effects', [])
        
        # Check for critical hit (5% chance)
        is_crit = random.random() < 0.05
        
        # Check for Moxie skill (doubles Soultimate damage)
        is_moxie = attacker.get('skill_name', '').lower() == 'moxie'
        
        # Get attitude bonuses
        attitude_str_boost = attacker.get('attitude_str_boost', 0)
        attitude_spr_boost = attacker.get('attitude_spr_boost', 0)
        attitude_def_boost = target.get('attitude_def_boost', 0)
        
        # Calculate damage using damage_calc module
        damage_result = get_attack_damage(
            attack_data=soultimate_data,
            attacker_str=attacker_str,
            attacker_spr=attacker_spr,
            defender_data=target,
            defender_def=defender_def,
            defender_hp=defender_hp,
            attack_type=3,  # 3 = Soultimate
            is_defending=is_defending,
            is_crit=is_crit,
            is_moxie=is_moxie,
            attitude_str_boost=attitude_str_boost,
            attitude_spr_boost=attitude_spr_boost,
            attitude_def_boost=attitude_def_boost
        )
        
        total_damage = damage_result['damage']
        hits = damage_result['stats_used']['hit_amount']
        
        # Apply damage to target
        target['current_hp'] = max(0, target['current_hp'] - total_damage)
        
        # Reset soul meter after using soultimate
        attacker['current_soul'] = 0
        
        if target['current_hp'] == 0:
            target['is_fainted'] = True
        
        result = {
            'success': True,
            'type': 'soultimate',
            'soultimate_name': soultimate_data.get('command', 'Unknown Soultimate'),
            'damage': total_damage,
            'hits': hits,
            'is_crit': is_crit,
            'is_moxie': is_moxie,
            'element': soultimate_data.get('element'),
            'elemental_modifier': damage_result['multipliers']['elemental'],
            'damage_breakdown': damage_result,
            'target_remaining_hp': target['current_hp'],
            'target_fainted': target['is_fainted']
        }
        
        return result
    
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
