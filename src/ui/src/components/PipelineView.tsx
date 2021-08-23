import React from 'react'

import PipelineEditor from './PipelineEditor'
import SeismicPlot from './SeismicPlot'

interface State {}

interface Props {
  pipelineID: string
}
class PipelineView extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props)
  }

  public render() {
    return (
      <div>
        <PipelineEditor pipelineID={this.props.pipelineID} />
        <SeismicPlot></SeismicPlot>
      </div>
    )
  }
}

export default PipelineView
