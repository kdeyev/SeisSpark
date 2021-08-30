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
import React from 'react'
import './App.css'
import PipelineTable from './components/PipelineTable'
import PipelineView from './components/PipelineView'

// FIXME: remove before release
// OpenAPI.BASE = 'http://localhost:9091'

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
      return <PipelineView pipelineID={pipelineID} />
    } else {
      return <PipelineTable onSelectPipeline={this.onSelectPipeline} />
    }
  }
}

export default App
