import { API_CONFIG } from './config';

function fetchWithTimeout(url: string, options: RequestInit = {}, timeout = 10000): Promise<Response> {
	return Promise.race([
		fetch(url, options),
		new Promise<Response>((_, reject) =>
			setTimeout(() => reject(new Error('Request timeout')), timeout)
		),
	]);
}

export async function apiFetch<T>(
	endpoint: string,
	options: RequestInit = {}
): Promise<T> {
	const url = `${API_CONFIG.baseURL}${endpoint}`;

	const config: RequestInit = {
		...options,
		headers: {
			...API_CONFIG.headers,
			...options.headers,
		},
	};

	try {
		const response = await fetchWithTimeout(url, config, 10000);

		if (!response.ok) {
			const error = await response.json().catch(() => ({
				message: response.statusText,
			}));
			throw new Error(error.message || `HTTP ${response.status}`);
		}

		return await response.json();
	} catch (error) {
		console.error('API Error:', error);
		throw error;
	}
}


export const api = {
	get: <T>(endpoint: string, options?: RequestInit) =>
		apiFetch<T>(endpoint, { ...options, method: 'GET' }),

	post: <T>(endpoint: string, data?: unknown, options?: RequestInit) =>
		apiFetch<T>(endpoint, {
			...options,
			method: 'POST',
			body: JSON.stringify(data),
		}),

	put: <T>(endpoint: string, data?: unknown, options?: RequestInit) =>
		apiFetch<T>(endpoint, {
			...options,
			method: 'PUT',
			body: JSON.stringify(data),
		}),

	delete: <T>(endpoint: string, options?: RequestInit) =>
		apiFetch<T>(endpoint, { ...options, method: 'DELETE' }),

	patch: <T>(endpoint: string, data?: unknown, options?: RequestInit) =>
		apiFetch<T>(endpoint, {
			...options,
			method: 'PATCH',
			body: JSON.stringify(data),
		}),
};
