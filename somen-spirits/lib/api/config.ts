export const API_CONFIG = {
	baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
	timeout: 30000,
	headers: {
		'Content-Type': 'application/json',
	},
};

export const API_ENDPOINTS = {
	yokai: {
		list: '/api/yokai/',
		get: (id: string) => `/api/yokai/${id}/`,
	},
	teams: {
		list: '/api/teams/',
		get: (id: string) => `/api/teams/${id}/`,
		create: '/api/teams/',
		update: (id: string) => `/api/teams/${id}/`,
		delete: (id: string) => `/api/teams/${id}/`,
	},
	matchmaking: {
		join: '/api/matchmaking/join/',
		leave: '/api/matchmaking/leave/',
		status: '/api/matchmaking/status/',
	},
	battles: {
		create: '/api/battles/',
		get: (id: string) => `/api/battles/${id}/`,
		action: (id: string) => `/api/battles/${id}/action/`,
	},
	users: {
		create: '/api/users/',
		get: (id: string) => `/api/users/${id}/`,
	},
	attacks: '/api/attacks/',
	attitudes: '/api/attitudes/',
	equipment: '/api/equipment/',
	inspirits: '/api/inspirits/',
	skills: '/api/skills/',
	soulGems: '/api/soul-gems/',
	soultimates: '/api/soultimates/',
	techniques: '/api/techniques/',
};

export const WS_CONFIG = {
	url: process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000',
	reconnection: true,
	reconnectionAttempts: 5,
	reconnectionDelay: 1000,
};
