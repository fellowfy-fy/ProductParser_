/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ShortUser } from './ShortUser';

export type PatchedCategory = {
    readonly id?: number;
    author?: ShortUser;
    readonly created_at?: string | null;
    readonly updated_at?: string | null;
    name?: string;
};
