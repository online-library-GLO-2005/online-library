import api from "./api";
import type {Author} from "../types/author";
import type {ApiSuccess} from "../types/api";

export async function getAuthors(): Promise<Author[]> {
    const response = await api.get("/authors");
    return response.data.data;
}

export async function getAuthorsById(id:number): Promise<Author> {
    const response = await api.get(`/authors/${id}`);
    return response.data.data;
}

export async function createAuthor(data:Author): Promise<ApiSuccess> {
    const response = await api.post("/authors", data);
    return response.data;
}

export async function updateAuthor(id:number, data:Partial<Author>): Promise<ApiSuccess> {
    const response = await api.put(`/authors/${id}`, data);
    return response.data;
}

export async function deleteAuthor(id:number): Promise<ApiSuccess> {
    const response = await api.delete(`/authors/${id}`);
    return response.data;
}