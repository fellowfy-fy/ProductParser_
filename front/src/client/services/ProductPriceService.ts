/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { PaginatedProductPriceHistoryFullList } from '../models/PaginatedProductPriceHistoryFullList';
import type { ProductPriceHistoryFull } from '../models/ProductPriceHistoryFull';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class ProductPriceService {

    /**
     * @returns PaginatedProductPriceHistoryFullList 
     * @throws ApiError
     */
    public static productPriceList({
ordering,
page,
pageSize,
parseSettings,
product,
search,
task,
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
parseSettings?: number,
product?: number,
/**
 * A search term.
 */
search?: string,
task?: number,
}): CancelablePromise<PaginatedProductPriceHistoryFullList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/product_price/',
            query: {
                'ordering': ordering,
                'page': page,
                'page_size': pageSize,
                'parse_settings': parseSettings,
                'product': product,
                'search': search,
                'task': task,
            },
        });
    }

    /**
     * @returns ProductPriceHistoryFull 
     * @throws ApiError
     */
    public static productPriceRetrieve({
id,
}: {
/**
 * A unique integer value identifying this История цен.
 */
id: number,
}): CancelablePromise<ProductPriceHistoryFull> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/product_price/{id}/',
            path: {
                'id': id,
            },
        });
    }

}
