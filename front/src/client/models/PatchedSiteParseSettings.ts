/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ParseModeEnum } from './ParseModeEnum';
import type { RequestMethodEnum } from './RequestMethodEnum';

export type PatchedSiteParseSettings = {
    readonly id?: number;
    url?: string;
    url_match?: string | null;
    parse_mode?: ParseModeEnum;
    request_method?: RequestMethodEnum;
    request_headers?: Record<string, any> | null;
    request_data?: Record<string, any> | null;
    path_title?: string;
    path_price?: string;
    force_parser_url?: boolean;
    readonly domain?: string | null;
};
