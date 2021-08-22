import React from 'react';
import logo from './logo.svg';
import './App.css';
import ListModules from './components/ListModules';
import PipelineTable from './components/PipelineTable';
import {OpenAPI} from './services/suspark/core/OpenAPI'

// FIXME: remove before release
OpenAPI.BASE = 'http://localhost:9091';

interface State {

}

interface Props {
}

class App extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
  }

  private onSelectPipeline(pipelineID: string) {
      window.location.hash = "";
      window.location.search = "?pipelineID=" + pipelineID;
  }  

  public render() {
    const urlParams = new URLSearchParams(window.location.search);
    const pipelineID = urlParams.get("pipelineID");
    if (pipelineID) {
      return (<ListModules/>);
    }
    else {
      return (
      <PipelineTable onSelectPipeline={this.onSelectPipeline}/>
    );
      }
  }
}


export default App;
