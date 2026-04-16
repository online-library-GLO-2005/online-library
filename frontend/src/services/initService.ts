import { useAuthStore } from '../store/authStore';
import type { User } from '../types/user';
import { refreshRequest } from './authService';
import { getCurrentUser } from './userService';

export async function initAuth() {
  try {
    const res = await refreshRequest();
    useAuthStore.getState().setToken(res.access_token);

    console.log('token set:', useAuthStore.getState().accessToken); // ← add this

    const user: User = await getCurrentUser(); // GET /users/me with the new token
    useAuthStore.getState().setUser(user);
  } catch {
    useAuthStore.getState().logout();
  }
}
