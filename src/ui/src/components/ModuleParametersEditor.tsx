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
import { Paper } from '@material-ui/core'
import { ISubmitEvent } from '@rjsf/core'
import Form from '@rjsf/material-ui'
import { JSONSchema7 } from 'json-schema'
import React from 'react'

import { PipelinesService } from '../services/seisspark/services/PipelinesService'

interface State {
  schema: JSONSchema7
  parameters: any
}

interface Props {
  pipelineIDToShow: string | undefined
  moduleIDToShow: string | undefined
  onModuleParametersChange: (pipelineID: string, moduleID: string) => void
}

class ModuleParametersEditor extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props)

    let schema = {} as JSONSchema7
    this.state = {
      schema: schema,
      parameters: {},
    }
    this.loadSchema()
    this.loadParameters()
  }

  onParametersSubmit = (e: ISubmitEvent<any>) => {
    if (this.props.pipelineIDToShow && this.props.moduleIDToShow) {
      PipelinesService.setPipelineModuleParameters(
        this.props.pipelineIDToShow,
        this.props.moduleIDToShow,
        e.formData
      )
        .then(() => {
          if (this.props.pipelineIDToShow && this.props.moduleIDToShow) {
            this.props.onModuleParametersChange(
              this.props.pipelineIDToShow,
              this.props.moduleIDToShow
            )
            this.loadSchema()
            this.loadParameters()
          }
        })
        .catch((error: string) => {
          console.error(error)
        })
    }
  }

  loadSchema = () => {
    if (this.props.pipelineIDToShow && this.props.moduleIDToShow)
      PipelinesService.getPipelineModuleSchema(
        this.props.pipelineIDToShow,
        this.props.moduleIDToShow
      )
        .then((schema: any) => {
          this.setState({ schema: schema as JSONSchema7 })
        })
        .catch((error: string) => {
          console.error(error)
        })
  }

  loadParameters = () => {
    if (this.props.pipelineIDToShow && this.props.moduleIDToShow)
      PipelinesService.getPipelineModuleParameters(
        this.props.pipelineIDToShow,
        this.props.moduleIDToShow
      )
        .then((parameters: any) => {
          this.setState({ parameters: parameters })
        })
        .catch((error: string) => {
          console.error(error)
        })
  }

  componentDidUpdate = (prevProps: Props) => {
    if (
      prevProps.pipelineIDToShow !== this.props.pipelineIDToShow ||
      prevProps.moduleIDToShow !== this.props.moduleIDToShow
    ) {
      this.loadSchema()
      this.loadParameters()
    }
  }

  public render() {
    return (
      <Paper>
        <Form
          schema={this.state.schema}
          formData={this.state.parameters}
          // onChange={log('changed')}
          onSubmit={this.onParametersSubmit}
          // onError={log('errors')}
        />
      </Paper>
    )
  }
}

export default ModuleParametersEditor
