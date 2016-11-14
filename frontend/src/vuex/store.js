import Vue from 'vue'
import Vuex from 'vuex'

import VulType from './modules/VulType'
// import Records from './modules/Records'
import Records from './modules/BriefRecords'

Vue.use(Vuex)

export default new Vuex.Store({
    modules: {
        Records,
        VulType
    }
})
