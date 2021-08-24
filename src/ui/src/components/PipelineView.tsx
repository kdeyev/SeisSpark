import React from 'react'

import ModuleParametersEditor from './ModuleParametersEditor'
import PipelineEditor from './PipelineEditor'
import SeismicPlot from './SeismicPlot'

interface State {
  pipelineIDToShow: string | undefined
  moduleIDToShow: string | undefined
}

interface Props {
  pipelineID: string
}
class PipelineView extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props)

    this.state = { pipelineIDToShow: undefined, moduleIDToShow: undefined }
  }

  onShowMudule = (pipelineID: string, moduleID: string) => {
    this.setState({ pipelineIDToShow: pipelineID, moduleIDToShow: moduleID })
  }

  onModuleParametersChange = (pipelineID: string, moduleID: string) => {}

  public render() {
    return (
      <div>
        <PipelineEditor pipelineID={this.props.pipelineID} onShowMudule={this.onShowMudule} />
        <ModuleParametersEditor
          pipelineIDToShow={this.state.pipelineIDToShow}
          moduleIDToShow={this.state.moduleIDToShow}
          onModuleParametersChange={this.onModuleParametersChange}
        />
        <SeismicPlot
          pipelineIDToShow={this.state.pipelineIDToShow}
          moduleIDToShow={this.state.moduleIDToShow}
        />
      </div>
    )
  }
}

export default PipelineView
