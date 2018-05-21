export default {
  username: localStorage['username'],
  level: localStorage['level'],
  currentUser: {
    id: '',
    username: '',
    level: ''
  },
  isLogin: localStorage['isLogin'] === 'true',
  iFuncCodes: {},
  mFuncCodes: {},
  mMemories: {},
  iec104: {
    currentCode: [],
    reserveCode: []
  },
  modbus: {
    currentCode: [],
    reserveCode: [],
    memory: []
  }
}
