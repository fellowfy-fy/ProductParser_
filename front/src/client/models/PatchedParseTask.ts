/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { MonitoringModeEnum } from './MonitoringModeEnum';
import type { MonitoringTypeEnum } from './MonitoringTypeEnum';
import type { NotificationsTargetEnum } from './NotificationsTargetEnum';
import type { PeriodEnum } from './PeriodEnum';
import type { StatusEnum } from './StatusEnum';
import type { WorkModeEnum } from './WorkModeEnum';

export type PatchedParseTask = {
    readonly id?: number;
    name?: string | null;
    status?: StatusEnum;
    period?: PeriodEnum;
    period_date1?: string | null;
    period_date2?: string | null;
    monitoring_mode?: MonitoringModeEnum;
    monitoring_type?: MonitoringTypeEnum;
    work_mode?: WorkModeEnum;
    urls?: string | null;
    notifications_enable?: boolean;
    notifications_target?: NotificationsTargetEnum | null;
    readonly created_at?: string | null;
    readonly updated_at?: string | null;
    author?: number;
    products?: Array<number>;
};
