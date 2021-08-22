/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import { request as __request } from '../core/request';

export class ModulesService {

    /**
     * Get Modules
     * @returns any Successful Response
     * @throws ApiError
     */
    public static async getModulesApiV1ModulesGet(): Promise<any> {
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