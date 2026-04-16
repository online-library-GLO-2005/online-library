import api from "./api";
import type { Genre } from "../types/genre";
import type { Book } from "../types/book";
import type {ApiSuccess} from "../types/api";

export async function getGenres():Promise<Genre[]> {
    const response = await api.get("/genres");
    return response.data.data;
}

export async function getGenreById(id:number):Promise<Genre> {
    const response = await api.get(`/genres/${id}`);
    return response.data.data;
}

export async function getBooksByGenre(id:number): Promise<Book[]> {
    const response = await api.get(`/genres/${id}/books`);
    return response.data.data;
}

export async function createGenre(data:Genre):Promise<ApiSuccess> {
    const response = await api.post("/genres", data);
    return response.data;
}

export async function updateGenre(id:number, data:Partial<Genre>): Promise<ApiSuccess> {
    const response = await api.put(`/genres/${id}`, data);
    return response.data;
}

export async function deleteGenre(id:number): Promise<ApiSuccess> {
    const response = await api.delete(`/genres/${id}`);
    return response.data;
}