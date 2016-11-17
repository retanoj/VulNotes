/* eslint-disable no-unused-vars */
import 'font-awesome/less/font-awesome.less'
import 'bootstrap/less/bootstrap.less'
import 'vue-toast/dist/vue-toast.min.css'
import 'bootstrap-datetimepicker/css/bootstrap-datetimepicker.min.css'
import 'summernote/dist/summernote.css'

import 'bootstrap/dist/js/bootstrap'
import 'bootstrap-datetimepicker/js/bootstrap-datetimepicker'
import 'bootstrap-datetimepicker/js/locales/bootstrap-datetimepicker.zh-CN'
import 'summernote/dist/summernote.min.js'

import Vue from 'vue'
import VueRouter from 'vue-router'
import VueValidator from 'vue-validator'
import VueResource from 'vue-resource'
import { configRouter } from './router'

import App from './App'
import filters from './filters'
import { auth } from './interceptors/jwtAuth'

/* eslint-disable no-new */
Object.keys(filters).forEach(k => Vue.filter(k, filters[k]))
Vue.use(VueRouter)
Vue.use(VueResource)

export var router = new VueRouter({
    history: false,
    saveScrollPosition: true
})
configRouter(router)

Vue.http.interceptors.push(auth(router))
router.start(App, '#app')
console.log('Welcome!')

