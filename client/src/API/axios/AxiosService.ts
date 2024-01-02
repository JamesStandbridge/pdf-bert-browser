import axios, { AxiosResponse } from 'axios';

import { AxiosInterface } from './AxiosInterface';
import { headerBuilder } from '../headerBuilder';

/**
 * `AxiosService` is an implementation of the `AxiosInterface`, providing a consistent
 * interface for making HTTP requests using Axios.
 *
 * It defines methods to make GET, POST, DELETE, and PATCH requests, and uses predefined
 * headers from `headerBuilder` for each request type.
 */
const AxiosService: AxiosInterface = {
    /**
     * Sends a POST request to the specified URL with the given request body.
     *
     * @template T Type of the request body. Defaults to `any`.
     * @template R Type of the expected AxiosResponse. Defaults to `AxiosResponse<T>`.
     * @param url The endpoint to which the request will be sent.
     * @param body Request body. Defaults to an empty object of type T.
     * @returns Promise resolving with an AxiosResponse of the specified type.
     */
    post: async function <T = any, R = AxiosResponse<T>>(
        url: string,
        body: T = {} as T,
        headers: any = headerBuilder.POST_HEADER,
    ): Promise<R> {
        const res = await axios.post<T, R>(url, body, {
            headers: headers,
        });
        return res;
    },

    /**
     * Sends a GET request to the specified URL.
     *
     * @template T Type for the expected AxiosResponse data. Defaults to `any`.
     * @template R Type of the expected AxiosResponse. Defaults to `AxiosResponse<T>`.
     * @param url The endpoint from which data will be fetched.
     * @returns Promise resolving with an AxiosResponse of the specified type.
     */
    get: async function <T = any, R = AxiosResponse<T>>(
        url: string,
    ): Promise<R> {
        const res = await axios.get<T, R>(url, {
            headers: headerBuilder.GET_HEADER,
        });
        return res;
    },

    /**
     * Sends a DELETE request to the specified URL with the provided data.
     *
     * @template T Type for the optional request body or params. Defaults to `any`.
     * @template R Type of the expected AxiosResponse. Defaults to `AxiosResponse<T>`.
     * @param url The endpoint to which the delete request will be sent.
     * @param data Optional data to be included in the request.
     * @returns Promise resolving with an AxiosResponse of the specified type.
     */
    delete: async function <T = any, R = AxiosResponse<T>>(
        url: string,
        data?: T,
    ): Promise<R> {
        const res = await axios.delete<T, R>(url, {
            headers: headerBuilder.DELETE_HEADER,
            data,
        });
        return res;
    },

    /**
     * Sends a PATCH request to the specified URL with the provided request body.
     *
     * @template T Type of the request body. Defaults to `any`.
     * @template R Type of the expected AxiosResponse. Defaults to `AxiosResponse<T>`.
     * @param url The endpoint to which the request will be sent.
     * @param body Request body.
     * @returns Promise resolving with an AxiosResponse of the specified type.
     */
    patch: async function <T = any, R = AxiosResponse<T>>(
        url: string,
        body?: T,
    ): Promise<R> {
        const res = await axios.patch<T, R>(url, body, {
            headers: headerBuilder.PATCH_HEADER,
        });
        return res;
    },
};

export default AxiosService;
