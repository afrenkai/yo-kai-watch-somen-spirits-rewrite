import { create } from 'zustand';

type MatchmakingStatus = 'idle' | 'searching' | 'found' | 'error';

interface MatchmakingState {
  status: MatchmakingStatus;
  tier: string | null;
  playersInQueue: number;
  opponentId: string | null;
  error: string | null;
  setStatus: (status: MatchmakingStatus) => void;
  setTier: (tier: string | null) => void;
  setPlayersInQueue: (count: number) => void;
  setOpponent: (opponentId: string | null) => void;
  setError: (error: string | null) => void;
  reset: () => void;
}

export const useMatchmakingStore = create<MatchmakingState>((set) => ({
  status: 'idle',
  tier: null,
  playersInQueue: 0,
  opponentId: null,
  error: null,
  setStatus: (status) => set({ status }),
  setTier: (tier) => set({ tier }),
  setPlayersInQueue: (count) => set({ playersInQueue: count }),
  setOpponent: (opponentId) => set({ opponentId }),
  setError: (error) => set({ error }),
  reset: () => set({
    status: 'idle',
    tier: null,
    playersInQueue: 0,
    opponentId: null,
    error: null,
  }),
}));
