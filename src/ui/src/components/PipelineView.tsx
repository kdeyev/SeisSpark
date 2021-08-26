import DockLayout, { LayoutBase, LayoutData, TabBase, TabData } from 'rc-dock'
import 'rc-dock/dist/rc-dock.css'
import React from 'react'

import ModuleParametersEditor from './ModuleParametersEditor'
import PipelineEditor from './PipelineEditor'
import SeismicPlot from './SeismicPlot'

const Context = React.createContext({ moduleIDToShow: '', pipelineRevision: '' })

let randomString = (length: number) => {
  let result = ''
  let characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
  let charactersLength = characters.length
  for (let i = 0; i < length; i++) {
    result += characters.charAt(Math.floor(Math.random() * charactersLength))
  }
  return result
}

let groups = {
  default: {
    floatable: true,
    maximizable: true,
  },
}

interface State {
  // pipelineIDToShow: string | undefined
  moduleIDToShow: string

  pipelineRevision: string
  layout: LayoutBase | undefined
}

interface Props {
  pipelineID: string
}
class PipelineView extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props)

    this.state = {
      // pipelineIDToShow: undefined,
      moduleIDToShow: '',
      pipelineRevision: '',
      layout: {
        dockbox: {
          mode: 'horizontal',
          children: [
            {
              tabs: [
                {
                  id: 'PipelineEditor',
                },
              ],
            },
            {
              tabs: [
                {
                  id: 'SeismicPlot',
                },
              ],
            },
          ],
        },
        floatbox: {
          mode: 'float',
          children: [
            {
              tabs: [
                {
                  id: 'ModuleParametersEditor',
                },
              ],
              x: 300,
              y: 600,
              w: 500,
              h: 400,
            },
          ],
        },
      } as LayoutData,
    }
  }

  onShowMudule = (pipelineID: string, moduleID: string) => {
    this.setState({ moduleIDToShow: moduleID })
  }

  onModuleParametersChange = (moduleID: string) => {
    this.setState({ pipelineRevision: randomString(5) })
  }

  onPipelineModified = (pipelineID: string) => {
    this.setState({ pipelineRevision: randomString(5) })
  }

  onLayoutChange = (layout: LayoutBase) => {
    this.setState({ layout })
  }

  loadTab = (tab: TabBase) => {
    let id = tab.id
    switch (id) {
      case 'PipelineEditor':
        return {
          id,
          title: 'PipelineEditor',
          group: 'default',

          content: (
            <PipelineEditor
              pipelineID={this.props.pipelineID}
              onShowMudule={this.onShowMudule}
              onPipelineModified={this.onPipelineModified}
            />
          ),
        } as TabData
      case 'ModuleParametersEditor':
        return {
          id,
          title: 'ModuleParametersEditor',
          // group: 'default',

          content: (
            <Context.Consumer>
              {(state) => (
                <ModuleParametersEditor
                  pipelineIDToShow={this.props.pipelineID}
                  moduleIDToShow={state.moduleIDToShow}
                  onModuleParametersChange={this.onModuleParametersChange}
                />
              )}
            </Context.Consumer>
          ),
        } as TabData
      case 'SeismicPlot':
        return {
          id,
          title: 'SeismicPlot',
          group: 'default',

          content: (
            <Context.Consumer>
              {(state) => (
                <SeismicPlot
                  pipelineIDToShow={this.props.pipelineID}
                  moduleIDToShow={state.moduleIDToShow}
                  pipelineRevision={state.pipelineRevision}
                />
              )}
            </Context.Consumer>
          ),
        } as TabData
    }

    return {
      id,
      title: id,
      content: <div>Tab Content</div>,
    } as TabData
  }

  public render() {
    return (
      // pipelineIDToShow: string | undefined
      // moduleIDToShow: string | undefined

      // pipelineRevision: string | undefined

      <Context.Provider
        value={{
          moduleIDToShow: this.state.moduleIDToShow,
          pipelineRevision: this.state.pipelineRevision,
        }}
      >
        <DockLayout
          loadTab={this.loadTab}
          groups={groups}
          layout={this.state.layout}
          onLayoutChange={this.onLayoutChange}
          style={{
            position: 'absolute',
            left: 10,
            top: 10,
            right: 10,
            bottom: 10,
          }}
        />
      </Context.Provider>
    )
    // <PipelineEditor
    //   pipelineID={this.props.pipelineID}
    //   onShowMudule={this.onShowMudule}
    //   onPipelineModified={this.onPipelineModified}
    // />
    // <ModuleParametersEditor
    //   pipelineIDToShow={this.state.pipelineIDToShow}
    //   moduleIDToShow={this.state.moduleIDToShow}
    //   onModuleParametersChange={this.onModuleParametersChange}
    // />
    // <SeismicPlot
    //   pipelineIDToShow={this.state.pipelineIDToShow}
    //   moduleIDToShow={this.state.moduleIDToShow}
    //   pipelineRevision={this.state.pipelineRevision}
    // />
  }
}

export default PipelineView
