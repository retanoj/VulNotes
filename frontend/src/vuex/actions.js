import Vue from 'vue'
import * as types from './mutation-types'
import * as config from '../config'

var host_api = config.HOST_VUL_API

var vulnotelist = Vue.resource(host_api +'/vulnotelist')
var vultypelist = Vue.resource(host_api +'/vultypelist')
var vulstatus   = Vue.resource(host_api +'/vulstatus{/id}')
var vulnote     = Vue.resource(host_api +'/vulnote{/id}')
var vulcount    = Vue.resource(host_api +'/vulcount')
var vulnotebrieflist = Vue.resource(host_api +'/vulnotebrieflist')

var login       = Vue.resource(config.HOST_COMM_API +'/login')

// 登录
export const getLogin = () => {
  return login.query()
}

// 获取一条漏洞记录，按id
export const getVulRecord = ({dispatch}, id) => {
  return vulnote.query({id:id})
}

// 获取一组漏洞记录简要信息
export const loadBriefVulRecords = ({dispatch}, pageNum=1, pageSize=20) => {
  return vulnotebrieflist.get({'pageNum':pageNum, 'pageSize':pageSize}).then((resp) => {
    dispatch(types.SET_RECORDLIST, resp.json().data)
  })
}

// 搜索一组漏洞记录简要信息
export const searchBriefVulRecords = ({dispatch}, keyword=null, field=null, pageNum=1, pageSize=20) => {
  return vulnotebrieflist.get({'keyword':keyword, 'field':field, 'pageNum':pageNum, 'pageSize':pageSize}).then((resp) => {
    dispatch(types.SET_RECORDLIST, resp.json().data)
  })
}

// 获取漏洞记录总数
export const getVulRecordsCnt = ({dispatch}) => {
  return vulcount.get()
}

// 获取漏洞类型列表
export const getVulType = ({dispatch}) => {
  return vultypelist.get().then((resp) => {
    dispatch(types.SET_VULTYPELIST, resp.json().data)
  })
}

// 更改漏洞状态，按id
export const changeRecordStatus = ({dispatch}, id, status) => {
  return vulstatus.update({id:id}, {"status":status}).then((resp) => {
    dispatch(types.SET_RECORDSTATUS, id, status)
  })
}

// 删除一条漏洞，按id
export const deleteRecord = ({dispatch}, id) => {
  return vulnote.remove({id:id}).then((resp) => {
    dispatch(types.DEL_RECORD, id)
  })
}

// 更新一条漏洞，按id
export const updateRecord = ({dispatch}, id, record) => {
  return vulnote.update({id:id}, record).then((resp) => {
    dispatch(types.UPDATE_RECORD, id, record)
  })
}

// 插入一条漏洞，按id
export const insertRecord = ({dispatch}, record) => {
  return vulnotelist.save(record).then((_) => {
    vulnotebrieflist.get().then((resp) => {
      dispatch(types.SET_RECORDLIST, resp.json().data)
    })
  })
}

// 设置搜索Mod
export const setSearchMod = ({dispatch}, kw, f) => {
  dispatch(types.SET_KEYWORD_FIELD, kw, f)
}
