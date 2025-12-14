import { api } from './client';
import { API_ENDPOINTS } from './config';
import type {
  Yokai,
  Team,
  User,
  Attack,
  Technique,
  Inspirit,
  Soultimate,
  Skill,
  Attitude,
  Equipment,
  MatchmakingRequest,
  MatchmakingResponse,
  BattleState,
} from './types';

export const yokaiApi = {
  getAll: () => api.get<Yokai[]>(API_ENDPOINTS.yokai.list),
  getById: (id: string) => api.get<Yokai>(API_ENDPOINTS.yokai.get(id)),
  search: (query: string) => api.get<Yokai[]>(`${API_ENDPOINTS.yokai.list}?search=${encodeURIComponent(query)}`),
};

export const teamsApi = {
  getAll: () => api.get<Team[]>(API_ENDPOINTS.teams.list),
  getById: (id: string) => api.get<Team>(API_ENDPOINTS.teams.get(id)),
  getByUserId: (userId: string) => api.get<Team[]>(`${API_ENDPOINTS.teams.list}?user_id=${userId}`),
  create: (team: Omit<Team, 'id' | 'created_at' | 'updated_at'>) =>
    api.post<Team>(API_ENDPOINTS.teams.create, team),
  update: (id: string, team: Partial<Team>) =>
    api.put<Team>(API_ENDPOINTS.teams.update(id), team),
  delete: (id: string) => api.delete(API_ENDPOINTS.teams.delete(id)),
};

export const usersApi = {
  create: (username: string) =>
    api.post<User>(API_ENDPOINTS.users.create, { username }),
  getById: (id: string) => api.get<User>(API_ENDPOINTS.users.get(id)),
};

export const matchmakingApi = {
  join: (request: MatchmakingRequest) =>
    api.post<MatchmakingResponse>(API_ENDPOINTS.matchmaking.join, request),
  leave: (userId: string) =>
    api.post(API_ENDPOINTS.matchmaking.leave, { user_id: userId }),
  getStatus: () => api.get<{
    total_online: number;
    active_battles: number;
    looking_for_games: number;
  }>(API_ENDPOINTS.matchmaking.status),
};

export const battlesApi = {
  create: (player1_id: string, player2_id: string, team1_id: string, team2_id: string) =>
    api.post<BattleState>(API_ENDPOINTS.battles.create, {
      player1_id,
      player2_id,
      team1_id,
      team2_id,
    }),
  getById: (id: string) => api.get<BattleState>(API_ENDPOINTS.battles.get(id)),
  submitAction: (battleId: string, action: unknown) =>
    api.post(API_ENDPOINTS.battles.action(battleId), action),
};

export const attacksApi = {
  getAll: () => api.get<Attack[]>(API_ENDPOINTS.attacks),
};

export const techniquesApi = {
  getAll: () => api.get<Technique[]>(API_ENDPOINTS.techniques),
};

export const inspiritsApi = {
  getAll: () => api.get<Inspirit[]>(API_ENDPOINTS.inspirits),
};

export const soultimatesApi = {
  getAll: () => api.get<Soultimate[]>(API_ENDPOINTS.soultimates),
};

export const skillsApi = {
  getAll: () => api.get<Skill[]>(API_ENDPOINTS.skills),
};

export const attitudesApi = {
  getAll: () => api.get<Attitude[]>(API_ENDPOINTS.attitudes),
};

export const equipmentApi = {
  getAll: () => api.get<Equipment[]>(API_ENDPOINTS.equipment),
};
