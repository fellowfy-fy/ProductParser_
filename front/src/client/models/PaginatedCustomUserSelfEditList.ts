/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { CustomUserSelfEdit } from './CustomUserSelfEdit';

export type PaginatedCustomUserSelfEditList = {
    count?: number;
    next?: string | null;
    previous?: string | null;
    results?: Array<CustomUserSelfEdit>;
};
