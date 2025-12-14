'use client';

import Image from "next/image";
import styles from "./page.module.css";

export default function Battle() {
	return (
		<div className={styles.container}>
			<div className={styles.battleViewport}>
				<Image
					src="/images/battle/viewportBG.png"
					alt="Battle Viewport"
					fill
					className={styles.battleViewportBG}
					sizes="58vw"
					unoptimized
				/>

				<p className={`${styles.myName} ${styles.myName0}`}>Placeholder</p>
				<p className={`${styles.myName} ${styles.myName1}`}>Placeholder</p>
				<p className={`${styles.myName} ${styles.myName2}`}>Placeholder</p>

				<p className={`${styles.otherName} ${styles.otherName0}`}>Placeholder</p>
				<p className={`${styles.otherName} ${styles.otherName1}`}>Placeholder</p>
				<p className={`${styles.otherName} ${styles.otherName2}`}>Placeholder</p>

				<progress className={`${styles.HP} ${styles.myHP0}`} value={100} max={100} />
				<progress className={`${styles.HP} ${styles.myHP1}`} value={100} max={100} />
				<progress className={`${styles.HP} ${styles.myHP2}`} value={100} max={100} />

				<progress className={`${styles.HP} ${styles.otherHP0}`} value={100} max={100} />
				<progress className={`${styles.HP} ${styles.otherHP1}`} value={100} max={100} />
				<progress className={`${styles.HP} ${styles.otherHP2}`} value={100} max={100} />

				<progress className={`${styles.SOUL} ${styles.mySoul0}`} value={0} max={100} />
				<progress className={`${styles.SOUL} ${styles.mySoul1}`} value={0} max={100} />
				<progress className={`${styles.SOUL} ${styles.mySoul2}`} value={0} max={100} />

				<Image src="/images/teambuilder/whisperPlaceholder.webp" alt="My Yokai 0" width={100} height={100} className={`${styles.myYokai} ${styles.myYokai0}`} />
				<Image src="/images/teambuilder/whisperPlaceholder.webp" alt="My Yokai 1" width={100} height={100} className={`${styles.myYokai} ${styles.myYokai1}`} />
				<Image src="/images/teambuilder/whisperPlaceholder.webp" alt="My Yokai 2" width={100} height={100} className={`${styles.myYokai} ${styles.myYokai2}`} />

				<Image src="/images/battle/positive_inspirit.png" alt="Positive" width={30} height={30} className={`${styles.spin} ${styles.myPosInsp0}`} />
				<Image src="/images/battle/positive_inspirit.png" alt="Positive" width={30} height={30} className={`${styles.spin} ${styles.myPosInsp1}`} />
				<Image src="/images/battle/positive_inspirit.png" alt="Positive" width={30} height={30} className={`${styles.spin} ${styles.myPosInsp2}`} />
				<Image src="/images/battle/negative_inspirit.png" alt="Negative" width={30} height={30} className={`${styles.spin} ${styles.myNegInsp0}`} />
				<Image src="/images/battle/negative_inspirit.png" alt="Negative" width={30} height={30} className={`${styles.spin} ${styles.myNegInsp1}`} />
				<Image src="/images/battle/negative_inspirit.png" alt="Negative" width={30} height={30} className={`${styles.spin} ${styles.myNegInsp2}`} />

				<Image src="/images/teambuilder/whisperPlaceholder.webp" alt="Other Yokai 0" width={100} height={100} className={`${styles.otherYokai} ${styles.otherYokai0}`} />
				<Image src="/images/teambuilder/whisperPlaceholder.webp" alt="Other Yokai 1" width={100} height={100} className={`${styles.otherYokai} ${styles.otherYokai1}`} />
				<Image src="/images/teambuilder/whisperPlaceholder.webp" alt="Other Yokai 2" width={100} height={100} className={`${styles.otherYokai} ${styles.otherYokai2}`} />

				<Image src="/images/battle/positive_inspirit.png" alt="Positive" width={30} height={30} className={`${styles.spin} ${styles.otherPosInsp0}`} />
				<Image src="/images/battle/positive_inspirit.png" alt="Positive" width={30} height={30} className={`${styles.spin} ${styles.otherPosInsp1}`} />
				<Image src="/images/battle/positive_inspirit.png" alt="Positive" width={30} height={30} className={`${styles.spin} ${styles.otherPosInsp2}`} />
				<Image src="/images/battle/negative_inspirit.png" alt="Negative" width={30} height={30} className={`${styles.spin} ${styles.otherNegInsp0}`} />
				<Image src="/images/battle/negative_inspirit.png" alt="Negative" width={30} height={30} className={`${styles.spin} ${styles.otherNegInsp1}`} />
				<Image src="/images/battle/negative_inspirit.png" alt="Negative" width={30} height={30} className={`${styles.spin} ${styles.otherNegInsp2}`} />

				<Image src="/images/battle/pin.png" alt="Pin" width={20} height={20} className={styles.pin0} />
				<Image src="/images/battle/pin.png" alt="Pin" width={20} height={20} className={styles.pin1} />
				<Image src="/images/battle/pin.png" alt="Pin" width={20} height={20} className={styles.pin2} />

				<p className={`${styles.viewText} ${styles.myGuard0}`}>Guarding</p>
				<p className={`${styles.viewText} ${styles.myGuard1}`}>Guarding</p>
				<p className={`${styles.viewText} ${styles.myGuard2}`}>Guarding</p>
				<p className={`${styles.viewText} ${styles.myLoaf0}`}>Loafing...</p>
				<p className={`${styles.viewText} ${styles.myLoaf1}`}>Loafing...</p>
				<p className={`${styles.viewText} ${styles.myLoaf2}`}>Loafing...</p>

				<p className={`${styles.viewText} ${styles.otherGuard0}`}>Guarding</p>
				<p className={`${styles.viewText} ${styles.otherGuard1}`}>Guarding</p>
				<p className={`${styles.viewText} ${styles.otherGuard2}`}>Guarding</p>
				<p className={`${styles.viewText} ${styles.otherLoaf0}`}>Loafing...</p>
				<p className={`${styles.viewText} ${styles.otherLoaf1}`}>Loafing...</p>
				<p className={`${styles.viewText} ${styles.otherLoaf2}`}>Loafing...</p>
				<p className={`${styles.viewText} ${styles.otherCharge0}`}>Charging Soultimate!!!</p>
				<p className={`${styles.viewText} ${styles.otherCharge1}`}>Charging Soultimate!!!</p>
				<p className={`${styles.viewText} ${styles.otherCharge2}`}>Charging Soultimate!!!</p>

				<p className={styles.switchingText}>Opponent is switching Yokai!</p>
			</div>

			<video className={styles.soultimateVideo} />

			{[...Array(6)].map((_, i) => (
				<Image key={`m${i}`} id={`mpreload${i}`} src="" alt="" width={1} height={1} className={styles.preload} />
			))}
			{[...Array(6)].map((_, i) => (
				<Image key={`o${i}`} id={`opreload${i}`} src="" alt="" width={1} height={1} className={styles.preload} />
			))}

			<Image src="/images/panelBG.png" alt="Chat BG" width={400} height={200} className={styles.chatBG} />
			<div className={styles.chatBox}></div>
			<input type="text" className={styles.messageInput} autoComplete="off" />

			<Image src="/images/battle/wheelMidHexagon.png" alt="Wheel Mid" width={200} height={200} className={styles.wheelMid} />

			<button className={styles.soultimateButton}>
				<Image src="/images/battle/soultimateButtonNew.png" alt="Soultimate" fill sizes="21vmin" unoptimized />
			</button>
			<button className={styles.targetButton}>
				<Image src="/images/battle/targetButtonNew.png" alt="Target" fill sizes="21vmin" unoptimized />
			</button>
			<button className={styles.checkButton}>
				<Image src="/images/battle/checkButton.png" alt="Check" fill sizes="21vmin" unoptimized />
			</button>
			<button className={styles.purifyButton}>
				<Image src="/images/battle/purifyButtonNew.png" alt="Purify" fill sizes="21vmin" unoptimized />
			</button>

			<Image src="/images/battle/wheelBGHexagon.png" alt="Wheel BG" width={400} height={400} className={styles.wheelBG} />
			<Image src="/images/battle/wheelShadowHexagon.png" alt="Wheel Shadow" width={400} height={400} className={styles.wheelShadow} />
			<Image src="/images/battle/wheelLinesHexagon.png" alt="Wheel Lines" width={400} height={400} className={styles.wheelLines} />

			<div className={styles.wheelViewport}>
				<Image id="slot1" src="" alt="" width={80} height={80} className={styles.slot1} />
				<Image id="slot2" src="" alt="" width={80} height={80} className={styles.slot2} />
				<Image id="slot3" src="" alt="" width={80} height={80} className={styles.slot3} />
				<Image id="slot4" src="" alt="" width={80} height={80} className={styles.slot4} />
				<Image id="slot5" src="" alt="" width={80} height={80} className={styles.slot5} />
				<Image id="slot6" src="" alt="" width={80} height={80} className={styles.slot6} />

				{[...Array(6)].map((_, i) => (
					<Image key={i} id={`soulStatus${i}`} src="/images/battle/mSkillReady.png" alt="Soul Status" width={30} height={30} className={styles[`soulStatus${i}`]} />
				))}

				{[...Array(6)].map((_, i) => (
					<progress key={`hp${i}`} id={`pro${i}`} className={styles.HP} value={50} max={100} />
				))}

				{[...Array(6)].map((_, i) => (
					<progress key={`soul${i}`} id={`soul${i}`} className={styles.SOUL} value={100} max={100} />
				))}
			</div>

			<Image src="/images/battle/soultimateBG.png" alt="Soultimate BG" width={400} height={400} className={styles.soultimateBG} />
			<Image src="/images/teambuilder/whisperPlaceholder.webp" alt="Yokai Thumbnail" width={100} height={100} className={styles.yokaiThumbnail} />

			<progress className={`${styles.SOUL} ${styles.soultCharge}`} value={0} max={100} />
			<progress className={`${styles.DAMAGE} ${styles.pokeDamageCharge}`} value={0} max={100} />
			<progress className={`${styles.SOUL} ${styles.pokeSoulCharge}`} value={0} max={100} />

			<div className={styles.switchCooldown}>
				<p className={styles.cooldownCount}>3</p>
			</div>
			<div className={styles.switchTimer}>
				<p className={styles.timerCount}>3</p>
			</div>

			<Image src="/images/battle/targetCursor.png" alt="Target Cursor" width={50} height={50} className={styles.targetCursor} />
			<Image src="/images/battle/magnifyCursor.png" alt="Check Cursor" width={50} height={50} className={styles.checkCursor} />

			<div className={styles.infoDisplay}>
				<p className={styles.infoText}>Name: </p>
				<p className={styles.infoText}>HP: ---%</p>
				<p className={styles.infoText}>Active inspirits:</p>
			</div>

			<button className={styles.toggleMid}></button>

			{typeof window !== 'undefined' && (
				<audio id="bgm" suppressHydrationWarning />
			)}

			<button className={styles.toggleMusic}>
				<Image src="/images/musicON.png" alt="Toggle Music" width={50} height={50} />
			</button>

			<Image src="/images/battle/selectSoult.png" alt="Select Soult" width={400} height={400} className={styles.soultSelect} />
			<p className={styles.cancelSoult}>Click the soultimate button again to cancel!</p>

			<Image src="/images/battle/selectPurify.png" alt="Select Purify" width={400} height={400} className={styles.purifySelect} />
			<p className={styles.cancelPurify}>Click the purify button again to cancel!</p>

			<p className={styles.chargedLabel}>Charged!</p>

			<p className={styles.minigameTypeLabel}>placeholder lol</p>
			<input type="text" className={styles.minigameTypeInput} autoComplete="off" />

			<button className={styles.oneSoult}></button>
			<button className={styles.twoSoult}></button>
			<button className={styles.threeSoult}></button>

			<button className={styles.onePurify}></button>
			<button className={styles.twoPurify}></button>
			<button className={styles.threePurify}></button>

			<button className={styles.pokeDamageButton}></button>
			<button className={styles.pokeSoulButton}></button>

			<div className={styles.results}>
				<Image id="resultsImage" src="/images/battle/victory.webp" alt="Results" fill sizes="100vw" unoptimized />
			</div>

			<div className={styles.alertMessage}>
				<Image src="/images/fullPanelBG.png" alt="Alert BG" fill sizes="100vw" unoptimized />
				<p className={styles.alertText1}>
					The server took too long to respond. Please click anywhere to go back to matchmaking. Sorry!
				</p>
			</div>
		</div>
	);
}
