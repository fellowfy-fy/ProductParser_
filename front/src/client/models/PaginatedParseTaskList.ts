/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ParseTask } from './ParseTask';

export type PaginatedParseTaskList = {
    count?: number;
    next?: string | null;
    previous?: string | null;
    results?: Array<ParseTask>;
};
