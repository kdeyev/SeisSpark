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
import Slider from '@material-ui/core/Slider'
import Typography from '@material-ui/core/Typography'
import React from 'react'
import Plot from 'react-plotly.js'
import { PipelinesService } from '../services/seisspark/services/PipelinesService'

let findMinMax = (data: Array<Array<number>>) => {
  var max = -Infinity
  var min = +Infinity

  for (let i = 0; i < data.length; i++) {
    const elementArray = data[i]
    if (max < Math.max.apply(Math, elementArray)) {
      max = Math.max.apply(Math, elementArray)
    }
    if (min > Math.min.apply(Math, elementArray)) {
      min = Math.min.apply(Math, elementArray)
    }
  }
  return { min: min, max: max }
}

interface State {
  keys: Array<number> | undefined
  data: Array<Array<number>> | undefined
  currentKey: number | undefined
  currentIndex: number
  minValue: number
  maxValue: number
}

interface Props {
  pipelineIDToShow: string | undefined
  moduleIDToShow: string | undefined
  pipelineRevision: string | undefined
}

class SeismicPlot extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props)

    this.state = {
      keys: undefined,
      data: undefined,
      currentKey: undefined,
      currentIndex: 0,
      minValue: 0,
      maxValue: 0,
    }
  }

  loadKeys = () => {
    if (this.props.pipelineIDToShow && this.props.moduleIDToShow) {
      PipelinesService.getPipelineModuleDataInfoApiV1PipelinesPipelineIdModulesModuleIdKeysGet(
        this.props.pipelineIDToShow,
        this.props.moduleIDToShow
      )
        .then((keys: Array<number>) => {
          let currentIndex = 0
          if (this.state.currentKey && keys.includes(this.state.currentKey)) {
            currentIndex = keys.findIndex((i: number) => {
              return i === this.state.currentKey
            })
          }
          let currentKey = keys[currentIndex]

          this.setState({ keys, currentKey, currentIndex })
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
          const minMax = findMinMax(data)
          this.setState({ data: data, minValue: minMax.min, maxValue: minMax.max })
        })
        .catch((error: string) => {
          console.error(error)
        })
  }

  onKeyChange = (event: React.ChangeEvent<{}>, value: number | number[]) => {
    if (value !== undefined) {
      let key = this.keyValueByIndex(Array.isArray(value) ? value[0] : value)
      this.setState({ currentKey: key })
      this.loadKeys()
    }
  }
  componentDidUpdate = (prevProps: Props) => {
    if (
      prevProps.pipelineIDToShow !== this.props.pipelineIDToShow ||
      prevProps.moduleIDToShow !== this.props.moduleIDToShow ||
      prevProps.pipelineRevision !== this.props.pipelineRevision
    ) {
      this.loadKeys()
      this.loadData()
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
    const norm = Math.max(-this.state.minValue, this.state.maxValue)

    let slider = <div></div>
    if (this.state.keys !== undefined)
      slider = (
        <Slider
          defaultValue={this.state.currentIndex}
          valueLabelDisplay="on"
          step={1}
          marks
          min={0}
          max={this.state.keys.length - 1}
          getAriaValueText={this.keyValueByIndexString}
          valueLabelFormat={this.keyValueByIndexString}
          onChangeCommitted={this.onKeyChange}
        />
      )

    var config = { responsive: true, autosizable: true }

    return this.state.data ? (
      <div style={{ width: '100%', height: '100%' }}>
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
              // zmin: -norm,
              // zmax: norm,
              colorscale: [
                [0, 'rgb(0,0,255)'],
                [0.5, 'rgb(255,255,255)'],
                [1, 'rgb(255,0,0)'],
              ],
              //   colorbar: { symmetric: true },
              //   colorbar: { symmetric: true } as ColorBar,
            },
          ]}
          config={config}
          useResizeHandler={true}
          style={{ width: '100%', height: '100%' }}
          layout={{
            margin: {
              l: 50,
              r: 50,
              // b: 50,
              t: 50,
              pad: 4,
            },
            // title: 'A Fancy Plot',
            yaxis: { title: 'Time', autorange: 'reversed' },
            showlegend: false,
            autosize: true,
          }}
        />
      </div>
    ) : (
      <div />
    )
  }
}

export default SeismicPlot
