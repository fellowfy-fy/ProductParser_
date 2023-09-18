/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ExportRequest } from '../models/ExportRequest';
import type { ExportResults } from '../models/ExportResults';
import type { PaginatedParseTaskList } from '../models/PaginatedParseTaskList';
import type { ParseTask } from '../models/ParseTask';
import type { PatchedParseTask } from '../models/PatchedParseTask';
import type { TaskChangeStatus } from '../models/TaskChangeStatus';
import type { TestRunResults } from '../models/TestRunResults';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class ParseTaskService {

    /**
     * @returns PaginatedParseTaskList 
     * @throws ApiError
     */
    public static parseTaskList({
author,
ordering,
page,
pageSize,
search,
status,
}: {
author?: number,
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
/**
 * * `1` - Создана
 * * `2` - В работе
 * * `3` - Отменена
 * * `4` - Пауза
 * * `5` - Остановлена
 * * `6` - Настройка
 * * `7` - Ошибка
 */
status?: 1 | 2 | 3 | 4 | 5 | 6 | 7,
}): CancelablePromise<PaginatedParseTaskList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/parse_task/',
            query: {
                'author': author,
                'ordering': ordering,
                'page': page,
                'page_size': pageSize,
                'search': search,
                'status': status,
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

    /**
     * @returns ParseTask 
     * @throws ApiError
     */
    public static parseTaskChangeStatusCreate({
id,
requestBody,
}: {
/**
 * A unique integer value identifying this Задача парсера.
 */
id: number,
requestBody: TaskChangeStatus,
}): CancelablePromise<ParseTask> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/parse_task/{id}/change_status/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }

    /**
     * @returns TestRunResults 
     * @throws ApiError
     */
    public static parseTaskTestCreate({
id,
test,
}: {
/**
 * A unique integer value identifying this Задача парсера.
 */
id: number,
test?: boolean,
}): CancelablePromise<TestRunResults> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/parse_task/{id}/test/',
            path: {
                'id': id,
            },
            query: {
                'test': test,
            },
        });
    }

    /**
     * @returns ExportResults 
     * @throws ApiError
     */
    public static parseTaskExportCreate({
requestBody,
}: {
requestBody: ExportRequest,
}): CancelablePromise<ExportResults> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/parse_task/export/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }

}
