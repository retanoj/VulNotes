import {
  SET_RECORDLIST,
  SET_RECORDSTATUS,
  UPDATE_RECORD,
  DEL_RECORD
} from '../mutation-types'

/*
id              int
vul_type_id     int
vul_name        string(1024)
vul_level       enum(string)
vul_status      enum(string)
vul_company     string(100)
vul_detail      string
vul_find_date   datetime
vul_solve_date  datetime
*/

const state = {
  RecordsList: []
}

const mutations = {
  [SET_RECORDLIST] (state, list) {
    state.RecordsList = list
  },
  [SET_RECORDSTATUS] (state, id, status) {
    for(var i=0; i<state.RecordsList.length; i++){
      if (state.RecordsList[i].id == id){
        state.RecordsList[i].vul_status = status
        break
      }
    }
  },
  [UPDATE_RECORD] (state, id, record) {
    for(var i=0; i<state.RecordsList.length; i++){
      if (state.RecordsList[i].id == id){
        state.RecordsList[i].vul_type_id    = record.vul_type_id
        state.RecordsList[i].vul_name       = record.vul_name
        state.RecordsList[i].vul_level      = record.vul_level
        state.RecordsList[i].vul_status     = record.vul_status
        state.RecordsList[i].vul_company    = record.vul_company
        state.RecordsList[i].vul_detail     = record.vul_detail
        state.RecordsList[i].vul_find_date  = record.vul_find_date
        state.RecordsList[i].vul_solve_date = record.vul_solve_date
        break
      }
    }
  },
  [DEL_RECORD] (state, id){
    for(var i in state.RecordsList){
      if (state.RecordsList[i].id == id){
        state.RecordsList.splice(i, 1)
      }
    }
  }
}

export default {
  state,
  mutations
}
