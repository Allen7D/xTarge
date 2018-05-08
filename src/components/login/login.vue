<template>
  <div class="bg">
    <div class="login">
      <div class="logo"><img src="./logo.png" alt="logo"></div>
      <div class="title"><span>管理员登录</span></div>
      <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" label-width="100px"
               class="demo-ruleForm">
        <el-form-item prop="username">
          <el-input v-model.number="ruleForm.username" placeholder="用户名"></el-input>
        </el-form-item>
        <el-form-item prop="pass">
          <el-input type="password" v-model="ruleForm.pass" auto-complete="off" placeholder="密码"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm('ruleForm')">登录</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script type="text/ecmascript-6">
  import {mapState} from 'vuex'

  import axios from 'axios'
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
        this.$notify.error({
          title: '错误',
          message: '账号密码错误'
        })
        this.$router.push('/login')
      },
      submitForm(formName) {
        let postData = 'username=' + this.ruleForm.username + '&password=' + this.ruleForm.pass
        axios.post('http://127.0.0.1:5000/login', postData, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        }).then((res) => {
          console.log('登录', res)
          this.$store.commit('updateUserInfo', res.data)
          this.$store.commit('switchLogin', true)

          localStorage['username'] = res.data.name
          localStorage['level'] = res.data.level
          localStorage['id'] = res.data._id
          localStorage['isLogin'] = true

          this.$router.push('/modbus')
        }).catch(() => {
          this.handleLoginError()
        })
      }
    }
  }
</script>

<style lang="stylus" rel="stylesheet/stylus">
  .bg
    top: 0
    left: 0
    width: 100%
    height: 100%
    padding-top: 10%
    background-size: cover
    background-repeat: no-repeat
    background-image: url(./background.jpg)

  .login
    width: 400px
    padding: 20px 90px 100px 0
    margin: 0 auto
    border-radius: 10px
    text-align: center //内部居中
    background-color: white
    .logo
      img
        width: 70px
        border-radius: 50%
        border: 1px solid rgba(14, 32, 108, 0.4)
        padding: 5px
        margin-left: 100px
    .title
      font-size: 16px
      letter-spacing: 1px
      text-indent: 1px
      margin-bottom: 22px
      margin-left: 100px
    .el-button
      width: 300px
      background-color: rgba(14, 32, 108, 1.0)
      font-size: 20px
      letter-spacing: 20px
      text-indent: 20px

</style>
