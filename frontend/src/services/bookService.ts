import api from './api';
import type { Book } from '../types/book';
import type { Comment } from '../types/comment';
import type { ApiSuccess } from '../types/api';

export async function getBooks(): Promise<Book[]> {
  const response = await api.get('/books');
  return response.data.data;
}

export async function getBookById(id: number): Promise<Book> {
  const response = await api.get(`/books/${id}`);
  return response.data.data;
}

export async function getCommentsForBook(id: number): Promise<Comment[]> {
  const response = await api.get(`/books/${id}/comments`);
  return response.data.data;
}

export async function linkAuthorToBook(
  id: number,
  aid: number,
): Promise<ApiSuccess> {
  const response = await api.post(`/books/${id}/authors/${aid}`);
  return response.data;
}

export async function linkGenreToBook(
  id: number,
  gid: number,
): Promise<ApiSuccess> {
  const response = await api.post(`/books/${id}/genres/${gid}`);
  return response.data;
}

export async function postCommentToBook(
  id: number,
  message: string,
): Promise<ApiSuccess> {
  const response = await api.post(`/books/${id}/comments`, {
    message: message,
  });
  return response.data;
}

export async function rateBook(id:number, note:number): Promise<ApiSuccess> {
  const response = await api.post(`/books/${id}/ratings`, {note: note});
  return response.data;
}

export async function postBook(data: Book): Promise<ApiSuccess> {
  const response = await api.post(`/books`, data);
  return response.data;
}

export async function updateBook(
  id: number,
  data: Partial<Book>,
): Promise<ApiSuccess> {
  const response = await api.put(`/books/${id}`, data);
  return response.data;
}

export async function deleteBook(id: number): Promise<ApiSuccess> {
  const response = await api.delete(`/books/${id}`);
  return response.data;
}
