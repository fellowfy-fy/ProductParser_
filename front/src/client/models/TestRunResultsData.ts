/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ParseResult } from './ParseResult';
import type { ParseTaskShort } from './ParseTaskShort';
import type { ProductShort } from './ProductShort';
import type { SiteParseSettingsShort } from './SiteParseSettingsShort';

export type TestRunResultsData = {
    parse_result: Array<ParseResult>;
    task: ParseTaskShort;
    settings: SiteParseSettingsShort;
    product?: ProductShort;
};
