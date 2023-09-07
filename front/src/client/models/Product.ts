/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ShortUser } from './ShortUser';

export type Product = {
    readonly id: number;
    readonly author: ShortUser;
    readonly created_at: string | null;
    readonly updated_at: string | null;
    name: string;
    synonyms?: string;
    linked_id?: string | null;
    price: number;
    task?: number | null;
    categories?: Array<number>;
};
