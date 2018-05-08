export default {
  fullName (state) {
    let level = ''
    if (state.level === 'A') {
      level = '超级管理员'
    } else if (state.level === 'B') {
      level = '高级管理员'
    } else {
      level = '普通管理员'
    }
    return `${state.username}  (${level})`
  }
}
