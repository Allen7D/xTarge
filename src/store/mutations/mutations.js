export default {
  updateUserInfo(state, user) {
    state.username = user.name
    state.level = user.level
  },
  switchLogin(state, bool) {
    state.isLogin = bool
  },
  fetchIFuncCodes(state, iFuncCodes) {
    state.iFuncCodes = iFuncCodes
  },
  fetchMFuncCodes(state, mFuncCodes) {
    state.mFuncCodes = mFuncCodes
  },
  fetchMMemories(state, mMemories) {
    state.mMemories = mMemories
  },
  updateIec104(state, data) {
    state.iec104.currentCode = data
  },
  fetchIec104(state, data) {
    state.iec104 = data
  },
  updateModbus(state, data) {
    state.modbus.currentCode = data
  },
  fetchModbus(state, data) {
    state.modbus = data
  }
}
