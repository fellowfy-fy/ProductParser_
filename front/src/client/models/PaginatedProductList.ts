/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Product } from './Product';

export type PaginatedProductList = {
    count?: number;
    next?: string | null;
    previous?: string | null;
    results?: Array<Product>;
};
