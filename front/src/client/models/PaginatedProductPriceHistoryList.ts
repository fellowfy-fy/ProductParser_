/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ProductPriceHistory } from './ProductPriceHistory';

export type PaginatedProductPriceHistoryList = {
    count?: number;
    next?: string | null;
    previous?: string | null;
    results?: Array<ProductPriceHistory>;
};
