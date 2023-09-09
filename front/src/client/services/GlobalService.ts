/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { GlobalPreference } from '../models/GlobalPreference';
import type { PaginatedGlobalPreferenceList } from '../models/PaginatedGlobalPreferenceList';
import type { PatchedGlobalPreference } from '../models/PatchedGlobalPreference';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class GlobalService {

    /**
     * - list preferences
 * - detail given preference
 * - batch update preferences
 * - update a single preference
     * @returns PaginatedGlobalPreferenceList 
     * @throws ApiError
     */
    public static globalList({
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
}): CancelablePromise<PaginatedGlobalPreferenceList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/global/',
            query: {
                'ordering': ordering,
                'page': page,
                'page_size': pageSize,
                'search': search,
            },
        });
    }

    /**
     * - list preferences
 * - detail given preference
 * - batch update preferences
 * - update a single preference
     * @returns GlobalPreference 
     * @throws ApiError
     */
    public static globalRetrieve({
id,
}: {
id: string,
}): CancelablePromise<GlobalPreference> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/global/{id}/',
            path: {
                'id': id,
            },
        });
    }

    /**
     * - list preferences
 * - detail given preference
 * - batch update preferences
 * - update a single preference
     * @returns GlobalPreference 
     * @throws ApiError
     */
    public static globalUpdate({
id,
requestBody,
}: {
id: string,
requestBody: GlobalPreference,
}): CancelablePromise<GlobalPreference> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/v1/global/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }

    /**
     * - list preferences
 * - detail given preference
 * - batch update preferences
 * - update a single preference
     * @returns GlobalPreference 
     * @throws ApiError
     */
    public static globalPartialUpdate({
id,
requestBody,
}: {
id: string,
requestBody?: PatchedGlobalPreference,
}): CancelablePromise<GlobalPreference> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/v1/global/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }

    /**
     * Update multiple preferences at once
 *
 * this is a long method because we ensure everything is valid
 * before actually persisting the changes
     * @returns GlobalPreference 
     * @throws ApiError
     */
    public static globalBulkCreate({
requestBody,
}: {
requestBody: GlobalPreference,
}): CancelablePromise<GlobalPreference> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/global/bulk/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }

}
