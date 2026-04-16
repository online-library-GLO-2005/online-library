import api from './api';
import type { LoginData, SignupData, LoginResponse } from '../types/auth';
import type { ApiRefresh, ApiSuccess } from '../types/api';
import { unwrap } from '../utils/unwrap';
import { useAuthStore } from '../store/authStore';

export async function loginRequest(data: LoginData): Promise<LoginResponse> {
  const res = await api.post<ApiSuccess>('/auth/login', data);

  return unwrap<LoginResponse>(res);
}

export async function signupRequest(data: SignupData): Promise<LoginResponse> {
  const res = await api.post<ApiSuccess>('/auth/signup', data);

  return unwrap<LoginResponse>(res);
}

export async function logoutRequest(): Promise<void> {
  await api.post('/auth/logout');
}

export async function refreshRequest(): Promise<ApiRefresh> {
  const res = await api.post<ApiRefresh>('/auth/refresh');

  return res.data;
}

export async function initAuth() {
  try {
    const res = await refreshRequest(); // uses cookie

    useAuthStore.getState().setToken(res.access_token);

    // optional: fetch user profile here if needed
  } catch {
    useAuthStore.getState().logout();
  }
}
