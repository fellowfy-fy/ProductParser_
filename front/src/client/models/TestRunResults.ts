/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { TestRunResultsData } from './TestRunResultsData';
import type { TestRunResultsLog } from './TestRunResultsLog';

export type TestRunResults = {
    data: Array<TestRunResultsData>;
    logs: Array<TestRunResultsLog>;
};
