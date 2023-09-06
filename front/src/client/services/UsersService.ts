/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CustomUser } from '../models/CustomUser';
import type { CustomUserSelfEdit } from '../models/CustomUserSelfEdit';
import type { PaginatedCustomUserSelfEditList } from '../models/PaginatedCustomUserSelfEditList';
import type { PatchedCustomUserSelfEdit } from '../models/PatchedCustomUserSelfEdit';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class UsersService {

    /**
     * @returns PaginatedCustomUserSelfEditList 
     * @throws ApiError
     */
    public static usersList({
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
}): CancelablePromise<PaginatedCustomUserSelfEditList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/users/',
            query: {
                'ordering': ordering,
                'page': page,
                'page_size': pageSize,
                'search': search,
            },
        });
    }

    /**
     * @returns CustomUserSelfEdit 
     * @throws ApiError
     */
    public static usersCreate({
requestBody,
}: {
requestBody: CustomUserSelfEdit,
}): CancelablePromise<CustomUserSelfEdit> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/users/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }

    /**
     * @returns CustomUserSelfEdit 
     * @throws ApiError
     */
    public static usersRetrieve({
id,
}: {
/**
 * A unique integer value identifying this пользователь.
 */
id: number,
}): CancelablePromise<CustomUserSelfEdit> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/users/{id}/',
            path: {
                'id': id,
            },
        });
    }

    /**
     * @returns CustomUserSelfEdit 
     * @throws ApiError
     */
    public static usersUpdate({
id,
requestBody,
}: {
/**
 * A unique integer value identifying this пользователь.
 */
id: number,
requestBody: CustomUserSelfEdit,
}): CancelablePromise<CustomUserSelfEdit> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/v1/users/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }

    /**
     * @returns CustomUserSelfEdit 
     * @throws ApiError
     */
    public static usersPartialUpdate({
id,
requestBody,
}: {
/**
 * A unique integer value identifying this пользователь.
 */
id: number,
requestBody?: PatchedCustomUserSelfEdit,
}): CancelablePromise<CustomUserSelfEdit> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/v1/users/{id}/',
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
    public static usersDestroy({
id,
}: {
/**
 * A unique integer value identifying this пользователь.
 */
id: number,
}): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/v1/users/{id}/',
            path: {
                'id': id,
            },
        });
    }

    /**
     * @returns CustomUserSelfEdit 
     * @throws ApiError
     */
    public static usersSetPasswordCreate({
id,
requestBody,
}: {
/**
 * A unique integer value identifying this пользователь.
 */
id: number,
requestBody: CustomUserSelfEdit,
}): CancelablePromise<CustomUserSelfEdit> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/users/{id}/set_password/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }

    /**
     * @returns CustomUser 
     * @throws ApiError
     */
    public static usersCurrentRetrieve(): CancelablePromise<CustomUser> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/users/current/',
        });
    }

}
