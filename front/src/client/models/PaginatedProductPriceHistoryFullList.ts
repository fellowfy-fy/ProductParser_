/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ProductPriceHistoryFull } from './ProductPriceHistoryFull';

export type PaginatedProductPriceHistoryFullList = {
    count?: number;
    next?: string | null;
    previous?: string | null;
    results?: Array<ProductPriceHistoryFull>;
};
