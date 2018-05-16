<template>
  <div class="header">
    <a class="logo" href="/modbus"><img src="./logo.jpg" alt="首页"></a>
    <h1 class="title">安全协议栈配置与监控界面</h1>
    <el-menu class="navbar" mode="horizontal">
      <div class="right-menu">
        <el-dropdown class="avatar-container right-menu-item" trigger="click">
          <div class="avatar-wrapper">
            <img class="user-avatar" :src="logo">
            <i class="el-icon-caret-bottom"></i>
          </div>
          <el-dropdown-menu slot="dropdown">
              <el-dropdown-item>
                <span @click="toAdmin" style="display:block">后台管理</span>
              </el-dropdown-item>
            <el-dropdown-item>
              <span @click="toModbus" style="display:block">协议设置</span>
            </el-dropdown-item>
            <el-dropdown-item divided>
              <span @click="logout" style="display:block">退出登录</span>
            </el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </div>
    </el-menu>
  </div>
</template>

<script type="text/ecmascript-6">
  import logo from './logo.png'
  export default {
    data() {
      return {
        name: '',
        avata: '',
        logo
      }
    },
    methods: {
      toAdmin() {
        this.$router.push('/admin/user')
      },
      toModbus() {
        this.$router.push('/modbus')
      },
      logout() {
        this.$router.push('/login')
      }
    }
  }
</script>

<style scoped lang="stylus" rel="stylesheet/stylus">
  .header
    padding: 20px 0 10px 30px
    display:flex
    justify-content: space-between
    align-items:center
    background: rgba(14, 32, 108, 1.0)
    .logo
      img
        width: 210px
        height: 50px
    .title
      margin-left: -100px
      font-size: 30px
      letter-spacing: 10px
      text-indent: 10px
      color: #fff
    .navbar
      height: 50px
      line-height: 50px
      border-radius: 0px !important
      background: 0
      border: 0
      .right-menu
        float: right
        height: 100%
        &:focus
          outline: none
        .right-menu-item
          display: inline-block
          margin: 0 8px
        .avatar-container
          height: 50px
          margin-right: 30px
          .avatar-wrapper
            cursor: pointer
            margin-top: 5px
            position: relative
            .user-avatar
              width: 40px
              height: 40px
              border-radius: 10px
            .el-icon-caret-bottom
              position: absolute
              right: -20px
              top: 25px
              font-size: 12px
</style>
