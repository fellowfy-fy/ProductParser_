/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { StatusProduct } from './StatusProduct';

export type PaginatedStatusProductList = {
    count?: number;
    next?: string | null;
    previous?: string | null;
    results?: Array<StatusProduct>;
};
