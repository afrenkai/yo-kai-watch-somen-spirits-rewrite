import type { Yokai, TeamYokai } from '@/lib/api/types';

export function createDefaultTeamYokai(
yokai: Yokai,
position: number
): Omit<TeamYokai, 'yokai_id'> & { yokai_id: string } {
return {
yokai_id: yokai.id,
position,
level: 50,
attitude_id: 'rough',
loafing_attitude_id: 'serious',
ivs: {
hp: 0,
str: 0,
spr: 0,
def: 0,
spd: 0,
},
evs: {
hp: 0,
str: 0,
spr: 0,
def: 0,
spd: 0,
},
gym_points: {
str: 0,
spr: 0,
def: 0,
spd: 0,
},
equipment: [],
};
}

export function getYokaiImageUrl(yokai: Yokai, type: 'medal' | 'sprite' = 'medal'): string {
if (type === 'medal') {
return yokai.artwork_image || `/images/yokai/medals/${yokai.id}.png`;
}
return `/images/yokai/sprites/${yokai.id}-idle.png`;
}

export function formatStat(value: number): string {
return value.toString().padStart(3, '0');
}

export function getTeamTypeColor(teamType: 'bony' | 'fleshy'): string {
return teamType === 'bony' ? '#ff6b6b' : '#4ecdc4';
}
