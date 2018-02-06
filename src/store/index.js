import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    username: localStorage['username'] || '',
    isLogin: localStorage['isLogin'] === 'true'
  },
    mutations: {
    updateUserInfo (state, username) {
      state.username = username;
    },
    switchLogin(state, bool) {
      state.isLogin = bool;
    }
  }
});
