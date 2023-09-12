/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { CategoryShort } from './CategoryShort';
import type { ShortUser } from './ShortUser';

export type PatchedProduct = {
    readonly id?: number;
    categories?: Array<CategoryShort>;
    categories_write?: Array<number>;
    readonly author?: ShortUser;
    readonly created_at?: string | null;
    readonly updated_at?: string | null;
    name?: string;
    synonyms?: string;
    linked_id?: string | null;
    price?: number;
    task?: number | null;
};
