/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Category } from '../models/Category';
import type { PaginatedCategoryList } from '../models/PaginatedCategoryList';
import type { PatchedCategory } from '../models/PatchedCategory';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class CategoryService {

    /**
     * @returns PaginatedCategoryList 
     * @throws ApiError
     */
    public static categoryList({
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
}): CancelablePromise<PaginatedCategoryList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/category/',
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
    public static categoryCreate({
formData,
}: {
formData: Category,
}): CancelablePromise<Category> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/category/',
            formData: formData,
            mediaType: 'application/x-www-form-urlencoded',
        });
    }

    /**
     * @returns Category 
     * @throws ApiError
     */
    public static categoryRetrieve({
id,
}: {
/**
 * A unique integer value identifying this Раздел.
 */
id: number,
}): CancelablePromise<Category> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/category/{id}/',
            path: {
                'id': id,
            },
        });
    }

    /**
     * @returns Category 
     * @throws ApiError
     */
    public static categoryUpdate({
id,
formData,
}: {
/**
 * A unique integer value identifying this Раздел.
 */
id: number,
formData: Category,
}): CancelablePromise<Category> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/v1/category/{id}/',
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
    public static categoryPartialUpdate({
id,
formData,
}: {
/**
 * A unique integer value identifying this Раздел.
 */
id: number,
formData?: PatchedCategory,
}): CancelablePromise<Category> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/v1/category/{id}/',
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
    public static categoryDestroy({
id,
}: {
/**
 * A unique integer value identifying this Раздел.
 */
id: number,
}): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/v1/category/{id}/',
            path: {
                'id': id,
            },
        });
    }

}
