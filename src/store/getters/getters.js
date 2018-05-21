export default {
  fullName (state) {
    let level = ''
    if (state.level === 'A') {
      level = '超'
    } else if (state.level === 'B') {
      level = '高'
    } else {
      level = '普'
    }
    return `${state.username}  (${level})`
  },
  totalIec104Code (state) {
    return state.iec104.currentCode.concat(state.iec104.reserveCode)
  },
  totalModbusCode (state) {
    return state.modbus.currentCode.concat(state.modbus.reserveCode)
  }
}
