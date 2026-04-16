import { create } from 'zustand';
import type { User } from '../types/user';
interface AuthState {
  accessToken: string | null;
  name: string | null;
  email: string | null;
  is_admin: boolean;
  id: number | null;
  setToken: (token: string) => void;
  setUser: (user: User) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>()((set) => ({
  accessToken: null,
  name: null,
  is_admin: false,
  email: null,
  id: null,
  setToken: (token: string) => set({ accessToken: token }),
  setUser: (user: User) =>
    set({
      name: user.name,
      email: user.email,
      is_admin: user.is_admin,
      id: user.id,
    }),
  logout: () =>
    set({ accessToken: null, name: null, email: null, is_admin: false }),
}));
