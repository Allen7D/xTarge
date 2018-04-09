export default {
  updateUserInfo (state, user) {
    state.username = user.name;
    state.level = user.level;
  },
  switchLogin(state, bool) {
    state.isLogin = bool;
  },
  fetchIFuncCodes (state, iFuncCodes) {
    state.iFuncCodes = iFuncCodes;
  },
  fetchMFuncCodes (state, mFuncCodes) {
    state.mFuncCodes = mFuncCodes;
  },
  fetchMMemories (state, mMemories) {
    state.mMemories = mMemories;
  }
};
