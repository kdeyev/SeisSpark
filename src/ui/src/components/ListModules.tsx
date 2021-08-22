import React from 'react';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import ListItemAvatar from '@material-ui/core/ListItemAvatar';
import Avatar from '@material-ui/core/Avatar';
import ImageIcon from '@material-ui/icons/Image';
import {ModulesService} from '../services/suspark/services/ModulesService';

interface State {
    moduleTypes: Array<string>;
}

interface Props {
}

class ListModules extends React.Component<Props, State> {
    constructor(props: Props) {
        super(props);
        this.state = {moduleTypes: []}
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

    public render() {
        return (
            <List>
                {this.state.moduleTypes.map((moduleType: string) => (
                    <ListItem>
                        <ListItemAvatar>
                        <Avatar>
                            <ImageIcon />
                        </Avatar>
                        </ListItemAvatar>
                        <ListItemText primary={moduleType} 
                        //secondary="Jan 9, 2014" 
                        />
                    </ListItem>
                ))}
            </List>
        );
    }
}
export default ListModules;
