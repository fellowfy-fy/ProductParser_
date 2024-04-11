/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import { CategoryShort } from "./CategoryShort";
import { StatusProductShort } from "./StatusProductShort";

export type ProductShort = {
    readonly id: number;
    categories: CategoryShort[];
    statusproducts: StatusProductShort[];
    name: string;
};
