/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { MonitoringTypeEnum } from './MonitoringTypeEnum';
import type { NotificationsTargetEnum } from './NotificationsTargetEnum';
import type { PeriodEnum } from './PeriodEnum';
import type { Product } from './Product';
import type { ShortUser } from './ShortUser';
import type { StatusEnum } from './StatusEnum';
import type { WorkModeEnum } from './WorkModeEnum';

export type PatchedParseTask = {
    readonly id?: number;
    readonly author?: ShortUser;
    monitoring_type?: Array<MonitoringTypeEnum>;
    notifications_target?: Array<NotificationsTargetEnum>;
    readonly products?: Array<Product>;
    products_write?: Array<number>;
    name?: string | null;
    readonly status?: StatusEnum;
    period?: PeriodEnum;
    period_date1?: string | null;
    period_date2?: string | null;
    monitoring_mode?: WorkModeEnum;
    work_mode?: WorkModeEnum;
    urls?: string | null;
    notifications_enable?: boolean;
    readonly created_at?: string | null;
    readonly updated_at?: string | null;
    readonly last_run_at?: string | null;
    readonly invalid_urls?: Record<string, any> | null;
};
