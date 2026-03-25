import axios from 'axios';

// In development, use Vite proxy (/api → localhost:8000).
// In production (Vercel), point directly to the Render backend.
// Use Vite proxy in local development:
// If the app is running in 'development' mode (e.g. via npm run dev), 
// it will always use the local proxy '/api' to avoid CORS issues and use local backend.
export const SERVER_URL = import.meta.env.DEV 
  ? 'http://localhost:8000' 
  : (import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000');

const BASE_URL = import.meta.env.DEV ? '/api' : (import.meta.env.VITE_API_BASE_URL ? `${import.meta.env.VITE_API_BASE_URL}/api` : '/api');

const api = axios.create({
  baseURL: BASE_URL,
  timeout: 300000, // 5 minutes
});

// Intercept requests to inject the JWT auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default api;
