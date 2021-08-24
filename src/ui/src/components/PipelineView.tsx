import React from 'react'

import ModuleParametersEditor from './ModuleParametersEditor'
import PipelineEditor from './PipelineEditor'
import SeismicPlot from './SeismicPlot'

let randomString = (length: number) => {
  let result = ''
  let characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
  let charactersLength = characters.length
  for (let i = 0; i < length; i++) {
    result += characters.charAt(Math.floor(Math.random() * charactersLength))
  }
  return result
}

interface State {
  pipelineIDToShow: string | undefined
  moduleIDToShow: string | undefined

  pipelineRevision: string | undefined
}

interface Props {
  pipelineID: string
}
class PipelineView extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props)

    this.state = {
      pipelineIDToShow: undefined,
      moduleIDToShow: undefined,
      pipelineRevision: undefined,
    }
  }

  onShowMudule = (pipelineID: string, moduleID: string) => {
    this.setState({ pipelineIDToShow: pipelineID, moduleIDToShow: moduleID })
  }

  onModuleParametersChange = (pipelineID: string, moduleID: string) => {
    this.setState({ pipelineRevision: randomString(5) })
  }

  onPipelineModified = (pipelineID: string) => {
    this.setState({ pipelineRevision: randomString(5) })
  }

  public render() {
    return (
      <div>
        <PipelineEditor
          pipelineID={this.props.pipelineID}
          onShowMudule={this.onShowMudule}
          onPipelineModified={this.onPipelineModified}
        />
        <ModuleParametersEditor
          pipelineIDToShow={this.state.pipelineIDToShow}
          moduleIDToShow={this.state.moduleIDToShow}
          onModuleParametersChange={this.onModuleParametersChange}
        />
        <SeismicPlot
          pipelineIDToShow={this.state.pipelineIDToShow}
          moduleIDToShow={this.state.moduleIDToShow}
          pipelineRevision={this.state.pipelineRevision}
        />
      </div>
    )
  }
}

export default PipelineView
