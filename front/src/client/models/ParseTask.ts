/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { MonitoringTypeEnum } from './MonitoringTypeEnum';
import type { NotificationsTargetEnum } from './NotificationsTargetEnum';
import type { PeriodEnum } from './PeriodEnum';
import type { ShortUser } from './ShortUser';
import type { StatusEnum } from './StatusEnum';
import type { WorkModeEnum } from './WorkModeEnum';

export type ParseTask = {
    readonly id: number;
    author: ShortUser;
    monitoring_type: Array<MonitoringTypeEnum>;
    notifications_target: Array<NotificationsTargetEnum>;
    name?: string | null;
    readonly status: StatusEnum;
    period?: PeriodEnum;
    period_date1?: string | null;
    period_date2?: string | null;
    monitoring_mode?: WorkModeEnum;
    work_mode: WorkModeEnum;
    urls?: string | null;
    notifications_enable?: boolean;
    readonly created_at: string | null;
    readonly updated_at: string | null;
    products?: Array<number>;
};
