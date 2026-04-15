import axios from "axios"

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL,
    headers: {
        "Content-Type": "application/json"
    }
})

api.interceptors.request.use((config) => {
    const token = null;

    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }

    return config
});

api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            console.error("Demande non autorisée, redirection vers page de connection...")
        }
        return Promise.reject(error);
    });

export default api;