/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { CategoryShort } from './CategoryShort';
import type { ShortUser } from './ShortUser';
import { StatusProductShort } from './StatusProductShort';

export type Product = {
    readonly id: number;
    readonly categories: Array<CategoryShort>;
    categories_write: Array<number> | null;
    readonly statusproducts: Array<StatusProductShort>;
    statusproducts_write: Array<number> | null;
    readonly author: ShortUser;
    readonly created_at: string | null;
    readonly updated_at: string | null;
    name: string;
    synonyms?: string;
    linked_id?: string | null;
    price: number;
    task?: number | null;
};
