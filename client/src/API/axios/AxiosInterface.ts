import { AxiosResponse } from 'axios';

/**
 * `AxiosInterface` provides a clear contract for an HTTP client based on Axios.
 *
 * The methods defined in this interface correspond to HTTP methods like GET, POST, DELETE, and PATCH.
 * Each method returns a Promise which resolves with an AxiosResponse, providing flexibility to type the request body and the expected response.
 */
export interface AxiosInterface {
    /**
     * Sends a POST request to the specified URL with an optional request body.
     *
     * @template T Type of the request body. Defaults to `any`.
     * @template R Type of the expected response. Defaults to `any`.
     * @param url The endpoint to which the request will be sent.
     * @param body Optional request body.
     * @returns Promise resolving with an AxiosResponse containing the expected response type.
     */
    post<T = any, R = any>(
        url: string,
        body?: T,
        headers?: any,
    ): Promise<AxiosResponse<R>>;

    /**
     * Sends a GET request to the specified URL.
     *
     * @template R Type of the expected response. Defaults to `any`.
     * @param url The endpoint from which data will be fetched.
     * @returns Promise resolving with an AxiosResponse containing the expected response type.
     */
    get<R = any>(url: string): Promise<AxiosResponse<R>>;

    /**
     * Sends a DELETE request to the specified URL with an optional request body.
     *
     * @template T Type of the request body or params. Defaults to `any`.
     * @template R Type of the expected response. Defaults to `any`.
     * @param url The endpoint to which the delete request will be sent.
     * @param data Optional request body or params.
     * @returns Promise resolving with an AxiosResponse containing the expected response type.
     */
    delete<T = any, R = any>(url: string, data?: T): Promise<AxiosResponse<R>>;

    /**
     * Sends a PATCH request to the specified URL with an optional request body.
     *
     * @template T Type of the request body. Defaults to `any`.
     * @template R Type of the expected response. Defaults to `any`.
     * @param url The endpoint to which the request will be sent.
     * @param body Optional request body.
     * @returns Promise resolving with an AxiosResponse containing the expected response type.
     */
    patch<T = any, R = any>(url: string, body?: T): Promise<AxiosResponse<R>>;
}
