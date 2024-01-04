export const URLs = {
    BROWSER: '/',
    FILES: '/files',
};

export type URLValue = (typeof URLs)[keyof typeof URLs];