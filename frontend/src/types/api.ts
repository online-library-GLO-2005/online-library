export type ApiSuccess = {
    success: true;
    data?: unknown;
    message?: string;
}

export type ApiError = {
    success: false;
    error: string | object;
}