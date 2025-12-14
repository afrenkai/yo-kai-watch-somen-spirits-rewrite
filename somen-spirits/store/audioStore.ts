import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface AudioState {
  isMuted: boolean;
  volume: number;
  currentTrack: string | null;
  toggleMute: () => void;
  setVolume: (volume: number) => void;
  setCurrentTrack: (track: string | null) => void;
}

export const useAudioStore = create<AudioState>()(
  persist(
    (set) => ({
      isMuted: false,
      volume: 0.5,
      currentTrack: null,
      toggleMute: () => set((state) => ({ isMuted: !state.isMuted })),
      setVolume: (volume) => set({ volume: Math.max(0, Math.min(1, volume)) }),
      setCurrentTrack: (track) => set({ currentTrack: track }),
    }),
    {
      name: 'audio-storage',
    }
  )
);
