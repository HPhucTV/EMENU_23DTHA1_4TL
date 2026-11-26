export const ENV = {
  API_BASE_URL: (import.meta.env.VITE_API_BASE_URL as string | undefined)?.trim() || '',
  SWAGGER_URL:
    ((import.meta.env.VITE_API_BASE_URL as string | undefined)?.trim() || 'http://localhost:8000') +
    '/docs',
  TIMEZONE: 'Asia/Ho_Chi_Minh',
  CURRENCY: 'VND',
} as const;
