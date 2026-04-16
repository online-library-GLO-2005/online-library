import api from "./api";

export async function uploadBook(file:File, lid?:number): Promise<string> {
    const formData = new FormData();
    formData.append("file", file);
    if (lid) {
        formData.append("book_id", lid);
    }

    const response = await api.post("/media/books", formData, {
        headers: {"Content-Type": "multipart/form-data"}
    });
    return response.data.data;
}

export async function uploadCover(file:File, lid?:number): Promise<string> {
    const formData = new FormData();
    formData.append("file", file);
    if (lid) {
        formData.append("book_id", lid);
    }

    const response = await api.post("/media/covers", formData, {
        headers: {"Content-Type": "multipart/form-data"}
    });
    return response.data.data;
}

