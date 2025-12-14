import { create } from 'zustand';
import type { BattleState } from '@/lib/api/types';

interface BattleStoreState {
  battle: BattleState | null;
  isInBattle: boolean;
  currentTurn: number;
  setBattle: (battle: BattleState | null) => void;
  setCurrentTurn: (turn: number) => void;
  endBattle: () => void;
}

export const useBattleStore = create<BattleStoreState>((set) => ({
  battle: null,
  isInBattle: false,
  currentTurn: 0,
  setBattle: (battle) => set({ battle, isInBattle: !!battle }),
  setCurrentTurn: (turn) => set({ currentTurn: turn }),
  endBattle: () => set({ battle: null, isInBattle: false, currentTurn: 0 }),
}));
