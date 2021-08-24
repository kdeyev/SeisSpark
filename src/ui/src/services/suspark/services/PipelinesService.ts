/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CreateModuleRequest } from '../models/CreateModuleRequest';
import type { CreatePipelineRequest } from '../models/CreatePipelineRequest';
import type { ModuleDescription } from '../models/ModuleDescription';
import type { ModuleInfo } from '../models/ModuleInfo';
import type { MoveModuleRequest } from '../models/MoveModuleRequest';
import type { PipelineInfo } from '../models/PipelineInfo';
import { request as __request } from '../core/request';

export class PipelinesService {

    /**
     * Get Pipelines
     * @returns PipelineInfo Successful Response
     * @throws ApiError
     */
    public static async getPipelinesApiV1PipelinesGet(): Promise<Array<PipelineInfo>> {
        const result = await __request({
            method: 'GET',
            path: `/api/v1/pipelines`,
        });
        return result.body;
    }

    /**
     * Create Pipelines
     * @param requestBody 
     * @returns PipelineInfo Successful Response
     * @throws ApiError
     */
    public static async createPipelinesApiV1PipelinesPost(
requestBody: CreatePipelineRequest,
): Promise<PipelineInfo> {
        const result = await __request({
            method: 'POST',
            path: `/api/v1/pipelines`,
            body: requestBody,
            errors: {
                422: `Validation Error`,
            },
        });
        return result.body;
    }

    /**
     * Get Pipeline
     * @param pipelineId 
     * @returns PipelineInfo Successful Response
     * @throws ApiError
     */
    public static async getPipelineApiV1PipelinesPipelineIdGet(
pipelineId: string,
): Promise<PipelineInfo> {
        const result = await __request({
            method: 'GET',
            path: `/api/v1/pipelines/${pipelineId}`,
            errors: {
                422: `Validation Error`,
            },
        });
        return result.body;
    }

    /**
     * Delete Pipeline
     * @param pipelineId 
     * @returns any Successful Response
     * @throws ApiError
     */
    public static async deletePipelineApiV1PipelinesPipelineIdDelete(
pipelineId: string,
): Promise<any> {
        const result = await __request({
            method: 'DELETE',
            path: `/api/v1/pipelines/${pipelineId}`,
            errors: {
                422: `Validation Error`,
            },
        });
        return result.body;
    }

    /**
     * Get Pipeline Modules
     * @param pipelineId 
     * @returns ModuleInfo Successful Response
     * @throws ApiError
     */
    public static async getPipelineModulesApiV1PipelinesPipelineIdModulesGet(
pipelineId: string,
): Promise<Array<ModuleInfo>> {
        const result = await __request({
            method: 'GET',
            path: `/api/v1/pipelines/${pipelineId}/modules`,
            errors: {
                422: `Validation Error`,
            },
        });
        return result.body;
    }

    /**
     * Move Pipeline Module
     * @param pipelineId 
     * @param requestBody 
     * @returns ModuleDescription Successful Response
     * @throws ApiError
     */
    public static async movePipelineModuleApiV1PipelinesPipelineIdModulesPut(
pipelineId: string,
requestBody: MoveModuleRequest,
): Promise<ModuleDescription> {
        const result = await __request({
            method: 'PUT',
            path: `/api/v1/pipelines/${pipelineId}/modules`,
            body: requestBody,
            errors: {
                422: `Validation Error`,
            },
        });
        return result.body;
    }

    /**
     * Create Pipeline Module
     * @param pipelineId 
     * @param requestBody 
     * @returns ModuleDescription Successful Response
     * @throws ApiError
     */
    public static async createPipelineModuleApiV1PipelinesPipelineIdModulesPost(
pipelineId: string,
requestBody: CreateModuleRequest,
): Promise<ModuleDescription> {
        const result = await __request({
            method: 'POST',
            path: `/api/v1/pipelines/${pipelineId}/modules`,
            body: requestBody,
            errors: {
                422: `Validation Error`,
            },
        });
        return result.body;
    }

    /**
     * Delete Pipeline Module
     * @param pipelineId 
     * @param moduleId 
     * @returns any Successful Response
     * @throws ApiError
     */
    public static async deletePipelineModuleApiV1PipelinesPipelineIdModulesModuleIdDelete(
pipelineId: string,
moduleId: string,
): Promise<any> {
        const result = await __request({
            method: 'DELETE',
            path: `/api/v1/pipelines/${pipelineId}/modules/${moduleId}`,
            errors: {
                422: `Validation Error`,
            },
        });
        return result.body;
    }

    /**
     * Get Pipeline Module Parameters
     * @param pipelineId 
     * @param moduleId 
     * @returns any Successful Response
     * @throws ApiError
     */
    public static async getPipelineModuleParametersApiV1PipelinesPipelineIdModulesModuleIdParametersGet(
pipelineId: string,
moduleId: string,
): Promise<any> {
        const result = await __request({
            method: 'GET',
            path: `/api/v1/pipelines/${pipelineId}/modules/${moduleId}/parameters`,
            errors: {
                422: `Validation Error`,
            },
        });
        return result.body;
    }

    /**
     * Set Pipeline Module Parameters
     * @param pipelineId 
     * @param moduleId 
     * @param requestBody 
     * @returns any Successful Response
     * @throws ApiError
     */
    public static async setPipelineModuleParametersApiV1PipelinesPipelineIdModulesModuleIdParametersPut(
pipelineId: string,
moduleId: string,
requestBody: any,
): Promise<any> {
        const result = await __request({
            method: 'PUT',
            path: `/api/v1/pipelines/${pipelineId}/modules/${moduleId}/parameters`,
            body: requestBody,
            errors: {
                422: `Validation Error`,
            },
        });
        return result.body;
    }

    /**
     * Get Pipeline Module Schema
     * @param pipelineId 
     * @param moduleId 
     * @returns any Successful Response
     * @throws ApiError
     */
    public static async getPipelineModuleSchemaApiV1PipelinesPipelineIdModulesModuleIdSchemaGet(
pipelineId: string,
moduleId: string,
): Promise<any> {
        const result = await __request({
            method: 'GET',
            path: `/api/v1/pipelines/${pipelineId}/modules/${moduleId}/schema`,
            errors: {
                422: `Validation Error`,
            },
        });
        return result.body;
    }

    /**
     * Get Pipeline Module Data
     * @param pipelineId 
     * @param moduleId 
     * @returns any Successful Response
     * @throws ApiError
     */
    public static async getPipelineModuleDataApiV1PipelinesPipelineIdModulesModuleIdDataGet(
pipelineId: string,
moduleId: string,
): Promise<any> {
        const result = await __request({
            method: 'GET',
            path: `/api/v1/pipelines/${pipelineId}/modules/${moduleId}/data`,
            errors: {
                422: `Validation Error`,
            },
        });
        return result.body;
    }

}