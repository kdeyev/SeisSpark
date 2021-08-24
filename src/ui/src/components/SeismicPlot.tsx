import React from 'react'
import Plot from 'react-plotly.js'

import { PipelinesService } from '../services/suspark/services/PipelinesService'

interface State {
  data: Array<Array<number>> | undefined
}

interface Props {
  pipelineIDToShow: string | undefined
  moduleIDToShow: string | undefined
}

class SeismicPlot extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props)

    this.state = {
      data: undefined,
    }
  }

  loadData = () => {
    if (this.props.pipelineIDToShow && this.props.moduleIDToShow)
      PipelinesService.getPipelineModuleDataApiV1PipelinesPipelineIdModulesModuleIdDataGet(
        this.props.pipelineIDToShow,
        this.props.moduleIDToShow
      )
        .then((data: Array<Array<number>>) => {
          this.setState({ data: data })
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
      this.loadData()
    }
  }

  public render() {
    return this.state.data ? (
      <Plot
        data={[
          {
            z: this.state.data,
            type: 'heatmap',
            transpose: true,
            zsmooth: 'best',
            // zauto: false,
            // zmin: -zmax,
            // zmax: zmax,
            colorscale: [
              [0, 'rgb(0,0,255)'],
              [0.5, 'rgb(255,255,255)'],
              [1, 'rgb(255,0,0)'],
            ],
          },
        ]}
        layout={{ title: 'A Fancy Plot' }}
      />
    ) : (
      <div />
    )
  }
}

export default SeismicPlot
