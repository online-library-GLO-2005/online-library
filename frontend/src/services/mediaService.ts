import api from "./api";

export async function uploadBook(file:File): Promise<string> {
    const formData = new FormData();
    formData.append("file", file);

    const response = await api.post("/media/books", formData, {
        headers: {"Content-Type": "multipart/form-data"}
    });
    return response.data.data;
}

export async function uploadCover(file:File): Promise<string> {
    const formData = new FormData();
    formData.append("file", file);

    const response = await api.post("/media/covers", formData, {
        headers: {"Content-Type": "multipart/form-data"}
    });
    return response.data.data;
}

