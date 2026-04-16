import type { ApiSuccess } from '../types/api';

// This neglects the possibility of the API returning a success: false with an error message,
// but for simplicity we assume all responses are successful if they reach this point.
export function unwrap<T>(response: { data: ApiSuccess }): T {
  return response.data.data as T;
}
