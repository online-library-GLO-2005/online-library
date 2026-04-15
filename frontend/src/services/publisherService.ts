import api from "./api";
import type {Publisher} from "../types/publisher";
import type {ApiSuccess} from "../types/api";

export async function getPublishers(): Promise<Publisher[]> {
    const response = await api.get("/publishers");
    return response.data.data;
}

export async function getPublishersById(id:number): Promise<Publisher> {
    const response = await api.get(`/publishers/${id}`);
    return response.data.data;
}

export async function createPublisher(data:Publisher): Promise<ApiSuccess> {
    const response = await api.post("/publishers", data);
    return response.data;
}

export async function updatePublisher(id:number, data:Partial<Publisher>): Promise<ApiSuccess> {
    const response = await api.put(`/publishers/${id}`, data);
    return response.data;
}

export async function deletePublisher(id:number): Promise<ApiSuccess> {
    const response = await api.delete(`/publishers/${id}`);
    return response.data;
}