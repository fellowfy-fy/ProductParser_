/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { PaginatedSiteParseSettingsList } from '../models/PaginatedSiteParseSettingsList';
import type { PatchedSiteParseSettings } from '../models/PatchedSiteParseSettings';
import type { SiteParseSettings } from '../models/SiteParseSettings';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class ParseSettingsService {

    /**
     * @returns PaginatedSiteParseSettingsList 
     * @throws ApiError
     */
    public static parseSettingsList({
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
}): CancelablePromise<PaginatedSiteParseSettingsList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/parse_settings/',
            query: {
                'ordering': ordering,
                'page': page,
                'page_size': pageSize,
                'search': search,
            },
        });
    }

    /**
     * @returns SiteParseSettings 
     * @throws ApiError
     */
    public static parseSettingsCreate({
requestBody,
}: {
requestBody: SiteParseSettings,
}): CancelablePromise<SiteParseSettings> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/parse_settings/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }

    /**
     * @returns SiteParseSettings 
     * @throws ApiError
     */
    public static parseSettingsRetrieve({
id,
}: {
/**
 * A unique integer value identifying this Настройки парсинга сайта.
 */
id: number,
}): CancelablePromise<SiteParseSettings> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/parse_settings/{id}/',
            path: {
                'id': id,
            },
        });
    }

    /**
     * @returns SiteParseSettings 
     * @throws ApiError
     */
    public static parseSettingsUpdate({
id,
requestBody,
}: {
/**
 * A unique integer value identifying this Настройки парсинга сайта.
 */
id: number,
requestBody: SiteParseSettings,
}): CancelablePromise<SiteParseSettings> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/v1/parse_settings/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }

    /**
     * @returns SiteParseSettings 
     * @throws ApiError
     */
    public static parseSettingsPartialUpdate({
id,
requestBody,
}: {
/**
 * A unique integer value identifying this Настройки парсинга сайта.
 */
id: number,
requestBody?: PatchedSiteParseSettings,
}): CancelablePromise<SiteParseSettings> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/v1/parse_settings/{id}/',
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
    public static parseSettingsDestroy({
id,
}: {
/**
 * A unique integer value identifying this Настройки парсинга сайта.
 */
id: number,
}): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/v1/parse_settings/{id}/',
            path: {
                'id': id,
            },
        });
    }

}
