'use client';

import Image from "next/image";
import styles from "./page.module.css";

export default function Countdown() {
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
				src="/images/home/Logo.png"
				alt="Yo-kai Watch Somen Spirits"
				width={600}
				height={400}
				className={styles.logo}
			/>

			<p className={styles.countdown}>-1-1:-1-1</p>
		</div>
	);
}
