<template>
  <div class="user">
    <div>
      <el-button type="primary" icon="el-icon-circle-plus" @click="handleCreate"> 添加管理员</el-button>
    </div>
    <el-table ref="multipleTable" :data="userList" tooltip-effect="dark" height="800" border>
      <el-table-column type="selection" width="55"></el-table-column>
      <el-table-column prop="id" label="ID" width="80"></el-table-column>
      <el-table-column prop="username" label="登录名" width="150" show-overflow-tooltip></el-table-column>
      <el-table-column prop="password" label="密码" width="150" show-overflow-tooltip></el-table-column>
      <el-table-column prop="level" label="权限" width="80" show-overflow-tooltip></el-table-column>
      <el-table-column label="注册日期">
        <template slot-scope="scope">
          <i class="el-icon-time"></i><span style="margin-left: 10px">{{ scope.row.date }}</span>
        </template>
      </el-table-column>
      <el-table-column width="200" label="操作">
        <template slot-scope="scope">
          <el-button size="mini" @click="handleUpdate(scope.row)">编辑</el-button>
          <el-button size="mini" @click="handleDelete(scope.$index, scope.row)" type="danger">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <user-editor :show.sync="show" @update="getUserData" :dialogStatus="dialogStatus" :dataForm="tempUser" :currentLevel="currentUser.level"></user-editor>

  </div>
</template>

<script type="text/ecmascript-6">
  import { fetchUser, deleteUser } from '@/api/user'
  import UserEditor from './components/userEditor.vue'

  export default {
    components: {
      UserEditor
    },
    data() {
      return {
        userList: [],
        dialogStatus: '',
        show: false,
        currentUser: {id: localStorage['id'], level: localStorage['level']},
        tempUser: {id: '', username: '', password: '', checkPass: '', level: ''}
      }
    },
    methods: {
      getUserData() {
        this.userList = []
        fetchUser().then(res => {
          res.data.users.forEach((item, index) => {
            this.userList.push({
              id: item.user_id,
              date: item.register_time,
              username: item.username,
              password: '******',
              level: item.level
            })
          })
        })
      },
      notify(message) {
        this.$notify({title: '警告', message: message, type: 'warning', duration: 2000})
      },
      message(type, message) {
        this.$message({type: type, message: message})
      },
      resetTemp() {
        this.tempUser = {id: '', username: '', password: '', checkPass: '', level: ''}
      },
      handleCreate() {
        this.resetTemp()
        this.dialogStatus = 'create'
        this.show = true
        this.$nextTick(() => {
          this.$refs['dataForm'].clearValidate()
        })
      },
      handleUpdate(row) {
        let cUser = this.currentUser
        if (parseInt(cUser.id) !== parseInt(row.id)) {
          if (cUser.level && cUser.level >= row.level) {
            this.notify('当前用户的权限不够，无法进行相应的操作！')
            return
          }
        }
        this.tempUser = Object.assign({}, row)
        this.tempUser.password = ''
        this.dialogStatus = 'update'
        this.show = true
        this.$nextTick(() => {
          this.$refs['dataForm'].clearValidate()
        })
      },
      handleDelete(index, row) {
        if (localStorage['level'] && localStorage['level'] >= row.level) {
          this.notify('当前用户的权限不够，无法进行相应的操作！')
          return false
        }
        this.$confirm('此操作将永久删除该账户, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          deleteUser(row.id).then((res) => {
            this.message('success', '删除成功!')
            this.userList.splice(index, 1)
          })
        }).catch(() => {
          this.message('info', '已取消删除')
        })
      }
    },
    mounted() {
      this.getUserData()
    }
  }
</script>

<style lang="stylus" rel="stylesheet/stylus">
  .user
    width: 100%
    .el-button
      margin-bottom: 10px
</style>
