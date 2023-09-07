/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ShortUser } from './ShortUser';

export type Category = {
    readonly id: number;
    readonly author: ShortUser;
    readonly created_at: string | null;
    readonly updated_at: string | null;
    name: string;
};
