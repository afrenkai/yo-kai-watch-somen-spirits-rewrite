import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { Team } from '@/lib/api/types';

interface TeamState {
  currentTeam: Team | null;
  selectedTeamId: string | null;
  setCurrentTeam: (team: Team | null) => void;
  setSelectedTeamId: (id: string | null) => void;
  clearTeam: () => void;
}

export const useTeamStore = create<TeamState>()(
  persist(
    (set) => ({
      currentTeam: null,
      selectedTeamId: null,
      setCurrentTeam: (team) => set({ currentTeam: team }),
      setSelectedTeamId: (id) => set({ selectedTeamId: id }),
      clearTeam: () => set({ currentTeam: null, selectedTeamId: null }),
    }),
    {
      name: 'team-storage',
    }
  )
);
