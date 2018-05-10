<template>
  <el-dialog :title="textMap[dialogStatus]" center :visible.sync="isVisible" @close="hideForm">
    <el-form :model="dataForm" ref="dataForm" status-icon :rules="formRules" label-position="right" label-width="100px" style="width: 400px; margin-left:50px">
      <el-form-item label="ID" prop="id">
        <el-input v-model="dataForm.id" auto-complete="off" :disabled="disabled"></el-input>
      </el-form-item>
      <el-form-item label="用户名" prop="username">
        <el-input v-model="dataForm.username" auto-complete="off" :disabled="disabled"></el-input>
      </el-form-item>
      <el-form-item label="新密码" prop="password">
        <el-input type="password" v-model="dataForm.password" auto-complete="off"></el-input>
      </el-form-item>
      <el-form-item label="确认新密码" prop="checkPass">
        <el-input type="password" v-model="dataForm.checkPass" auto-complete="off"></el-input>
      </el-form-item>
      <el-form-item label="权限级别">
        <el-select v-model="dataForm.level" placeholder="请设置管理员权限">
          <el-option v-for="(item, index) in adminLevel" v-if="currentLevel <= item.level"
                     :label="item.name" :value="item.level" :key="index"></el-option>
        </el-select>
      </el-form-item>
    </el-form>
    <div slot="footer" class="dialog-footer">
      <el-button @click="hideForm">取 消</el-button>
      <el-button v-if="dialogStatus==='create'" type="primary" @click="createData">确 定</el-button>
      <el-button v-else type="primary" @click="updateData">确 定</el-button>
    </div>
  </el-dialog>
</template>

<script type="text/ecmascript-6">
  import { createUser, updateUser } from '@/api/user'
  export default {
    props: {
      dataForm: {
        type: Object
      },
      show: {
        type: Boolean,
        default: false
      },
      dialogStatus: {
        type: String
      },
      currentLevel: {
        type: String
      }
    },
    data() {
      var validatePass = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请输入密码'))
        } else {
          if (this.dataForm.checkPass !== '') {
            this.$refs.dataForm.validateField('checkPass')
          }
          callback()
        }
      }
      var validatePass2 = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请再次输入密码'))
        } else if (value !== this.dataForm.password) {
          callback(new Error('两次输入密码不一致!'))
        } else {
          callback()
        }
      }
      return {
        formRules: {
          password: [
            {validator: validatePass, trigger: 'blur'}
          ],
          checkPass: [
            {validator: validatePass2, trigger: 'blur'}
          ]
        },
        isVisible: this.show,
        textMap: {
          update: '修改管理员',
          create: '添加管理员'
        },
        adminLevel: [
          {name: '超级管理员: A级', level: 'A'},
          {name: '高级管理员: B级', level: 'B'},
          {name: '普通管理员: C级', level: 'C'}
        ]
      }
    },
    computed: {
      disabled() {
        return this.dialogStatus === 'update'
      }
    },
    watch: {
      show() {
        this.isVisible = this.show
      }
    },
    methods: {
      hideForm() {
        this.$emit('update:show', false)
      },
      sendUpdate() {
        this.$emit('update')
        this.hideForm()
      },
      createData() {
        let item = this.dataForm
        this.$refs['dataForm'].validate((valid) => {
          if (valid) {
            let postData = `id=${item.id}&username=${item.username}&password=${item.password}&level=${item.level}`
            createUser(postData).then(() => {
              this.sendUpdate()
              this.$notify({title: '成功', message: '创建成功', type: 'success', duration: 2000})
            })
          } else {
            this.$notify({title: '警告', message: '提交失败！请重新校验表单数据', type: 'warning', duration: 2000})
          }
        })
      },
      updateData() {
        let item = this.dataForm
        this.$refs['dataForm'].validate((valid) => {
          if (valid) {
            let postData = `password=${item.password}&level=${item.level}`
            updateUser(item.id, postData).then(res => {
              this.sendUpdate()
              this.$notify({title: '成功', message: '更新成功', type: 'success', duration: 2000})
            }).catch(err => {
              console.error('更新失败:', err)
            })
          } else {
            this.$notify({title: '警告', message: '提交失败！请重新校验表单数据', type: 'warning', duration: 2000})
          }
        })
      }
    }
  }
</script>

<style scoped lang="stylus" rel="stylesheet/stylus">

</style>