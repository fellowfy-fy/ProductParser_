/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export type ProductPriceHistory = {
    readonly id: number;
    readonly created_at: string | null;
    readonly updated_at: string | null;
    price: number;
    product: number;
    task?: number | null;
};
