/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { CustomUser } from './CustomUser';

export type PaginatedCustomUserList = {
    count?: number;
    next?: string | null;
    previous?: string | null;
    results?: Array<CustomUser>;
};
