'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Image from "next/image";
import styles from "./page.module.css";
import { useAudio } from '@/hooks/useAudio';
import { useAudioStore } from '@/store/audioStore';

export default function Home() {
	const router = useRouter();
	const [showStartMenu, setShowStartMenu] = useState(false);
	const { isMuted, toggleMute } = useAudioStore();

	const { play: playBGM } = useAudio('/audios/music/Springdale.mp3', {
		volume: isMuted ? 0 : 0.5,
		loop: true,
		autoplay: false,
	});

	const handleBattleClick = () => {
		router.push('/teambuilder');
	};

	const handleTeambuilderClick = () => {
		router.push('/teambuilder');
	};

	const handleMenuClick = () => {
		setShowStartMenu(!showStartMenu);
	};

	const handleMusicToggle = () => {
		toggleMute();
	};

	useEffect(() => {
		playBGM();
	}, [playBGM]);

	return (
		<div className={styles.container}>
			<Image
				src="/images/home/homeBG.jpg"
				alt="Background"
				fill
				className={styles.bg}
				priority
				sizes="100vw"
				unoptimized
			/>

			<Image
				src="/images/home/TokoPortrait.png"
				alt="Toko Portrait"
				width={400}
				height={800}
				className={styles.dialogPortrait}
			/>

			<Image
				src="/images/home/homePanel.png"
				alt="Home Panel"
				width={800}
				height={1000}
				className={styles.homePanel}
			/>

			<Image
				src="/images/home/Logo.png"
				alt="Yo-kai Watch Somen Spirits"
				width={600}
				height={400}
				className={styles.logo}
			/>

			<button className={styles.battleButton} onClick={handleBattleClick}>
				Battle!
			</button>

			<button className={styles.teambuilderButton} onClick={handleTeambuilderClick}>
				Teambuilder
			</button>

			<button className={styles.toggleMusic} onClick={handleMusicToggle}>
				<Image
					src={isMuted ? "/images/musicOFF.png" : "/images/musicON.png"}
					alt="Toggle Music"
					width={50}
					height={50}
				/>
			</button>

			{showStartMenu && (
				<div className={styles.startMenu}>
					<Image
						src="/images/fullPanelBG.png"
						alt="Menu Background"
						width={600}
						height={800}
						className={styles.menuBG}
					/>
					<h2>Menu</h2>
					<button onClick={() => setShowStartMenu(false)}>Close</button>
				</div>
			)}

			<Image
				src="/images/padTrans.png"
				alt="Transition"
				fill
				className={styles.padTrans}
				sizes="100vw"
				unoptimized
			/>
		</div>
	);
}
