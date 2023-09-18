/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { TypeEnum } from './TypeEnum';

export type ExportRequest = {
    task?: number;
    product?: number;
    date_from?: string;
    date_to?: string;
    type: TypeEnum;
};
