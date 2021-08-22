import React from 'react';

import ListItemAvatar from '@material-ui/core/ListItemAvatar';
import Avatar from '@material-ui/core/Avatar';
import Paper from '@material-ui/core/Paper'
import ImageIcon from '@material-ui/icons/Image';
import {ModulesService} from '../services/suspark/services/ModulesService';
import {
    List,
    ListItem,
    ListItemText,
    ListItemIcon,
    IconButton,
    ListItemSecondaryAction
  } from "@material-ui/core";
  import RootRef from "@material-ui/core/RootRef";
  import { DragDropContext, Droppable, Draggable, DropResult , ResponderProvided, DroppableProvided , DroppableStateSnapshot} from "react-beautiful-dnd";
  import InboxIcon from "@material-ui/icons/Inbox";
  import EditIcon from "@material-ui/icons/Edit";
  import {ModuleInfo} from '../services/suspark/models/ModuleInfo';
  
  const getItemStyle = (isDragging: boolean, draggableStyle: any) => ({
    // styles we need to apply on draggables
    ...draggableStyle,
  
    ...(isDragging && {
      background: "rgb(235,235,235)"
    })
  });

  interface State {
    moduleTypes: Array<string>;
    modules: Array<ModuleInfo>;
}

interface Props {
}

class PipelineEditor extends React.Component<Props, State> {
    constructor(props: Props) {
        super(props);
        this.state = {moduleTypes: [], modules: []}
        this.loadModules();
    }
    private loadModules() {
        ModulesService.getModulesApiV1ModulesGet()
            .then((moduleTypes: Array<string>) => {
                this.setState({moduleTypes: moduleTypes})
            })
            .catch((error: string) => {
                console.error(error);
            });
    }
 
    private onDragEnd(result: DropResult, provided: ResponderProvided) {
        const { source, destination } = result;

        // dropped outside the list
        if (!destination) {
            return;
        }

        switch (source.droppableId) {
            case "moduleTypes":
                this.setState({});
            break;
            case "pipeline":
                this.setState({});
            break;
        }
    }

    public render() {
        return (
        <DragDropContext onDragEnd={this.onDragEnd}>
            <Droppable droppableId="moduleTypes">
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
                        {...provided.dragHandleProps}>
                            <ListItemAvatar>
                            <Avatar>
                                {/* <ImageIcon /> */}
                            </Avatar>
                            </ListItemAvatar>
                            <ListItemText primary={moduleType} 
                            //secondary="Jan 9, 2014" 
                            />
                        </ListItem>
                        {snapshot.isDragging && (
                            <ListItem >
                                <ListItemAvatar>
                                <Avatar>
                                </Avatar>
                                </ListItemAvatar>
                                <ListItemText primary={moduleType} 
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
            <Paper>
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
                                <Avatar>
                                    {/* <ImageIcon /> */}
                                </Avatar>
                                </ListItemAvatar>
                                <ListItemText primary={moduleInfo} 
                                //secondary="Jan 9, 2014" 
                                />
                            </ListItem>
                                )}
                            </Draggable>
                            ))}
                            {provided.placeholder}
                        </List>
                    </RootRef>
                    )}
                </Droppable>
            </Paper>
            
        </DragDropContext>
                
        );
    }
}
export default PipelineEditor;
