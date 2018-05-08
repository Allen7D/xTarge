<template>
  <el-dialog title="修改管理员" center>
    <el-form :model="admin" status-icon :rules="registerRules" ref="admin">
      <el-form-item label="ID" prop="id" :label-width="formLabelWidth">
        <el-input v-model="admin.id" auto-complete="off" :disabled="true"></el-input>
      </el-form-item>
      <el-form-item label="用户名" prop="username" :label-width="formLabelWidth">
        <el-input v-model="admin.username" auto-complete="off" :disabled="true"></el-input>
      </el-form-item>
      <el-form-item label="新密码" prop="pass" :label-width="formLabelWidth">
        <el-input type="password" v-model="admin.pass" auto-complete="off"></el-input>
      </el-form-item>
      <el-form-item label="确认新密码" prop="checkPass" :label-width="formLabelWidth">
        <el-input type="password" v-model="admin.checkPass" auto-complete="off"></el-input>
      </el-form-item>
      <el-form-item label="权限级别" :label-width="formLabelWidth">
        <el-select v-model="admin.level" placeholder="请选择管理员权限">
          <el-option label="超级管理员: A级" value="A" v-if="currentUser.level <= 'A'"></el-option>
          <el-option label="高级管理员: B级" value="B" v-if="currentUser.level < 'B'"></el-option>
          <el-option label="普通管理员: C级" value="C"></el-option>
        </el-select>
      </el-form-item>
    </el-form>
    <div slot="footer" class="dialog-footer">
      <el-button @click="isVisible = false">取 消</el-button>
      <el-button type="primary" @click="handleEditUser(admin)">确 定</el-button>
    </div>
  </el-dialog>
</template>

<script type="text/ecmascript-6">
  import axios from 'axios'
  export default {
    props: {
      admin: {
        type: Object
      },
      currentUser: {
        type: Object
      }
    },
    data() {
      return {
        isVisible: false
      }
    },
    methods: {
      handleVisible() {
        this.isVisible = !this.isVisible
      },
      handleEditUser(row) {
        let params = `password=${row.pass}&level=${row.level}`
        axios.put(`/api/v1.0/users/${row.id}`, params, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        }).then(res => {
          // 需要刷新用户列表
          console.log(res)
        }).catch(err => {
            console.error('更新失败:', err)
          })
        this.admin.id = ''
        this.admin.username = ''
        this.admin.level = ''
        this.isVisible = false
      }
    }
  }
</script>

<style scoped lang="stylus" rel="stylesheet/stylus">

</style>