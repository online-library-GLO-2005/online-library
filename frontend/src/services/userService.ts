import api from "./api";
import type { User } from "../types/user"
import type { Book } from "../types/book"
import type { Comment } from "../types/comment";
import type { ApiSuccess } from "../types/api";

export async function getUsers(): Promise<User[]> {
    const response = await api.get("/users");
    return response.data.data;
}

export async function getUserById(id:number): Promise<User> {
    const response = await api.get(`/users/${id}`);
    return response.data.data;
}

export async function getCurrentUser(): Promise<User> {
    const response = await api.get("/users/me");
    return response.data.data;
}

export async function getCurrentUserComments(): Promise<Comment[]> {
    const response = await api.get("/users/me/comments");
    return response.data.data;
}

export async function getCurrentUserBookList(): Promise<Book[]> {
    const response = await api.get("/users/me/books");
    return response.data.data;
}

export async function saveToCurrentUserBookList(id:number): Promise<ApiSuccess> {
    const response = await api.post("/users/me/books",{
        book_id: id
    });
    return response.data;
}

export async function deleteFromCurrentUserBookList(id:number): Promise<ApiSuccess> {
    const response = await api.delete(`/users/me/books/${id}`);
    return response.data;
}

export async function updateUser(id:number, data:Partial<User>): Promise<ApiSuccess> {
    const response = await api.put(`/users/${id}`, data);
    return response.data;
}

export async function deleteUser(id:number): Promise<ApiSuccess> {
    const response = await api.delete(`/users/${id}`);
    return response.data
}