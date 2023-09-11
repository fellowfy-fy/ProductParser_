/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { PaginatedProductList } from '../models/PaginatedProductList';
import type { PatchedProduct } from '../models/PatchedProduct';
import type { Product } from '../models/Product';
import type { StatusOkCount } from '../models/StatusOkCount';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class ProductService {

    /**
     * @returns PaginatedProductList 
     * @throws ApiError
     */
    public static productList({
ordering,
page,
pageSize,
search,
}: {
/**
 * Which field to use when ordering the results.
 */
ordering?: string,
/**
 * A page number within the paginated result set.
 */
page?: number,
/**
 * Number of results to return per page.
 */
pageSize?: number,
/**
 * A search term.
 */
search?: string,
}): CancelablePromise<PaginatedProductList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/product/',
            query: {
                'ordering': ordering,
                'page': page,
                'page_size': pageSize,
                'search': search,
            },
        });
    }

    /**
     * @returns Product 
     * @throws ApiError
     */
    public static productCreate({
requestBody,
}: {
requestBody: Product,
}): CancelablePromise<Product> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/product/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }

    /**
     * @returns Product 
     * @throws ApiError
     */
    public static productRetrieve({
id,
}: {
/**
 * A unique integer value identifying this Товар.
 */
id: number,
}): CancelablePromise<Product> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/product/{id}/',
            path: {
                'id': id,
            },
        });
    }

    /**
     * @returns Product 
     * @throws ApiError
     */
    public static productUpdate({
id,
requestBody,
}: {
/**
 * A unique integer value identifying this Товар.
 */
id: number,
requestBody: Product,
}): CancelablePromise<Product> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/v1/product/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }

    /**
     * @returns Product 
     * @throws ApiError
     */
    public static productPartialUpdate({
id,
requestBody,
}: {
/**
 * A unique integer value identifying this Товар.
 */
id: number,
requestBody?: PatchedProduct,
}): CancelablePromise<Product> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/v1/product/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }

    /**
     * @returns void 
     * @throws ApiError
     */
    public static productDestroy({
id,
}: {
/**
 * A unique integer value identifying this Товар.
 */
id: number,
}): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/v1/product/{id}/',
            path: {
                'id': id,
            },
        });
    }

    /**
     * @returns StatusOkCount 
     * @throws ApiError
     */
    public static productImportProductsCreate({
formData,
}: {
formData?: {
file?: Blob;
},
}): CancelablePromise<StatusOkCount> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/product/import_products/',
            formData: formData,
            mediaType: 'multipart/form-data',
        });
    }

}
