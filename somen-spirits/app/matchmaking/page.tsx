'use client';

import Image from "next/image";
import styles from "./page.module.css";

export default function Matchmaking() {
	return (
		<div className={styles.container}>
			<Image
				src="/images/home/home2_upscaled (1).jpeg"
				alt="Background"
				fill
				className={styles.bg}
				priority
				sizes="100vw"
				unoptimized
			/>

			<Image
				src="/images/matchmaking/spriteBG.png"
				alt="Background Sprite"
				fill
				className={styles.bgSprite}
				sizes="100vw"
				unoptimized
			/>

			<Image
				src="/images/panelBG.png"
				alt="Menu Panel"
				width={800}
				height={1000}
				className={styles.menuBG}
			/>

			<button className={styles.homeButton}>
				<Image
					src="/images/teambuilder/padIcon.png"
					alt="Home"
					width={50}
					height={50}
				/>
			</button>

			<button className={styles.toggleMusic}>
				<Image
					src="/images/musicON.png"
					alt="Toggle Music"
					width={50}
					height={50}
				/>
			</button>

			<p className={styles.tierLabel}>Select a format!</p>
			<select className={`${styles.tierSelect} ${styles.uiBG}`}>
				<option>OU</option>
			</select>

			<p className={styles.teamLabel}>Choose a team!</p>
			<select className={`${styles.teamSelect} ${styles.uiBG}`}></select>

			<input
				type="text"
				className={`${styles.usernameInput} ${styles.uiBG}`}
				placeholder="Enter username"
				autoComplete="off"
			/>

			<p className={styles.countData}>
				Total Online: --- | Active Battles: --- | Players Looking for Games: ---
			</p>

			<button className={`${styles.battleButton} ${styles.uiBG}`}>
				Battle!
			</button>

			<div className={styles.matchmakingMenu}>
				<Image
					src="/images/fullPanelBG.png"
					alt="Full Panel"
					fill
					className={styles.fullPanelBG}
					sizes="100vw"
					unoptimized
				/>
				<p className={styles.lookingText}>
					Looking for opponents... (click anywhere to cancel)
				</p>
			</div>

			{typeof window !== 'undefined' && (
				<>
					<audio id="bgm" suppressHydrationWarning />
					<audio id="menuSFX" suppressHydrationWarning />
					<audio id="beachSFX" src="/audios/BeachBG.mp3" suppressHydrationWarning />
				</>
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
