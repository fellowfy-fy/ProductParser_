/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { GlobalPreference } from './GlobalPreference';

export type PaginatedGlobalPreferenceList = {
    count?: number;
    next?: string | null;
    previous?: string | null;
    results?: Array<GlobalPreference>;
};
