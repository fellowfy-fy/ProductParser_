/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { PaginatedProductPriceHistoryList } from '../models/PaginatedProductPriceHistoryList';
import type { PatchedProductPriceHistory } from '../models/PatchedProductPriceHistory';
import type { ProductPriceHistory } from '../models/ProductPriceHistory';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class ProductPriceService {

    /**
     * @returns PaginatedProductPriceHistoryList 
     * @throws ApiError
     */
    public static productPriceList({
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
}): CancelablePromise<PaginatedProductPriceHistoryList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/product_price/',
            query: {
                'ordering': ordering,
                'page': page,
                'page_size': pageSize,
                'search': search,
            },
        });
    }

    /**
     * @returns ProductPriceHistory 
     * @throws ApiError
     */
    public static productPriceCreate({
requestBody,
}: {
requestBody: ProductPriceHistory,
}): CancelablePromise<ProductPriceHistory> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/product_price/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }

    /**
     * @returns ProductPriceHistory 
     * @throws ApiError
     */
    public static productPriceRetrieve({
id,
}: {
/**
 * A unique integer value identifying this История цен.
 */
id: number,
}): CancelablePromise<ProductPriceHistory> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/product_price/{id}/',
            path: {
                'id': id,
            },
        });
    }

    /**
     * @returns ProductPriceHistory 
     * @throws ApiError
     */
    public static productPriceUpdate({
id,
requestBody,
}: {
/**
 * A unique integer value identifying this История цен.
 */
id: number,
requestBody: ProductPriceHistory,
}): CancelablePromise<ProductPriceHistory> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/v1/product_price/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }

    /**
     * @returns ProductPriceHistory 
     * @throws ApiError
     */
    public static productPricePartialUpdate({
id,
requestBody,
}: {
/**
 * A unique integer value identifying this История цен.
 */
id: number,
requestBody?: PatchedProductPriceHistory,
}): CancelablePromise<ProductPriceHistory> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/v1/product_price/{id}/',
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
    public static productPriceDestroy({
id,
}: {
/**
 * A unique integer value identifying this История цен.
 */
id: number,
}): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/v1/product_price/{id}/',
            path: {
                'id': id,
            },
        });
    }

}
