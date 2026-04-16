import api from './api';
import type { User } from '../types/user';
import type { Book } from '../types/book';
import type { Comment } from '../types/comment';
import type { ApiSuccess } from '../types/api';

// --- USERS ---

export async function getUsers(): Promise<User[]> {
  const response = await api.get('/users');
  return response.data.data;
}

// ❌ N'existe pas côté backend
// export async function getUserById(id:number): Promise<User> {
//     const response = await api.get(`/users/${id}`);
//     return response.data.data;
// }

export async function getCurrentUser(): Promise<User> {
  const response = await api.get('/users/me');
  return response.data.data;
}

export async function getCurrentUserComments(): Promise<Comment[]> {
  const response = await api.get('/users/me/comments');
  return response.data.data;
}

// --- BOOKS (HISTORIQUE) ---

export async function getCurrentUserBookList(): Promise<Book[]> {
  const response = await api.get('/users/me/books');
  return response.data.data;
}

// ❌ N'existe pas côté backend
// export async function saveToCurrentUserBookList(id:number): Promise<ApiSuccess> {
//     const response = await api.post("/users/me/books",{
//         book_id: id
//     });
//     return response.data;
// }

// ❌ N'existe pas côté backend
// export async function deleteFromCurrentUserBookList(id:number): Promise<ApiSuccess> {
//     const response = await api.delete(`/users/me/books/${id}`);
//     return response.data;
// }

// --- FAVORITES (EXISTE côté backend) ---

export async function getFavorites(): Promise<Book[]> {
  const response = await api.get('/users/me/favorites');
  return response.data.data;
}

export async function addFavorite(bookId: number): Promise<ApiSuccess> {
  const response = await api.post('/users/me/favorites', {
    book_id: bookId,
  });
  return response.data;
}

export async function removeFavorite(bookId: number): Promise<ApiSuccess> {
  const response = await api.delete(`/users/me/favorites/${bookId}`);
  return response.data;
}

// --- ADMIN / USERS ---

// ❌ N'existe pas côté backend
// export async function updateUser(id:number, data:Partial<User>): Promise<ApiSuccess> {
//     const response = await api.put(`/users/${id}`, data);
//     return response.data;
// }

// ❌ N'existe pas côté backend
// export async function deleteUser(id:number): Promise<ApiSuccess> {
//     const response = await api.delete(`/users/${id}`);
//     return response.data
// }
