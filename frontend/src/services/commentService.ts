import api from "./api";
import type { ApiSuccess } from "../types/api";
import type { Comment } from "../types/comment";

export async function modifyComment(id:number, data:Partial<Comment>): Promise<ApiSuccess> {
    const response = await api.put(`/comments/${id}`, data);
    return response.data;
}

export async function deleteComment(id:number): Promise<ApiSuccess> {
    const response = await api.delete(`/comments/${id}`);
    return response.data;
}