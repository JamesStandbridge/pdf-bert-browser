/**
 * A utility object providing predefined HTTP headers for various request methods.
 *
 * The `headerBuilder` contains headers specifically designed for different HTTP request
 * methods, namely POST, GET, PATCH, and DELETE. Each set of headers is associated
 * with a key representing its request method.
 *
 * These headers primarily define the Content-Type for the requests to indicate that
 * the body contains JSON. Additionally, each set specifies the HTTP method, which
 * can be useful for certain server configurations or middlewares that rely on explicit
 * method declarations in the headers.
 *
 * Example Usage:
 * ```typescript
 * const myPostHeaders = headerBuilder.POST_HEADER;
 * const myGetHeaders = headerBuilder.GET_HEADER;
 * ```
 *
 * @const
 * @type {object}
 * @property {object} POST_HEADER - Headers for POST requests.
 * @property {object} GET_HEADER - Headers for GET requests.
 * @property {object} PATCH_HEADER - Headers for PATCH requests.
 * @property {object} DELETE_HEADER - Headers for DELETE requests.
 */
export const headerBuilder = {
    POST_HEADER: {
        'Content-type': 'application/json',
        method: 'POST',
    },

    GET_HEADER: {
        'Content-type': 'application/json',
        method: 'GET',
    },

    PATCH_HEADER: {
        'Content-type': 'application/json',
        method: 'PATCH',
    },

    DELETE_HEADER: {
        'Content-type': 'application/json',
        method: 'DELETE',
    },
};
