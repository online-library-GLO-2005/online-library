import api from "./api";
import type { ApiSuccess } from "../types/api";
import type { SignupData, LoginData } from "../types/auth";

export async function login(data:LoginData): Promise<ApiSuccess> {
    const response = await api.post("/auth/login", data);
    return response.data;
}

export async function signup(data:SignupData): Promise<ApiSuccess> {
    const response = await api.post("/auth/signup", data)
    return response.data;
}

export async function logout(): Promise<ApiSuccess> {
    const response = await api.post("/auth/logout");
    return response.data;
}

export async function refresh(): Promise<ApiSuccess> {
    const response = await api.post("/auth/refresh");
    return response.data;
}