import axios from 'axios';
import { ENV } from '../config/env';

export const httpClient = axios.create({
  baseURL: ENV.API_BASE_URL,
  timeout: 8000,
  headers: {
    'Content-Type': 'application/json',
  },
});
