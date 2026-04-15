import api from "./api";

export async function search(query:string): Promise<unknown> {
    const response = await api.get("/search", { params: {q:query}});
    return response.data.data;
}