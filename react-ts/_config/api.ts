// Set here api base urls from environment variables
export const API_URL = import.meta.env.VITE_API_URL;

// Set here api prefix paths if they are defined in environment variables
export const API_URL_PREFIX_PATH = import.meta.env.VITE_API_URL_PREFIX;

// Construct full API host URLs to use in api calls
export const MAIN_API_HOST = `${API_URL}${API_URL_PREFIX_PATH}`;
