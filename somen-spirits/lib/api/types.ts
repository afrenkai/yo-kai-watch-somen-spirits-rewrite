export interface Yokai {
  id: string;
  name: string;
  image: string | null;
  bs_a_hp: number;
  bs_a_str: number;
  bs_a_spr: number;
  bs_a_def: number;
  bs_a_spd: number;
  bs_b_hp: number;
  bs_b_str: number;
  bs_b_spr: number;
  bs_b_def: number;
  bs_b_spd: number;
  fire_res: number;
  water_res: number;
  electric_res: number;
  earth_res: number;
  wind_res: number;
  ice_res: number;
  equipment_slots: number;
  attack_prob: number;
  attack_id: string;
  technique_prob: number;
  technique_id: string | null;
  inspirit_prob: number;
  inspirit_id: string | null;
  guard_prob: number;
  soultimate_id: string;
  skill_id: number | null;
  rank: string;
  tribe: string;
  artwork_image: string | null;
  tier: string | null;
  extra: string | null;
}

export interface Attack {
  id: string;
  name: string;
  description: string;
  element: string;
  power: number;
  accuracy: number;
  target: string;
}

export interface Technique {
  id: string;
  name: string;
  description: string;
  element: string;
  power: number;
  accuracy: number;
  target: string;
  mp_cost: number;
}

export interface Inspirit {
  id: string;
  name: string;
  description: string;
  stat_changes: Record<string, number>;
  duration: number;
}

export interface Soultimate {
  id: string;
  name: string;
  description: string;
  element: string;
  power: number;
  target: string;
  video: string | null;
}

export interface Skill {
  id: number;
  name: string;
  description: string;
  effect: string;
}

export interface Attitude {
  id: string;
  name: string;
  hp_mod: number;
  str_mod: number;
  spr_mod: number;
  def_mod: number;
  spd_mod: number;
}

export interface Equipment {
  id: string;
  name: string;
  description: string;
  hp_boost: number;
  str_boost: number;
  spr_boost: number;
  def_boost: number;
  spd_boost: number;
  resistances: Record<string, number>;
}

export interface TeamYokai {
  yokai_id: string;
  position: number; // 0-5
  nickname?: string;
  level: number;
  attitude_id: string;
  loafing_attitude_id: string;
  ivs: {
    hp: number;
    str: number;
    spr: number;
    def: number;
    spd: number;
  };
  evs: {
    hp: number;
    str: number;
    spr: number;
    def: number;
    spd: number;
  };
  gym_points: {
    str: number;
    spr: number;
    def: number;
    spd: number;
  };
  equipment: string[]; // Equipment IDs
}

export interface Team {
  id: string;
  user_id: string;
  name: string;
  team_type: 'bony' | 'fleshy';
  yokai: TeamYokai[];
  created_at: string;
  updated_at: string;
}

export interface User {
  id: string;
  username: string;
  created_at: string;
}

export interface BattleState {
  id: string;
  player1_id: string;
  player2_id: string;
  player1_team: Team;
  player2_team: Team;
  current_turn: number;
  status: 'waiting' | 'active' | 'finished';
  winner_id: string | null;
  created_at: string;
}

export interface MatchmakingRequest {
  user_id: string;
  team_id: string;
  tier: string;
}

export interface MatchmakingResponse {
  match_id: string;
  opponent_id: string;
  battle_id: string;
}
