/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ParseModeEnum } from './ParseModeEnum';
import type { RequestMethodEnum } from './RequestMethodEnum';

export type SiteParseSettings = {
    readonly id: number;
    url: string;
    url_match?: string | null;
    url_before?: string | null;
    match_regex?: string | null;
    parse_mode?: ParseModeEnum;
    request_method?: RequestMethodEnum;
    request_headers?: Record<string, any> | null;
    request_data?: Record<string, any> | null;
    path_title: string;
    path_price: string;
    attribute_title?: string | null;
    attribute_price?: string | null;
    force_parser_url?: boolean;
    use_selenium?: boolean;
    readonly domain: string | null;
};
