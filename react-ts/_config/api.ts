const apiUrl = import.meta.env.VITE_API_URL;
const apiPrefix = import.meta.env.VITE_API_PREFIX;
const isProd = import.meta.env.VITE_IS_PROD;

export const API_URL = apiUrl;
export const API_PREFIX_PATH = apiPrefix ?? '';
export const DEV_API_HOST = `http://${API_URL}${API_PREFIX_PATH}`;
export const PROD_API_HOST = `https://${API_URL}${API_PREFIX_PATH}`;

export const MAIN_API_HOST = isProd ? PROD_API_HOST : DEV_API_HOST;
