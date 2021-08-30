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
import type { ApiResult } from './ApiResult'

export class ApiError extends Error {
  public readonly url: string
  public readonly status: number
  public readonly statusText: string
  public readonly body: any

  constructor(response: ApiResult, message: string) {
    super(message)

    this.url = response.url
    this.status = response.status
    this.statusText = response.statusText
    this.body = response.body
  }
}
