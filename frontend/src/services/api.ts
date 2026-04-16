import axios from 'axios';
import { useAuthStore } from '../store/authStore';
import { refreshRequest } from './authService';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().accessToken;

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

api.interceptors.response.use(
  (res) => res,
  async (error) => {
    const originalRequest = error.config;
    if (!originalRequest) return Promise.reject(error);

    const isAuthRoute = originalRequest.url?.startsWith('/auth');

    if (
      error.response?.status === 401 &&
      !originalRequest._retry &&
      !isAuthRoute
    ) {
      originalRequest._retry = true;

      const token = useAuthStore.getState().accessToken;
      if (!token) return Promise.reject(error);

      try {
        const res = await refreshRequest();

        useAuthStore.getState().setToken(res.access_token);

        originalRequest.headers.Authorization = `Bearer ${res.access_token}`;

        return api(originalRequest);
      } catch (err) {
        useAuthStore.getState().logout();
        return Promise.reject(err);
      }
    }

    return Promise.reject(error);
  },
);

export default api;
