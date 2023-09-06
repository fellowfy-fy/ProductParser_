/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { PaginatedParseTaskList } from '../models/PaginatedParseTaskList';
import type { ParseTask } from '../models/ParseTask';
import type { PatchedParseTask } from '../models/PatchedParseTask';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class ParseTaskService {

    /**
     * @returns PaginatedParseTaskList 
     * @throws ApiError
     */
    public static parseTaskList({
ordering,
page,
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
 * A search term.
 */
search?: string,
}): CancelablePromise<PaginatedParseTaskList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/parse_task/',
            query: {
                'ordering': ordering,
                'page': page,
                'search': search,
            },
        });
    }

    /**
     * @returns ParseTask 
     * @throws ApiError
     */
    public static parseTaskCreate({
requestBody,
}: {
requestBody: ParseTask,
}): CancelablePromise<ParseTask> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/parse_task/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }

    /**
     * @returns ParseTask 
     * @throws ApiError
     */
    public static parseTaskRetrieve({
id,
}: {
/**
 * A unique integer value identifying this Задача парсера.
 */
id: number,
}): CancelablePromise<ParseTask> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/parse_task/{id}/',
            path: {
                'id': id,
            },
        });
    }

    /**
     * @returns ParseTask 
     * @throws ApiError
     */
    public static parseTaskUpdate({
id,
requestBody,
}: {
/**
 * A unique integer value identifying this Задача парсера.
 */
id: number,
requestBody: ParseTask,
}): CancelablePromise<ParseTask> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/v1/parse_task/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }

    /**
     * @returns ParseTask 
     * @throws ApiError
     */
    public static parseTaskPartialUpdate({
id,
requestBody,
}: {
/**
 * A unique integer value identifying this Задача парсера.
 */
id: number,
requestBody?: PatchedParseTask,
}): CancelablePromise<ParseTask> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/v1/parse_task/{id}/',
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
    public static parseTaskDestroy({
id,
}: {
/**
 * A unique integer value identifying this Задача парсера.
 */
id: number,
}): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/v1/parse_task/{id}/',
            path: {
                'id': id,
            },
        });
    }

}
