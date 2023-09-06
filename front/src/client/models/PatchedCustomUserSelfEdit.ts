/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { RoleEnum } from './RoleEnum';

export type PatchedCustomUserSelfEdit = {
    readonly id?: number;
    readonly auth_token?: string;
    readonly last_login?: string | null;
    /**
     * Обязательное поле. Не более 150 символов. Только буквы, цифры и символы @/./+/-/_.
     */
    username?: string;
    first_name?: string;
    last_name?: string;
    readonly email?: string;
    /**
     * Отметьте, если пользователь может входить в административную часть сайта.
     */
    readonly is_staff?: boolean;
    /**
     * Отметьте, если пользователь должен считаться активным. Уберите эту отметку вместо удаления учётной записи.
     */
    is_active?: boolean;
    readonly date_joined?: string;
    middle_name?: string | null;
    role?: RoleEnum;
    manager?: number | null;
};
