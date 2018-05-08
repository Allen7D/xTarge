// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
// import VueAxios from 'vue-axios'
import router from './router/index'
import createStore from './store/index'
import App from './App'

// Vuex 进行状态管理
Vue.use(Vuex)
// 用 axios 进行 Ajax 请求
Vue.use(axios)
/* eslint-disable no-new */

const store = createStore()

new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App)
})
