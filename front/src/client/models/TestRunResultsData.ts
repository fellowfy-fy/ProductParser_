/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { CachedLog } from './CachedLog';
import type { ProcessResult } from './ProcessResult';

export type TestRunResultsData = {
    logs: Array<CachedLog>;
    data: Array<ProcessResult>;
};
