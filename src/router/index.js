import Vue from 'vue'
import Router from 'vue-router'
import VueResource from 'vue-resource'
import VueSocketio from 'vue-socket.io'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'

import Login from 'components/login/login'
import AdminLayout from 'views/admin/layout'
import User from 'views/admin/user'
import Operate from 'views/admin/operate'
import Alert from 'views/admin/alert'
import Home from 'components/home/index'
import Iec104 from 'components/home/iec104'
import Modbus from 'components/home/modbus'

Vue.use(Router)
Vue.use(VueResource)
Vue.use(VueSocketio, 'http://localhost:5000')
Vue.use(ElementUI)

const routes = [{
  path: '/login',
  name: 'Login',
  component: Login,
  alias: '/'
}, {
  path: '/',
  name: '日志管理',
  component: AdminLayout,
  children: [
    { path: '/admin/operate', component: Operate, name: '操作日志' },
    { path: '/admin/alert', component: Alert, name: '报警日志' }
  ]
}, {
  path: '/',
  name: '用户管理',
  component: AdminLayout,
  children: [
    { path: '/admin/user', component: User, name: '用户列表' }
  ]
}, {
  path: '/',
  name: 'Home',
  component: Home,
  children: [
    { path: '/modbus', component: Modbus },
    { path: '/iec104', component: Iec104 }
  ]
}]

export default new Router({
  linkActiveClass: 'active',
  mode: 'history',
  routes
})
