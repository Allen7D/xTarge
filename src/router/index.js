import Vue from 'vue';
import Router from 'vue-router';
import VueResource from 'vue-resource';
import VueSocketio from 'vue-socket.io';
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';

import Login from 'components/login/login';
import Admin from 'components/admin/admin';
import User from 'components/admin/user';
import OpLog from 'components/admin/opLog';
import AlertLog from 'components/admin/alertLog';
import Home from 'components/home/index';
import Iec104 from 'components/home/iec104';
import Modbus from 'components/home/modbus';

import Test from 'components/test/test';

Vue.use(Router);
Vue.use(VueResource);
Vue.use(VueSocketio, 'http://localhost:5000');
Vue.use(ElementUI);

const routes = [{
  path: '/login',
  name: 'Login',
  component: Login,
  alias: '/'
}, {
  path: '/',
  name: 'Admin',
  component: Admin,
  children: [
    { path: '/admin/user', component: User },
    { path: '/admin/oplog', component: OpLog },
    { path: '/admin/alertlog', component: AlertLog }
  ]
}, {
  path: '/',
  name: 'Home',
  component: Home,
  children: [
    { path: '/modbus', component: Modbus },
    { path: '/iec104', component: Iec104 }
  ]
}, {
  path: '/test',
  name: 'Test',
  component: Test
}];

export default new Router({
  linkActiveClass: 'active',
  mode: 'history',
  routes
});
