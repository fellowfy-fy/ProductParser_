/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CustomUser } from '../models/CustomUser';
import type { PaginatedCustomUserList } from '../models/PaginatedCustomUserList';
import type { PatchedCustomUser } from '../models/PatchedCustomUser';
import type { StatusOk } from '../models/StatusOk';
import type { UserSetPassword } from '../models/UserSetPassword';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class UsersService {

    /**
     * @returns PaginatedCustomUserList 
     * @throws ApiError
     */
    public static usersList({
isActive,
ordering,
page,
pageSize,
role,
search,
}: {
isActive?: boolean,
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
 * * `1` - Сотрудник
 * * `2` - Руководитель
 * * `3` - Администратор
 */
role?: 1 | 2 | 3,
/**
 * A search term.
 */
search?: string,
}): CancelablePromise<PaginatedCustomUserList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/users/',
            query: {
                'is_active': isActive,
                'ordering': ordering,
                'page': page,
                'page_size': pageSize,
                'role': role,
                'search': search,
            },
        });
    }

    /**
     * @returns CustomUser 
     * @throws ApiError
     */
    public static usersCreate({
requestBody,
}: {
requestBody: CustomUser,
}): CancelablePromise<CustomUser> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/users/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }

    /**
     * @returns CustomUser 
     * @throws ApiError
     */
    public static usersRetrieve({
id,
}: {
/**
 * A unique integer value identifying this пользователь.
 */
id: number,
}): CancelablePromise<CustomUser> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/users/{id}/',
            path: {
                'id': id,
            },
        });
    }

    /**
     * @returns CustomUser 
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
requestBody: CustomUser,
}): CancelablePromise<CustomUser> {
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
     * @returns CustomUser 
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
requestBody?: PatchedCustomUser,
}): CancelablePromise<CustomUser> {
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
     * @returns StatusOk 
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
requestBody: UserSetPassword,
}): CancelablePromise<StatusOk> {
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
