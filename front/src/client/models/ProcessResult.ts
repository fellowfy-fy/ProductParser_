/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ParseResult } from './ParseResult';

export type ProcessResult = {
    parse_result: Array<ParseResult>;
    settings: number;
    task: number;
    product?: number | null;
};
