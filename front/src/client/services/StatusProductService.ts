/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { StatusProduct } from '../models/StatusProduct';
import type { PaginatedProductList } from '../models/PaginatedProductList';
import type { PatchedStatusProduct } from '../models/PatchedStatusProduct';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class StatusProductService {

    /**
     * @returns PaginatedStatusProductList 
     * @throws ApiError
     */
    public static statusproductList({
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
            url: '/api/v1/statusproduct/',
            query: {
                'ordering': ordering,
                'page': page,
                'page_size': pageSize,
                'search': search,
            },
        });
    }

    /**
     * @returns Category 
     * @throws ApiError
     */
    public static statusproductCreate({
formData,
}: {
formData: StatusProduct,
}): CancelablePromise<StatusProduct> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/statusproduct/',
            formData: formData,
            mediaType: 'application/x-www-form-urlencoded',
        });
    }

    /**
     * @returns Category 
     * @throws ApiError
     */
    public static statusproductRetrieve({
id,
}: {
/**
 * A unique integer value identifying this Раздел.
 */
id: number,
}): CancelablePromise<StatusProduct> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/statusproduct/{id}/',
            path: {
                'id': id,
            },
        });
    }

    /**
     * @returns Category 
     * @throws ApiError
     */
    public static statusproductUpdate({
id,
formData,
}: {
/**
 * A unique integer value identifying this Раздел.
 */
id: number,
formData: StatusProduct,
}): CancelablePromise<StatusProduct> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/v1/statusproduct/{id}/',
            path: {
                'id': id,
            },
            formData: formData,
            mediaType: 'application/x-www-form-urlencoded',
        });
    }

    /**
     * @returns Category 
     * @throws ApiError
     */
    public static statusproductPartialUpdate({
id,
formData,
}: {
/**
 * A unique integer value identifying this Раздел.
 */
id: number,
formData?: PatchedStatusProduct,
}): CancelablePromise<StatusProduct> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/v1/statusproduct/{id}/',
            path: {
                'id': id,
            },
            formData: formData,
            mediaType: 'application/x-www-form-urlencoded',
        });
    }

    /**
     * @returns void 
     * @throws ApiError
     */
    public static statusproductDestroy({
id,
}: {
/**
 * A unique integer value identifying this Раздел.
 */
id: number,
}): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/v1/statusproduct/{id}/',
            path: {
                'id': id,
            },
        });
    }

}
