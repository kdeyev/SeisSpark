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
import AddBox from '@material-ui/icons/AddBox'
import ArrowUpward from '@material-ui/icons/ArrowUpward'
import Check from '@material-ui/icons/Check'
import ChevronLeft from '@material-ui/icons/ChevronLeft'
import ChevronRight from '@material-ui/icons/ChevronRight'
import Clear from '@material-ui/icons/Clear'
import DeleteOutline from '@material-ui/icons/DeleteOutline'
import Edit from '@material-ui/icons/Edit'
import FilterList from '@material-ui/icons/FilterList'
import FirstPage from '@material-ui/icons/FirstPage'
import LastPage from '@material-ui/icons/LastPage'
import Refresh from '@material-ui/icons/Refresh'
import Remove from '@material-ui/icons/Remove'
import SaveAlt from '@material-ui/icons/SaveAlt'
import Search from '@material-ui/icons/Search'
import ViewColumn from '@material-ui/icons/ViewColumn'
import MaterialTable, { Icons, Query, QueryResult } from 'material-table'
import React, { forwardRef } from 'react'

import { PipelineInfo } from '../services/seisspark'
import { CreatePipelineRequest } from '../services/seisspark/models/CreatePipelineRequest'
import { PipelinesService } from '../services/seisspark/services/PipelinesService'

interface TableRef {
  onQueryChange: () => void
}

const tableIcons: Icons = {
  Add: forwardRef((props, ref) => <AddBox {...props} ref={ref} />),
  Check: forwardRef((props, ref) => <Check {...props} ref={ref} />),
  Clear: forwardRef((props, ref) => <Clear {...props} ref={ref} />),
  Delete: forwardRef((props, ref) => <DeleteOutline {...props} ref={ref} />),
  DetailPanel: forwardRef((props, ref) => <ChevronRight {...props} ref={ref} />),
  Edit: forwardRef((props, ref) => <Edit {...props} ref={ref} />),
  Export: forwardRef((props, ref) => <SaveAlt {...props} ref={ref} />),
  Filter: forwardRef((props, ref) => <FilterList {...props} ref={ref} />),
  FirstPage: forwardRef((props, ref) => <FirstPage {...props} ref={ref} />),
  LastPage: forwardRef((props, ref) => <LastPage {...props} ref={ref} />),
  NextPage: forwardRef((props, ref) => <ChevronRight {...props} ref={ref} />),
  PreviousPage: forwardRef((props, ref) => <ChevronLeft {...props} ref={ref} />),
  ResetSearch: forwardRef((props, ref) => <Clear {...props} ref={ref} />),
  Search: forwardRef((props, ref) => <Search {...props} ref={ref} />),
  SortArrow: forwardRef((props, ref) => <ArrowUpward {...props} ref={ref} />),
  ThirdStateCheck: forwardRef((props, ref) => <Remove {...props} ref={ref} />),
  ViewColumn: forwardRef((props, ref) => <ViewColumn {...props} ref={ref} />),
}

interface State {
  // moduleTypes: Array<string>;
}

interface Props {
  onSelectPipeline: (pipelineID: string) => void
}

class PipelineTable extends React.Component<Props, State> {
  ref = React.createRef<TableRef>()

  constructor(props: Props) {
    super(props)
    this.state = {}
    // this.loadModules();
  }

  private onRawSelected(data: PipelineInfo | undefined) {
    if (data) {
      this.props.onSelectPipeline(data.id)
    }
  }

  private queryData(query: Query<PipelineInfo>): Promise<QueryResult<PipelineInfo>> {
    return new Promise((resolve, reject) => {
      PipelinesService.getPipelinesApiV1PipelinesGet()
        .then((pipelines: Array<PipelineInfo>) => {
          resolve({
            data: pipelines,
            page: query.page,
            totalCount: pipelines.length,
          })
        })
        .catch((error: string) => {
          console.error(error)
          reject()
        })
    })
  }
  public render() {
    return (
      <MaterialTable
        title="Pipelines"
        onRowClick={(event, rowData) => this.onRawSelected(rowData)}
        icons={tableIcons}
        columns={[
          {
            title: 'Pipeline Name',
            field: 'name',
            // render: rowData => (
            //   <img
            //     style={{ height: 36, borderRadius: '50%' }}
            //     src={rowData.avatar}
            //   />
            // ),
          },
          { title: 'Id', field: 'id', editable: 'never' },
        ]}
        data={this.queryData}
        editable={{
          onRowAdd: (newData) =>
            new Promise((resolve, reject) => {
              let request = { name: newData.name } as CreatePipelineRequest

              PipelinesService.createPipelinesApiV1PipelinesPost(request)
                .then((pipelineInfo: PipelineInfo) => {
                  resolve(pipelineInfo)
                  this.onRawSelected(pipelineInfo)
                })
                .catch((error: string) => {
                  console.error(error)
                  reject()
                })
            }),
          // onRowUpdate: (newData, oldData) =>
          //     new Promise((resolve, reject) => {
          //     }),
          onRowDelete: (oldData) =>
            new Promise((resolve, reject) => {
              PipelinesService.deletePipelineApiV1PipelinesPipelineIdDelete(oldData.id)
                .then((some: any) => {
                  resolve(some)
                })
                .catch((error: string) => {
                  console.error(error)
                  reject()
                })
            }),
        }}
        tableRef={this.ref}
        actions={[
          {
            icon: () => <Refresh />,
            tooltip: 'Refresh Data',
            isFreeAction: true,
            onClick: () => {
              if (this.ref.current) {
                this.ref.current.onQueryChange()
              }
            },
          },
        ]}
      />
    )
  }
}

export default PipelineTable
