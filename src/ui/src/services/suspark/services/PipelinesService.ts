/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CreateModuleRequest } from '../models/CreateModuleRequest';
import type { CreatePipelineRequest } from '../models/CreatePipelineRequest';
import type { ModuleDescription } from '../models/ModuleDescription';
import type { ModuleInfo } from '../models/ModuleInfo';
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
     * Create Pipeline Modules
     * @param pipelineId 
     * @param requestBody 
     * @returns ModuleDescription Successful Response
     * @throws ApiError
     */
    public static async createPipelineModulesApiV1PipelinesPipelineIdModulesPost(
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

}