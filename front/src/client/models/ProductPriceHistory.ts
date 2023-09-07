/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ShortUser } from './ShortUser';

export type ProductPriceHistory = {
    readonly id: number;
    author: ShortUser;
    readonly created_at: string | null;
    readonly updated_at: string | null;
    price: number;
    product: number;
    task?: number | null;
};
