import React from 'react';
import logo from './logo.svg';
import './App.css';
import ListModules from './components/ListModules';
import PipelineTable from './components/PipelineTable';
import {OpenAPI} from './services/suspark/core/OpenAPI'

// FIXME: remove before release
OpenAPI.BASE = 'http://localhost:9091';

function App() {
  return (
    <PipelineTable/>
  );
}

export default App;
