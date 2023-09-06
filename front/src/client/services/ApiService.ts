/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class ApiService {

    /**
     * OpenApi3 schema for this API. Format can be selected via content negotiation.
 *
 * - YAML: application/vnd.oai.openapi
 * - JSON: application/vnd.oai.openapi+json
     * @returns any 
     * @throws ApiError
     */
    public static apiSchemaRetrieve({
format,
lang,
}: {
format?: 'json' | 'yaml',
lang?: 'en' | 'ru',
}): CancelablePromise<Record<string, any>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/schema/',
            query: {
                'format': format,
                'lang': lang,
            },
        });
    }

}
