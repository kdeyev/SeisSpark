import {
  IconButton,
  List,
  ListItem,
  ListItemSecondaryAction,
  ListItemText,
} from '@material-ui/core'
import Avatar from '@material-ui/core/Avatar'
import ListItemAvatar from '@material-ui/core/ListItemAvatar'
import RootRef from '@material-ui/core/RootRef'
import DeleteIcon from '@material-ui/icons/Delete'
import ExtensionIcon from '@material-ui/icons/Extension'
import MemoryIcon from '@material-ui/icons/Memory'
import ShowChartIcon from '@material-ui/icons/ShowChart'
import React from 'react'
import {
  DragDropContext,
  Draggable,
  Droppable,
  DroppableProvided,
  DroppableStateSnapshot,
  DropResult,
  ResponderProvided,
} from 'react-beautiful-dnd'

import { CreateModuleRequest } from '../services/seisspark/models/CreateModuleRequest'
import { ModuleDescription } from '../services/seisspark/models/ModuleDescription'
import { ModuleInfo } from '../services/seisspark/models/ModuleInfo'
import { MoveModuleRequest } from '../services/seisspark/models/MoveModuleRequest'
import { ModulesService } from '../services/seisspark/services/ModulesService'
import { PipelinesService } from '../services/seisspark/services/PipelinesService'

const getItemStyle = (isDragging: boolean, draggableStyle: any) => ({
  // styles we need to apply on draggables
  ...draggableStyle,

  ...(isDragging && {
    background: 'rgb(235,235,235)',
  }),
})

interface State {
  moduleTypes: Array<string>
  modules: Array<ModuleInfo>
}

interface Props {
  pipelineID: string
  onShowMudule: (pipelineID: string, moduleID: string) => void
  onPipelineModified: (pipelineID: string) => void
}

class PipelineEditor extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props)
    this.state = { moduleTypes: [], modules: [] }
    this.loadModuleTypes()
    this.loadModules()
  }
  private loadModuleTypes() {
    ModulesService.getModulesApiV1ModulesGet()
      .then((moduleTypes: Array<string>) => {
        this.setState({ moduleTypes: moduleTypes })
      })
      .catch((error: string) => {
        console.error(error)
      })
  }

  loadModules = () => {
    PipelinesService.getPipelineModulesApiV1PipelinesPipelineIdModulesGet(this.props.pipelineID)
      .then((modules: Array<ModuleInfo>) => {
        this.setState({ modules: modules })
      })
      .catch((error: string) => {
        console.error(error)
      })
  }

  onModuleDelete = (moduleId: string) => {
    PipelinesService.deletePipelineModuleApiV1PipelinesPipelineIdModulesModuleIdDelete(
      this.props.pipelineID,
      moduleId
    )
      .then(() => {
        this.props.onPipelineModified(this.props.pipelineID)
        this.loadModules()
      })
      .catch((error: string) => {
        console.error(error)
      })
  }

  onModuleShow = (moduleId: string) => {
    this.props.onShowMudule(this.props.pipelineID, moduleId)
  }

  onDragEnd = (result: DropResult, provided: ResponderProvided) => {
    const { source, destination } = result

    // dropped outside the list
    if (!destination) {
      return
    }

    switch (source.droppableId) {
      case 'moduleTypes':
        if (destination.droppableId == 'pipeline') {
          const moduleType = this.state.moduleTypes[source.index]
          let prevModuleID = undefined
          if (destination.index > 0) {
            prevModuleID = this.state.modules[destination.index - 1].id
          }
          const request = {
            module_type: moduleType,
            name: moduleType,
            prev_module_id: prevModuleID,
          } as CreateModuleRequest
          PipelinesService.createPipelineModuleApiV1PipelinesPipelineIdModulesPost(
            this.props.pipelineID,
            request
          )
            .then((moduleDescription: ModuleDescription) => {
              this.props.onPipelineModified(this.props.pipelineID)
              this.loadModules()
            })
            .catch((error: string) => {
              console.error(error)
            })
        } else {
          console.error('wrong drop destination')
        }
        // this.setState({});
        break
      case 'pipeline':
        if (destination.droppableId == 'pipeline') {
          let prevModuleID = undefined
          if (destination.index > source.index) {
            prevModuleID = this.state.modules[destination.index].id
          } else if (destination.index < source.index) {
            if (destination.index > 0) {
              prevModuleID = this.state.modules[destination.index - 1].id
            }
          } else {
            return
          }
          const moduleID = this.state.modules[source.index].id

          const request = {
            module_id: moduleID,
            prev_module_id: prevModuleID,
          } as MoveModuleRequest

          PipelinesService.movePipelineModuleApiV1PipelinesPipelineIdModulesPut(
            this.props.pipelineID,
            request
          )
            .then((moduleDescription: ModuleDescription) => {
              this.props.onPipelineModified(this.props.pipelineID)
              this.loadModules()
            })
            .catch((error: string) => {
              console.error(error)
            })
        } else {
          console.error('wrong drop destination')
        }
        break
    }
  }

  public render() {
    return (
      //   <Drawer variant="persistent" anchor="left" open={true}>
      <DragDropContext onDragEnd={this.onDragEnd}>
        <Droppable droppableId="moduleTypes" isDropDisabled={true}>
          {(provided: DroppableProvided, snapshot: DroppableStateSnapshot) => (
            <RootRef rootRef={provided.innerRef}>
              <List>
                {this.state.moduleTypes.map((moduleType, index) => (
                  <Draggable key={moduleType} draggableId={moduleType} index={index}>
                    {(provided, snapshot) => (
                      <div>
                        <ListItem
                          ref={provided.innerRef}
                          {...provided.draggableProps}
                          {...provided.dragHandleProps}
                        >
                          <ListItemAvatar>
                            <Avatar>{<ExtensionIcon />}</Avatar>
                          </ListItemAvatar>
                          <ListItemText
                            primary={moduleType}
                            //secondary="Jan 9, 2014"
                          />
                        </ListItem>
                        {snapshot.isDragging && (
                          <ListItem>
                            <ListItemAvatar>
                              <Avatar>
                                {' '}
                                <ExtensionIcon />
                              </Avatar>
                            </ListItemAvatar>
                            <ListItemText
                              primary={moduleType}
                              //secondary="Jan 9, 2014"
                            />
                          </ListItem>
                        )}
                      </div>
                    )}
                  </Draggable>
                ))}
                {provided.placeholder}
              </List>
            </RootRef>
          )}
        </Droppable>
        <div>
          <Droppable droppableId="pipeline">
            {(provided, snapshot) => (
              <RootRef rootRef={provided.innerRef}>
                <List>
                  {this.state.modules.map((moduleInfo, index) => (
                    <Draggable key={moduleInfo.id} draggableId={moduleInfo.id} index={index}>
                      {(provided, snapshot) => (
                        <ListItem
                          ref={provided.innerRef}
                          {...provided.draggableProps}
                          {...provided.dragHandleProps}
                        >
                          <ListItemAvatar>
                            <Avatar>{<MemoryIcon />}</Avatar>
                          </ListItemAvatar>
                          <ListItemText
                            primary={moduleInfo.name}
                            //secondary="Jan 9, 2014"
                          />
                          <ListItemSecondaryAction>
                            <IconButton
                              edge="end"
                              aria-label="delete"
                              onClick={(event: any) => this.onModuleDelete(moduleInfo.id)}
                            >
                              <DeleteIcon />
                            </IconButton>
                            <IconButton
                              edge="end"
                              aria-label="show"
                              onClick={(event: any) => this.onModuleShow(moduleInfo.id)}
                            >
                              <ShowChartIcon />
                            </IconButton>
                          </ListItemSecondaryAction>
                        </ListItem>
                      )}
                    </Draggable>
                  ))}
                  {provided.placeholder}
                </List>
              </RootRef>
            )}
          </Droppable>
        </div>
      </DragDropContext>
      //   </Drawer>
    )
  }
}
export default PipelineEditor
