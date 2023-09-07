/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export type ShortUser = {
    /**
     * Обязательное поле. Не более 150 символов. Только буквы, цифры и символы @/./+/-/_.
     */
    username: string;
    readonly id: number;
    first_name?: string;
    last_name?: string;
    middle_name?: string | null;
};
