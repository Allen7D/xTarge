<template>
  <div class="login">
    <div class="main">
      <div class="logo">
        <img src="./logo.png" alt="logo">
      </div>
      <div class="title">
        <span>管理员登录</span>
      </div>
      <div class="content">
        <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
          <el-form-item prop="username">
            <el-input v-model.number="ruleForm.username" placeholder="用户名"></el-input>
          </el-form-item>
          <el-form-item prop="pass">
            <el-input type="password" v-model="ruleForm.pass" auto-complete="off" placeholder="密码"></el-input>
          </el-form-item>
          <el-form-item class="button">
            <el-button type="primary" @click="submitForm('ruleForm')">登录</el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
    <div class="bg">
    </div>
  </div>
</template>

<script type="text/ecmascript-6">
  import {mapState} from 'vuex'
  import { authLogin } from '@/api/auth'
  export default {
    data() {
      var checkUsername = (rule, value, callback) => {
        if (!value) {
          return callback(new Error('用户名不能为空'))
        } else {
          callback()
        }
      }
      var validatePass = (rule, value, callback) => {
        if (value === '') {
          return callback(new Error('请输入密码'))
        } else {
          callback()
        }
      }
      return {
        ruleForm: {
          username: '',
          pass: ''
        },
        rules: {
          username: [
            {validator: checkUsername, trigger: 'blur'}
          ],
          pass: [
            {validator: validatePass, trigger: 'blur'}
          ]
        }
      }
    },
    computed: {
      ...mapState(['isLogin'])
    },
    methods: {
      handleLoginError() {
        this.$notify.error({title: '错误', message: '账号密码错误'})
        this.$router.push('/login')
      },
      submitForm(formName) {
        const formData = 'username=' + this.ruleForm.username + '&password=' + this.ruleForm.pass
        authLogin(formData).then((res) => {
          const data = res.data
          this.$store.commit('updateUserInfo', data)
          this.$store.commit('switchLogin', true)

          localStorage['username'] = data.name
          localStorage['level'] = data.level
          localStorage['id'] = data._id
          localStorage['isLogin'] = true

          this.$router.push('/modbus')
        }).catch((err) => {
          this.loginStatus = err
          console.log('err', err)
          this.handleLoginError()
        })
      }
    }
  }
</script>

<style lang="stylus" rel="stylesheet/stylus">
  .login
    .main
      top: 0
      left: 0
      right: 0
      bottom: 0
      margin: auto
      position: absolute
      height 400px
      width: 500px
      border-radius: 10px
      text-align: center
      padding-top: 30px
      background: rgb(255,255,255)
      z-index: 1
      .logo img
        width: 70px
        border-radius: 50%
        border: 1px solid rgba(14, 32, 108, 0.4)
        margin: 5px auto
      .title
        font-size: 20px
        letter-spacing: 2px
        margin: 5px auto 30px
      .content
        margin: 0 80px 0 -20px
        .button
          margin-top: 50px
          .el-button
            width: 250px
            background-color: rgba(14, 32, 108, 1.0)
            font-size: 20px
            letter-spacing: 20px
            text-indent: 20px
    .bg
      top: 0
      left: 0
      right: 0
      bottom: 0
      margin: auto
      position: absolute
      background-size: cover
      background-repeat: no-repeat
      background-image: url(./background.jpg)
</style>
