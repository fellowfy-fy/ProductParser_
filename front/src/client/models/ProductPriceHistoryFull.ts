/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ParseTaskShort } from './ParseTaskShort';
import type { ProductShort } from './ProductShort';
import type { SiteParseSettingsShort } from './SiteParseSettingsShort';

export type ProductPriceHistoryFull = {
    readonly id: number;
    product: ProductShort;
    parse_settings: SiteParseSettingsShort;
    task: ParseTaskShort;
    readonly created_at: string | null;
    readonly updated_at: string | null;
    price: number;
};
