import { Paper } from '@material-ui/core'
import Slider from '@material-ui/core/Slider'
import Typography from '@material-ui/core/Typography'
import React from 'react'
import Plot from 'react-plotly.js'

import { PipelinesService } from '../services/suspark/services/PipelinesService'

interface State {
  keys: Array<number> | undefined
  data: Array<Array<number>> | undefined
  currentKey: number | undefined
}

interface Props {
  pipelineIDToShow: string | undefined
  moduleIDToShow: string | undefined
}

class SeismicPlot extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props)

    this.state = {
      keys: undefined,
      data: undefined,
      currentKey: undefined,
    }
  }

  loadKeys = () => {
    if (this.props.pipelineIDToShow && this.props.moduleIDToShow) {
      PipelinesService.getPipelineModuleDataInfoApiV1PipelinesPipelineIdModulesModuleIdKeysGet(
        this.props.pipelineIDToShow,
        this.props.moduleIDToShow
      )
        .then((keys: Array<number>) => {
          let currentKey = undefined
          if (this.state.currentKey && keys.includes(this.state.currentKey)) {
            currentKey = this.state.currentKey
          }
          if (currentKey === undefined) {
            currentKey = keys[0]
          }
          this.setState({ keys: keys, currentKey: currentKey })
          this.loadData()
        })
        .catch((error: string) => {
          console.error(error)
        })
    }
  }

  loadData = () => {
    if (
      this.props.pipelineIDToShow &&
      this.props.moduleIDToShow &&
      this.state.currentKey !== undefined
    )
      PipelinesService.getPipelineModuleDataApiV1PipelinesPipelineIdModulesModuleIdDataKeyGet(
        this.props.pipelineIDToShow,
        this.props.moduleIDToShow,
        this.state.currentKey
      )
        .then((data: Array<Array<number>>) => {
          this.setState({ data: data })
        })
        .catch((error: string) => {
          console.error(error)
        })
  }

  onKeyChange = (event: React.ChangeEvent<{}>, value: number | number[]) => {
    if (value !== undefined) {
      let key = this.keyValueByIndex(Array.isArray(value) ? value[0] : value)
      this.setState({ currentKey: key })
      this.loadData()
    }
  }
  componentDidUpdate = (prevProps: Props) => {
    if (
      prevProps.pipelineIDToShow !== this.props.pipelineIDToShow ||
      prevProps.moduleIDToShow !== this.props.moduleIDToShow
    ) {
      this.loadKeys()
    }
  }

  keyValueByIndex = (value: number) => {
    if (this.state.keys) {
      return this.state.keys[value]
    } else {
      return 0
    }
  }

  keyValueByIndexString = (value: number) => {
    return this.keyValueByIndex(value).toString()
  }
  public render() {
    let slider = <div></div>
    if (this.state.keys !== undefined)
      slider = (
        <Slider
          defaultValue={30}
          valueLabelDisplay="on"
          step={1}
          marks
          min={0}
          max={this.state.keys?.length - 1}
          getAriaValueText={this.keyValueByIndexString}
          valueLabelFormat={this.keyValueByIndexString}
          onChangeCommitted={this.onKeyChange}
        />
      )

    return this.state.data ? (
      <Paper>
        <Typography>Key: {this.state.currentKey}</Typography>
        {slider}
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
      </Paper>
    ) : (
      <Paper />
    )
  }
}

export default SeismicPlot
