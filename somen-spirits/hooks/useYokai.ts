'use client';

import { useEffect, useState } from 'react';
import { yokaiApi } from '@/lib/api';
import type { Yokai } from '@/lib/api/types';

let cachedYokaiList: Yokai[] | null = null;
let cachePromise: Promise<Yokai[]> | null = null;

export function useYokai(id?: number) {
	const [yokai, setYokai] = useState<Yokai | null>(null);
	const [loading, setLoading] = useState(true);
	const [error, setError] = useState<Error | null>(null);

	useEffect(() => {
		if (!id) {
			setLoading(false);
			return;
		}

		let cancelled = false;

		async function fetchYokai() {
			try {
				setLoading(true);
				setError(null);
				const data = await yokaiApi.getById(String(id));
				if (!cancelled) {
					setYokai(data);
				}
			} catch (err) {
				if (!cancelled) {
					setError(err instanceof Error ? err : new Error('Failed to fetch yokai'));
				}
			} finally {
				if (!cancelled) {
					setLoading(false);
				}
			}
		}

		fetchYokai();

		return () => {
			cancelled = true;
		};
	}, [id]);

	return { yokai, loading, error };
}

export function useYokaiList() {
	const [yokaiList, setYokaiList] = useState<Yokai[]>(() => cachedYokaiList || []);
	const [loading, setLoading] = useState(!cachedYokaiList);
	const [error, setError] = useState<Error | null>(null);

	useEffect(() => {
		if (cachedYokaiList) {
			setYokaiList(cachedYokaiList);
			setLoading(false);
			return;
		}

		if (cachePromise) {
			cachePromise
				.then((data) => {
					setYokaiList(data);
					setLoading(false);
				})
				.catch((err) => {
					setError(err instanceof Error ? err : new Error('Failed to fetch yokai list'));
					setLoading(false);
				});
			return;
		}

		let cancelled = false;

		async function fetchYokaiList() {
			try {
				setLoading(true);
				setError(null);

				cachePromise = yokaiApi.getAll();
				const data = await cachePromise;

				if (!cancelled) {
					cachedYokaiList = data;
					setYokaiList(data);
				}
			} catch (err) {
				if (!cancelled) {
					setError(err instanceof Error ? err : new Error('Failed to fetch yokai list'));
				}
				cachePromise = null;
			} finally {
				if (!cancelled) {
					setLoading(false);
				}
			}
		}

		fetchYokaiList();

		return () => {
			cancelled = true;
		};
	}, []);

	return { yokaiList, loading, error };
}

export function useYokaiSearch(query: string) {
	const [results, setResults] = useState<Yokai[]>([]);
	const [loading, setLoading] = useState(false);
	const [error, setError] = useState<Error | null>(null);

	useEffect(() => {
		if (!query.trim()) {
			setResults([]);
			return;
		}

		let cancelled = false;
		const timeoutId = setTimeout(async () => {
			try {
				setLoading(true);
				setError(null);
				const data = await yokaiApi.search(query);
				if (!cancelled) {
					setResults(data);
				}
			} catch (err) {
				if (!cancelled) {
					setError(err instanceof Error ? err : new Error('Failed to search yokai'));
				}
			} finally {
				if (!cancelled) {
					setLoading(false);
				}
			}
		}, 300); // finally I get to debounce

		return () => {
			cancelled = true;
			clearTimeout(timeoutId);
		};
	}, [query]);

	return { results, loading, error };
}
