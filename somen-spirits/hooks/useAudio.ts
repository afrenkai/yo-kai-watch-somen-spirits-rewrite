'use client';

import { useEffect, useRef, useState, useCallback } from 'react';

interface UseAudioOptions {
	volume?: number;
	loop?: boolean;
	autoplay?: boolean;
}

export function useAudio(src: string, options: UseAudioOptions = {}) {
	const {
		volume = 0.5,
		loop = false,
		autoplay = false,
	} = options;

	const audioRef = useRef<HTMLAudioElement | null>(null);
	const [isPlaying, setIsPlaying] = useState(false);
	const [currentTime, setCurrentTime] = useState(0);
	const [duration, setDuration] = useState(0);

	useEffect(() => {
		if (typeof window === 'undefined') return;

		const audio = new Audio(src);
		audio.volume = volume;
		audio.loop = loop;
		audioRef.current = audio;

		const handlePlay = () => setIsPlaying(true);
		const handlePause = () => setIsPlaying(false);
		const handleTimeUpdate = () => setCurrentTime(audio.currentTime);
		const handleLoadedMetadata = () => setDuration(audio.duration);
		const handleEnded = () => setIsPlaying(false);

		audio.addEventListener('play', handlePlay);
		audio.addEventListener('pause', handlePause);
		audio.addEventListener('timeupdate', handleTimeUpdate);
		audio.addEventListener('loadedmetadata', handleLoadedMetadata);
		audio.addEventListener('ended', handleEnded);

		if (autoplay) {
			audio.play().catch(console.error);
		}

		return () => {
			audio.pause();
			audio.removeEventListener('play', handlePlay);
			audio.removeEventListener('pause', handlePause);
			audio.removeEventListener('timeupdate', handleTimeUpdate);
			audio.removeEventListener('loadedmetadata', handleLoadedMetadata);
			audio.removeEventListener('ended', handleEnded);
		};
	}, [src, volume, loop, autoplay]);

	const play = useCallback(() => {
		audioRef.current?.play().catch(console.error);
	}, []);

	const pause = useCallback(() => {
		audioRef.current?.pause();
	}, []);

	const stop = useCallback(() => {
		if (audioRef.current) {
			audioRef.current.pause();
			audioRef.current.currentTime = 0;
		}
	}, []);

	const setVolume = useCallback((newVolume: number) => {
		if (audioRef.current) {
			audioRef.current.volume = Math.max(0, Math.min(1, newVolume));
		}
	}, []);

	const seek = useCallback((time: number) => {
		if (audioRef.current) {
			audioRef.current.currentTime = time;
		}
	}, []);

	return {
		isPlaying,
		currentTime,
		duration,
		play,
		pause,
		stop,
		setVolume,
		seek,
	};
}

export function useBackgroundMusic() {
	const [isMuted, setIsMuted] = useState(false);
	const [currentTrack, setCurrentTrack] = useState<string | null>(null);

	// should load mute from localStorage if i read correctly
	useEffect(() => {
		const saved = localStorage.getItem('BGMute');
		setIsMuted(saved === 'false');
	}, []);

	const toggleMute = useCallback(() => {
		setIsMuted((prev) => {
			const newValue = !prev;
			localStorage.setItem('BGMute', String(newValue));
			return newValue;
		});
	}, []);

	const playTrack = useCallback((src: string) => {
		setCurrentTrack(src);
	}, []);

	const stopTrack = useCallback(() => {
		setCurrentTrack(null);
	}, []);

	return {
		isMuted,
		currentTrack,
		toggleMute,
		playTrack,
		stopTrack,
	};
}
