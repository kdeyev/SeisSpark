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
import type { CreateModuleRequest } from '../models/CreateModuleRequest';
import type { CreatePipelineRequest } from '../models/CreatePipelineRequest';
import type { ModuleDescription } from '../models/ModuleDescription';
import type { ModuleInfo } from '../models/ModuleInfo';
import type { MoveModuleRequest } from '../models/MoveModuleRequest';
import type { PipelineInfo } from '../models/PipelineInfo';

export class PipelinesService {

    /**
     * Get Pipelines
     * @returns PipelineInfo Successful Response
     * @throws ApiError
     */
    public static async getPipelines(): Promise<Array<PipelineInfo>> {
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
    public static async createPipeline(
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
    public static async getPipeline(
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
    public static async deletePipeline(
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
    public static async getPipelineModules(
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
     * @returns any Successful Response
     * @throws ApiError
     */
    public static async movePipelineModule(
pipelineId: string,
requestBody: MoveModuleRequest,
): Promise<any> {
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
    public static async createPipelineModule(
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
    public static async deletePipelineModule(
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
    public static async getPipelineModuleParameters(
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
    public static async setPipelineModuleParameters(
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
    public static async getPipelineModuleSchema(
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
     * Get Pipeline Module Data Info
     * @param pipelineId
     * @param moduleId
     * @returns any Successful Response
     * @throws ApiError
     */
    public static async getPipelineModuleDataInfo(
pipelineId: string,
moduleId: string,
): Promise<any> {
        const result = await __request({
            method: 'GET',
            path: `/api/v1/pipelines/${pipelineId}/modules/${moduleId}/keys`,
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
     * @param key
     * @returns any Successful Response
     * @throws ApiError
     */
    public static async getPipelineModuleData(
pipelineId: string,
moduleId: string,
key: number,
): Promise<any> {
        const result = await __request({
            method: 'GET',
            path: `/api/v1/pipelines/${pipelineId}/modules/${moduleId}/data/${key}`,
            errors: {
                422: `Validation Error`,
            },
        });
        return result.body;
    }

}
