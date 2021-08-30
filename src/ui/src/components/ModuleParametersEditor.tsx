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
      PipelinesService.setPipelineModuleParametersApiV1PipelinesPipelineIdModulesModuleIdParametersPut(
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
      PipelinesService.getPipelineModuleSchemaApiV1PipelinesPipelineIdModulesModuleIdSchemaGet(
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
      PipelinesService.getPipelineModuleParametersApiV1PipelinesPipelineIdModulesModuleIdParametersGet(
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
