/*
 * Copyright (c) 2021 SeisSpark (https://github.com/kdeyev/SeisSpark).
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     https://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import { request as __request } from '../core/request';

export class ModulesService {

    /**
     * Get Modules
     * @returns string Successful Response
     * @throws ApiError
     */
    public static async getModulesApiV1ModulesGet(): Promise<Array<string>> {
        const result = await __request({
            method: 'GET',
            path: `/api/v1/modules`,
        });
        return result.body;
    }

    /**
     * Get Module Schema
     * @param moduleType
     * @returns any Successful Response
     * @throws ApiError
     */
    public static async getModuleSchemaApiV1ModulesModuleTypeGet(
moduleType: string,
): Promise<any> {
        const result = await __request({
            method: 'GET',
            path: `/api/v1/modules/${moduleType}`,
            errors: {
                422: `Validation Error`,
            },
        });
        return result.body;
    }

}
