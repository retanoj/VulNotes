import {
    SET_VULTYPELIST
} from '../mutation-types'

const state = {
  VulTypeList: []
}

const mutations = {
    [SET_VULTYPELIST] (state, list) {
        state.VulTypeList = list
    }
}

export default {
    state,
    mutations
}
