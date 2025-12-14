'use client';

import { useEffect, useState } from 'react';
import { attitudesApi, equipmentApi } from '@/lib/api';
import type { Attitude, Equipment } from '@/lib/api/types';

let cachedAttitudes: Attitude[] | null = null;
let cachedAttitudesMap: { [key: string]: Attitude } | null = null;
let attitudesPromise: Promise<Attitude[]> | null = null;

let cachedEquipment: Equipment[] | null = null;
let cachedEquipmentMap: { [key: string]: Equipment } | null = null;
let equipmentPromise: Promise<Equipment[]> | null = null;

export function useAttitudes() {
	const [attitudes, setAttitudes] = useState<Attitude[]>(() => cachedAttitudes || []);
	const [attitudesMap, setAttitudesMap] = useState<{ [key: string]: Attitude }>(() => cachedAttitudesMap || {});
	const [loading, setLoading] = useState(!cachedAttitudes);
	const [error, setError] = useState<Error | null>(null);

	useEffect(() => {
		if (cachedAttitudes && cachedAttitudesMap) {
			setAttitudes(cachedAttitudes);
			setAttitudesMap(cachedAttitudesMap);
			setLoading(false);
			return;
		}

		if (attitudesPromise) {
			attitudesPromise
				.then((data) => {
					const map: { [key: string]: Attitude } = {};
					data.forEach(attitude => {
						map[attitude.id] = attitude;
					});
					setAttitudes(data);
					setAttitudesMap(map);
					setLoading(false);
				})
				.catch((err) => {
					setError(err instanceof Error ? err : new Error('Failed to fetch attitudes'));
					setLoading(false);
				});
			return;
		}

		let cancelled = false;

		async function fetchAttitudes() {
			try {
				setLoading(true);
				setError(null);

				attitudesPromise = attitudesApi.getAll();
				const data = await attitudesPromise;

				if (!cancelled) {
					setAttitudes(data);
					const map: { [key: string]: Attitude } = {};
					data.forEach(attitude => {
						map[attitude.id] = attitude;
					});
					setAttitudesMap(map);
					cachedAttitudes = data;
					cachedAttitudesMap = map;
				}
			} catch (err) {
				if (!cancelled) {
					setError(err instanceof Error ? err : new Error('Failed to fetch attitudes'));
				}
				attitudesPromise = null;
			} finally {
				if (!cancelled) {
					setLoading(false);
				}
			}
		}

		fetchAttitudes();

		return () => {
			cancelled = true;
		};
	}, []);

	return { attitudes, attitudesMap, loading, error };
}

export function useEquipment() {
	const [equipment, setEquipment] = useState<Equipment[]>(() => cachedEquipment || []);
	const [equipmentMap, setEquipmentMap] = useState<{ [key: string]: Equipment }>(() => cachedEquipmentMap || {});
	const [loading, setLoading] = useState(!cachedEquipment);
	const [error, setError] = useState<Error | null>(null);

	useEffect(() => {
		if (cachedEquipment && cachedEquipmentMap) {
			setEquipment(cachedEquipment);
			setEquipmentMap(cachedEquipmentMap);
			setLoading(false);
			return;
		}

		if (equipmentPromise) {
			equipmentPromise
				.then((data) => {
					const map: { [key: string]: Equipment } = {};
					data.forEach(item => {
						map[item.id] = item;
					});
					setEquipment(data);
					setEquipmentMap(map);
					setLoading(false);
				})
				.catch((err) => {
					setError(err instanceof Error ? err : new Error('Failed to fetch equipment'));
					setLoading(false);
				});
			return;
		}

		let cancelled = false;

		async function fetchEquipment() {
			try {
				setLoading(true);
				setError(null);

				equipmentPromise = equipmentApi.getAll();
				const data = await equipmentPromise;

				if (!cancelled) {
					setEquipment(data);
					const map: { [key: string]: Equipment } = {};
					data.forEach(item => {
						map[item.id] = item;
					});
					setEquipmentMap(map);
					cachedEquipment = data;
					cachedEquipmentMap = map;
				}
			} catch (err) {
				if (!cancelled) {
					setError(err instanceof Error ? err : new Error('Failed to fetch equipment'));
				}
				equipmentPromise = null;
			} finally {
				if (!cancelled) {
					setLoading(false);
				}
			}
		}

		fetchEquipment();

		return () => {
			cancelled = true;
		};
	}, []);

	return { equipment, equipmentMap, loading, error };
}
