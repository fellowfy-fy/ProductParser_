/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export type Product = {
    readonly id: number;
    readonly created_at: string | null;
    readonly updated_at: string | null;
    name: string;
    synonyms?: string;
    linked_id?: string | null;
    price: number;
    task?: number | null;
    categories?: Array<number>;
};
