import { create } from 'zustand';
import type { User } from '../types/user';
import type { Book } from '../types/book';

interface AuthState {
  accessToken: string | null;
  name: string | null;
  email: string | null;
  is_admin: boolean;
  id: number | null;
  authReady: boolean;
  favorites: Book[];

  setAuthReady: (v: boolean) => void;

  setToken: (token: string) => void;
  setUser: (user: User) => void;

  setFavorites: (books: Book[]) => void;
  addFavorite: (book: Book) => void;
  removeFavorite: (bookId: number) => void;

  logout: () => void;
}

export const useAuthStore = create<AuthState>()((set, get) => ({
  accessToken: null,
  name: null,
  is_admin: false,
  email: null,
  id: null,
  authReady: false,

  favorites: [],

  setAuthReady: (v: boolean) => set({ authReady: v }),
  setToken: (token: string) => set({ accessToken: token }),

  setUser: (user: User) =>
    set({
      name: user.name,
      email: user.email,
      is_admin: user.is_admin,
      id: user.id,
    }),

  setFavorites: (books: Book[]) => set({ favorites: books }),

  addFavorite: (book: Book) => set({ favorites: [...get().favorites, book] }),

  removeFavorite: (bookId: number) =>
    set({
      favorites: get().favorites.filter((b) => b.id !== bookId),
    }),

  logout: () =>
    set({
      accessToken: null,
      name: null,
      email: null,
      is_admin: false,
      id: null,
      favorites: [],
    }),
}));
