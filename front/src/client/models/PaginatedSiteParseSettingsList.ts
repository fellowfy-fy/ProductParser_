/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { SiteParseSettings } from './SiteParseSettings';

export type PaginatedSiteParseSettingsList = {
    count?: number;
    next?: string | null;
    previous?: string | null;
    results?: Array<SiteParseSettings>;
};
