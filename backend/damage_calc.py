import random
from typing import Dict, Any, Tuple, Optional, List


#based on DamageCalc.js from hilwin's website repo, which I assume has proper logic


def get_random_multiplier() -> float:
    return round(random.uniform(0.9, 1.1), 2)


def calculate_stats(
    yokai_data: Dict[str, Any],
    hp_iv: int,
    str_iv: int,
    spr_iv: int,
    def_iv: int,
    spd_iv: int,
    level: int,
    hp_gym: int,
    str_gym: int,
    spr_gym: int,
    def_gym: int,
    spd_gym: int,
    hp_boost: int,
    str_boost: int,
    spr_boost: int,
    def_boost: int,
    spd_boost: int
) -> Tuple[int, int, int, int, int]:
    """
    Calculate final stats for a Yokai including IVs, EVs (gym), and attitude bonuses
    Returns: (HP, STR, SPR, DEF, SPD)
    
    #TODO: This is a placeholder that needs to be implemented based on game mechanics
    """
    # Base stats from yokai_data
    base_hp = yokai_data.get('hp', 100)
    base_str = yokai_data.get('str', 50)
    base_spr = yokai_data.get('spr', 50)
    base_def = yokai_data.get('def', 50)
    base_spd = yokai_data.get('spd', 50)
    
    final_hp = int(base_hp + hp_iv + hp_gym + hp_boost)
    final_str = int(base_str + str_iv + str_gym + str_boost)
    final_spr = int(base_spr + spr_iv + spr_gym + spr_boost)
    final_def = int(base_def + def_iv + def_gym + def_boost)
    final_spd = int(base_spd + spd_iv + spd_gym + spd_boost)
    
    return (final_hp, final_str, final_spr, final_def, final_spd)


def get_attack_damage(
    attack_data: Dict[str, Any],
    attacker_str: int,
    attacker_spr: int,
    defender_data: Dict[str, Any],
    defender_def: int,
    defender_hp: int,
    attack_type: int,
    is_defending: bool = False,
    is_crit: bool = False,
    is_moxie: bool = False,
    attitude_str_boost: int = 0,
    attitude_spr_boost: int = 0,
    attitude_def_boost: int = 0
) -> Dict[str, Any]:
    """
    Calculate damage for an attack based on type and conditions
    
    Args:
        attack_data: Attack/Technique/Soultimate data
        attacker_str: Attacker's STR stat
        attacker_spr: Attacker's SPR stat
        defender_data: Defender's yokai data (for elemental resistances)
        defender_def: Defender's DEF stat
        defender_hp: Defender's current HP
        attack_type: 1=Attack, 2=Technique, 3=Soultimate
        is_defending: Whether defender is in guard stance
        is_crit: Whether this is a critical hit
        is_moxie: Whether Moxie skill is active (Soultimate only)
        attitude_str_boost: STR boost from attitude
        attitude_spr_boost: SPR boost from attitude
        attitude_def_boost: DEF boost from attitude
    
    Returns:
        Dictionary with damage, hits to KO, and other combat info
    """
    power = int(attack_data.get('bp', 0) or attack_data.get('Lv10_power', 0))
    elemental_resistance = 1.0
    chosen_attack_stat = 0
    hit_amount = 1
    crit_multiplier = 1.0
    defence = defender_def + attitude_def_boost
    
    if attack_type == 1:  # Physical Attack
        chosen_attack_stat = attacker_str + attitude_str_boost
        hit_amount = attack_data.get('N_Hits', 1) or attack_data.get('hits', 1)
    
    elif attack_type == 2:  # Technique
        chosen_attack_stat = attacker_spr + attitude_spr_boost
        element = attack_data.get('Element') or attack_data.get('attribute')
        
        if element:
            # Get elemental resistance from defender
            resistance_map = {
                'fire': 'fire_res',
                'water': 'water_res',
                'lightning': 'lightning_res',
                'earth': 'earth_res',
                'wind': 'wind_res',
                'ice': 'ice_res'
            }
            res_key = resistance_map.get(element.lower())
            if res_key:
                elemental_resistance = defender_data.get(res_key, 1.0)
        
        hit_amount = 1
    
    elif attack_type == 3:  
        chosen_attack_stat = attacker_str + attitude_str_boost
        
        element = attack_data.get('element_type') or attack_data.get('Element')
        if element and element.lower() != 'none':
            chosen_attack_stat = attacker_spr + attitude_spr_boost
            
            resistance_map = {
                'fire': 'fire_res',
                'water': 'water_res',
                'lightning': 'lightning_res',
                'earth': 'earth_res',
                'wind': 'wind_res',
                'ice': 'ice_res'
            }
            res_key = resistance_map.get(element.lower())
            if res_key:
                elemental_resistance = defender_data.get(res_key, 1.0)
        
        hit_amount = attack_data.get('N_Hits', 1) or attack_data.get('hits', 1)
    
    random_multiplier = get_random_multiplier()
    
    defence_multiplier = 0.5 if is_defending else 1.0
    
    if is_crit:
        defence = 0
        crit_multiplier = 1.25
    
    moxie_multiplier = 1.0
    if is_moxie and attack_type == 3:
        moxie_multiplier = 2.0
    
    raw_damage = (chosen_attack_stat / 2 + power / 2 - defence / 4)
    
    if raw_damage < 1:
        raw_damage = 1
    
    final_damage = (
        raw_damage * 
        random_multiplier * 
        defence_multiplier * 
        elemental_resistance * 
        crit_multiplier * 
        moxie_multiplier
    )
    
    final_damage = round(final_damage)
    
    hits_to_ko = calculate_hits_to_ko(final_damage, defender_hp)
    
    return {
        'damage': final_damage,
        'raw_damage': round(raw_damage),
        'hits_to_ko': hits_to_ko,
        'multipliers': {
            'random': random_multiplier,
            'defence': defence_multiplier,
            'elemental': elemental_resistance,
            'crit': crit_multiplier,
            'moxie': moxie_multiplier
        },
        'stats_used': {
            'attack_stat': chosen_attack_stat,
            'power': power,
            'defence': round(defence),
            'hit_amount': hit_amount
        }
    }


def calculate_hits_to_ko(damage: int, defender_hp: int) -> int:
    """
    Calculate how many hits it takes to KO the defender
    
    Args:
        damage: Damage per hit
        defender_hp: Defender's current HP
    
    Returns:
        Number of hits required to KO
    """
    if damage <= 0:
        return float('inf')
    
    import math
    return math.ceil(defender_hp / damage)


def validate_ivs(ivs: List[int]) -> bool:
    """
    Validate that IVs sum to 40 and are all non-negative
    
    Args:
        ivs: List of 5 IV values [HP, STR, SPR, DEF, SPD]
    
    Returns:
        True if valid, False otherwise
    """
    if len(ivs) != 5:
        return False
    
    if any(iv < 0 for iv in ivs):
        return False
    
    if sum(ivs) != 40:
        return False
    
    return True


def validate_gym_stats(gym_stats: List[int]) -> bool:
    """
    Validate that gym stats don't exceed the limit of 5 total
    
    Args:
        gym_stats: List of 4 gym stat values [STR, SPR, DEF, SPD]
    
    Returns:
        True if valid, False otherwise
    """
    if len(gym_stats) != 4:
        return False
    
    if any(stat < 0 for stat in gym_stats):
        return False
    
    if sum(gym_stats) > 5:
        return False
    
    return True


def calculate_damage_range(
    attack_data: Dict[str, Any],
    attacker_str: int,
    attacker_spr: int,
    defender_data: Dict[str, Any],
    defender_def: int,
    attack_type: int,
    is_defending: bool = False,
    is_crit: bool = False,
    is_moxie: bool = False,
    attitude_str_boost: int = 0,
    attitude_spr_boost: int = 0,
    attitude_def_boost: int = 0
) -> Dict[str, int]:
    """
    Calculate minimum and maximum damage range (accounting for random multiplier)
    
    Returns:
        Dictionary with 'min' and 'max' damage values
    """
    min_result = get_attack_damage(
        attack_data=attack_data,
        attacker_str=attacker_str,
        attacker_spr=attacker_spr,
        defender_data=defender_data,
        defender_def=defender_def,
        defender_hp=100,  # TODO: Placeholder
        attack_type=attack_type,
        is_defending=is_defending,
        is_crit=is_crit,
        is_moxie=is_moxie,
        attitude_str_boost=attitude_str_boost,
        attitude_spr_boost=attitude_spr_boost,
        attitude_def_boost=attitude_def_boost
    )
    
    # Calculate with maximum multiplier (1.1)
    max_result = get_attack_damage(
        attack_data=attack_data,
        attacker_str=attacker_str,
        attacker_spr=attacker_spr,
        defender_data=defender_data,
        defender_def=defender_def,
        defender_hp=100,  # TODO: Placeholder
        attack_type=attack_type,
        is_defending=is_defending,
        is_crit=is_crit,
        is_moxie=is_moxie,
        attitude_str_boost=attitude_str_boost,
        attitude_spr_boost=attitude_spr_boost,
        attitude_def_boost=attitude_def_boost
    )
    
    base_multipliers = (
        min_result['multipliers']['defence'] *
        min_result['multipliers']['elemental'] *
        min_result['multipliers']['crit'] *
        min_result['multipliers']['moxie']
    )
    
    raw = min_result['raw_damage']
    
    return {
        'min': round(raw * 0.9 * base_multipliers),
        'max': round(raw * 1.1 * base_multipliers)
    }
