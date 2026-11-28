import axios from 'axios';
import { ENV } from '../config/env';

let currentAccessToken: string | null = null;
let unauthorizedHandler: (() => void) | null = null;

export function setHttpAccessToken(token: string | null): void {
  currentAccessToken = token;
}

export function setUnauthorizedHandler(handler: (() => void) | null): void {
  unauthorizedHandler = handler;
}

export const httpClient = axios.create({
  baseURL: ENV.API_BASE_URL,
  timeout: 8000,
  headers: {
    'Content-Type': 'application/json',
  },
});

httpClient.interceptors.request.use((config) => {
  if (currentAccessToken) {
    config.headers.Authorization = `Bearer ${currentAccessToken}`;
  }
  return config;
});

httpClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (axios.isAxiosError(error) && error.response?.status === 401) {
      const requestUrl = error.config?.url ?? '';
      if (!requestUrl.includes('/auth/login') && unauthorizedHandler) {
        unauthorizedHandler();
      }
    }
    return Promise.reject(error);
  },
);
