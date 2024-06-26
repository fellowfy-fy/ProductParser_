/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { TypeEnum } from './TypeEnum';

export type ExportRequest = {
    task?: number;
    products: Array<number>;
    statusproducts?: Array<number>;
    competitor?: string;
    categories?: Array<number>;
    date_from?: string;
    date_to?: string;
    type: TypeEnum;
};
