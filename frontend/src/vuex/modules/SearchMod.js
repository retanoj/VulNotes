import {
  SET_KEYWORD_FIELD
} from '../mutation-types'

const state = {
  Keyword: null,
  Field:   null
}

const mutations = {
  [SET_KEYWORD_FIELD] (state, kw, f){
    state.Keyword = kw
    state.Field = f
  }
}

export default {
  state,
  mutations
}
