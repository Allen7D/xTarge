<template>
  <div class="user">
    <div>
      <el-button type="primary" icon="el-icon-circle-plus" @click="addUserVisible = true"> 添加管理员</el-button>
    </div>
    <el-table ref="multipleTable" :data="userList" tooltip-effect="dark"
              style="width: 1000px" height="800" border @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55">
      </el-table-column>
      <el-table-column prop="id" label="ID" width="80">
      </el-table-column>
      <el-table-column prop="username" label="登录名" width="150" show-overflow-tooltip>
      </el-table-column>
      <el-table-column prop="pass" label="密码" width="150" show-overflow-tooltip>
      </el-table-column>
      <el-table-column prop="level" label="权限" width="80" show-overflow-tooltip>
      </el-table-column>
      <el-table-column label="注册日期">
        <template slot-scope="scope">
          <i class="el-icon-time"></i><span style="margin-left: 10px">{{ scope.row.date }}</span>
        </template>
      </el-table-column>
      <el-table-column width="200" label="操作">
        <template slot-scope="scope">
          <el-button size="mini" @click="intoEditor(scope.$index, scope.row)">编辑
          </el-button>
          <el-button size="mini" type="danger" @click="handleDeleteUser(scope.$index, scope.row)">删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <div class="add-user">
      <el-dialog title="添加管理员" center :visible.sync="addUserVisible">
        <el-form :model="currentUser" status-icon :rules="registerRules" ref="currentUser">
          <el-form-item label="ID" prop="id" :label-width="formLabelWidth">
            <el-input v-model="currentUser.id" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="用户名" prop="username" :label-width="formLabelWidth">
            <el-input v-model="currentUser.username" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="密码" prop="pass" :label-width="formLabelWidth">
            <el-input type="password" v-model="currentUser.pass" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="确认密码" prop="checkPass" :label-width="formLabelWidth">
            <el-input type="password" v-model="currentUser.checkPass" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="权限级别" :label-width="formLabelWidth">
            <el-select v-model="currentUser.level" placeholder="请选择管理员权限">
              <el-option label="超级管理员: A级" value="A" v-if="opLevel <= 'A'"></el-option>
              <el-option label="高级管理员: B级" value="B" v-if="opLevel < 'B'"></el-option>
              <el-option label="普通管理员: C级" value="C"></el-option>
            </el-select>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="addUserVisible = false">取 消</el-button>
          <el-button type="primary" @click="handleAddUser(userList, currentUser)">确 定</el-button>
        </div>
      </el-dialog>
    </div>

    <div class="edit-user">
      <el-dialog title="修改管理员" center :visible.sync="editUserVisible">
        <el-form :model="currentUser" status-icon :rules="registerRules" ref="currentUser">
          <el-form-item label="ID" prop="id" :label-width="formLabelWidth">
            <el-input v-model="currentUser.id" auto-complete="off" :disabled="true"></el-input>
          </el-form-item>
          <el-form-item label="用户名" prop="username" :label-width="formLabelWidth">
            <el-input v-model="currentUser.username" auto-complete="off" :disabled="true"></el-input>
          </el-form-item>
          <el-form-item label="新密码" prop="pass" :label-width="formLabelWidth">
            <el-input type="password" v-model="currentUser.pass" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="确认新密码" prop="checkPass" :label-width="formLabelWidth">
            <el-input type="password" v-model="currentUser.checkPass" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="权限级别" :label-width="formLabelWidth">
            <el-select v-model="currentUser.level" placeholder="请选择管理员权限">
              <el-option label="超级管理员: A级" value="A" v-if="opLevel <= 'A'"></el-option>
              <el-option label="高级管理员: B级" value="B" v-if="opLevel < 'B'"></el-option>
              <el-option label="普通管理员: C级" value="C"></el-option>
            </el-select>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="editUserVisible = false">取 消</el-button>
          <el-button type="primary" @click="handleEditUser(currentUser)">确 定</el-button>
        </div>
      </el-dialog>
    </div>

  </div>
</template>

<script type="text/ecmascript-6">
  import axios from 'axios'
  import UserEditor from './components/userEditor.vue'

  export default {
    components: {
      UserEditor
    },
    data() {
      var validatePass = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请输入密码'))
        } else {
          if (this.form.checkPass !== '') {
            this.$refs.form.validateField('checkPass')
          }
          callback()
        }
      }
      var validatePass2 = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请再次输入密码'))
        } else if (value !== this.form.pass) {
          callback(new Error('两次输入密码不一致!'))
        } else {
          callback()
        }
      }
      return {
        registerRules: {
          pass: [
            {validator: validatePass, trigger: 'blur'}
          ],
          checkPass: [
            {validator: validatePass2, trigger: 'blur'}
          ]
        },
        formLabelWidth: '120px',
        userList: [],
        currentUser: {
          id: '',
          username: '',
          pass: '',
          checkPass: '',
          level: ''
        },
        multipleSelection: [],
        addUserVisible: false,
        editUserVisible: false,
        opLevel: localStorage['level']
      }
    },
    methods: {
      getUserData() {
        axios.get('/api/v1.0/users')
          .then((res) => {
            res.data.users.forEach((item, index) => {
              this.userList.push({
                id: item.user_id,
                date: item.register_time,
                username: item.username,
                pass: '******',
                level: item.level
              })
            })
          })
      },
      notify(message) {
        this.$notify({title: '警告', message: message, type: 'warning'})
      },
      message(type, message) {
        this.$message({type: type, message: message})
      },
      handleSelectionChange(val) {
        this.multipleSelection = val
      },
      intoEditor(index, row) {
        if (parseInt(localStorage['id']) !== parseInt(row.id)) {
          if (localStorage['level'] && localStorage['level'] >= row.level) {
            this.notify('当前用户的权限不够，无法进行相应的操作！')
            return false
          } else {
            this.currentUser.id = row.id
            this.currentUser.username = row.username
            this.currentUser.level = row.level
            this.editUserVisible = true
          }
        }
      },
      handleDeleteUser(index, row) {
        if (localStorage['level'] && localStorage['level'] >= row.level) {
          this.notify('当前用户的权限不够，无法进行相应的操作！')
          return false
        }
        this.$confirm('此操作将永久删除该账户, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          axios.delete(`/api/v1.0/users/${row.id}`).then((res) => {
            this.message('success', '删除成功!')
            this.userList.splice(index, 1)
          })
        }).catch(() => {
          this.message('info', '已取消删除')
        })
      },
      handleAddUser(arr, item) {
        if (!(item.id && item.username && item.pass && item.level)) {
          this.notify('未填写完整信息，无法进行相应的操作！')
          return false
        }
        let postData = 'id=' + item.id + '&username=' + item.username + '&password=' + item.pass + '&level=' + item.level
        axios.post('/api/v1.0/users', postData, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        }).then(res => {
          arr.push({
            id: item.id,
            date: (new Date()).toLocaleString(),
            username: item.username,
            pass: item.pass,
            level: item.level || 'C'
          })
        }).catch(err => {
          console.error(err)
        })
        this.addUserVisible = false
      },
      handleEditUser(row) {
        let postData = 'password=' + row.pass + '&level=' + row.level
        axios.put(`/api/v1.0/users/${row.id}`, postData, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        }).then(res => {
          // 刷新用户列表
          this.userList = []
          this.getUserData()
        })
          .catch(err => {
            console.error('更新失败:', err)
          })
        this.currentUser.id = ''
        this.currentUser.username = ''
        this.currentUser.level = ''
        this.editUserVisible = false
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
