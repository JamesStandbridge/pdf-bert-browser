const apiUrl = import.meta.env.VITE_API_DOMAIN;

export const endpoints = {
    POST_UPLOAD_PDF: () => `${apiUrl}/upload-pdf`,
    POST_SEARCH: () => `${apiUrl}/search`,
    GET_ALL_FILENAMES: () => `${apiUrl}/get-all-pdf`,
    RESET_FILES: () => `${apiUrl}/reset-files`,
};
