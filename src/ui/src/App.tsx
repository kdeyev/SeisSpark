import React from 'react'

import './App.css'
import PipelineEditor from './components/PipelineEditor'
import PipelineTable from './components/PipelineTable'
import { OpenAPI } from './services/suspark/core/OpenAPI'

// FIXME: remove before release
OpenAPI.BASE = 'http://localhost:9091'

interface State {}

interface Props {}

class App extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props)
  }

  private onSelectPipeline(pipelineID: string) {
    window.location.hash = ''
    window.location.search = '?pipelineID=' + pipelineID
  }

  public render() {
    const urlParams = new URLSearchParams(window.location.search)
    const pipelineID = urlParams.get('pipelineID')
    if (pipelineID) {
      return <PipelineEditor pipelineID={pipelineID} />
    } else {
      return <PipelineTable onSelectPipeline={this.onSelectPipeline} />
    }
  }
}

export default App
