<template>
  <div class="protocol">
    <nav class="title">
      <i class="el-icon-setting"></i>
      配置 <span>(配置方式：选择限制的功能，完成后选择发送)</span>
    </nav>
    <div class="protocol-content">
      <el-form :model="configForm" ref="configForm" label-width="10px" class="demo-dynamic">
        <!--报警连接-->
        <v-connection :connection="configForm.connection"></v-connection>
        <!--功能码限制-->
        <m-limit :fc_options="fc_options" :m_options="m_options" :restrictions="configForm.restrictions"
                 :connection="configForm.connection"></m-limit>
      </el-form>
      <div class="command">
        <el-button type="text" @click="showConfig">功能码添加</el-button>
        <el-button type="text" @click="isShowDetail = true">显示</el-button>
        <el-button type="text" @click="verifyForm">验证</el-button>
        <el-button type="text" @click="submitForm">发送</el-button>
      </div>
    </div>

    <nav class="title">
      <i class="el-icon-setting"></i>监控 <span>(监控界面：每当设备收到不符合配置的数据包，信息将显示)</span>
    </nav>
    <div class="modbus-content">
      <alert-info :alertData="list" protocolType="modbus"></alert-info>
      <div class="pagination-container">
        <el-pagination background @size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page.sync="listQuery.page"
                       :page-sizes="[10, 20, 30, 50]" :page-size="listQuery.limit" layout="total, sizes, prev, pager, next, jumper" :total="total">
        </el-pagination>
      </div>
    </div>

    <config-detail :isShow.sync="isShowDetail" :configForm="configForm"
                :currentCode="currentCode" :modbusMemory="memory"></config-detail>
    <code-transfer :isShow.sync="isShowConfig" :updateCode="updateCode"
                 :currentCode="currentCode" :reserveCode="reserveCode"
    >
    </code-transfer>
  </div>
</template>

<script type="text/ecmascript-6">
  import connection from 'components/connection/connection'
  import alertInfo from './components/alertInfo'
  import mLimit from './mLimit'
  import UpdateFcn from './components/updateFcn'
  import FormatDate from 'components/time/formatDate'
  import ConfigDetail from './components/configDetail'
  import CodeTransfer from './components/codeTransfer'
  import { fetchAlert } from '@/api/alert'
  import { createOperate } from '@/api/operate'

  export default {
    components: {
      'v-connection': connection,
      'alert-info': alertInfo,
      'm-limit': mLimit,
      UpdateFcn,
      FormatDate,
      ConfigDetail,
      CodeTransfer
    },
    data() {
      return {
        total: null,
        listQuery: {
          limit: 10,
          page: 1,
          type: 'modbus'
        },
        list: [],
        isShowConfig: false,
        currentCode: this.$store.state.modbus.currentCode,
        reserveCode: this.$store.state.modbus.reserveCode,
        memory: this.$store.state.modbus.memory,
        isShowDetail: false,
        activeName: '1',
        configForm: {
          connection: {
            ip: '127.0.0.1',
            port: 8020
          },
          restrictions: []
        }
      }
    },
    computed: {
      totalCode() {
        return this.currentCode.concat(this.reserveCode)
      },
      fc_options() {
        return this.$store.state.modbus.currentCode
      },
      m_options() {
        return this.$store.state.modbus.memory
      }
    },
    mounted() {
      this.getAlertData()
    },
    methods: {
      showConfig() {
        this.isShowConfig = true
      },
      updateCode(data) {
        this.$store.commit('updateModbus', data)
      },
      verifyForm() {
        this.$alert('<strong>是否 <i>确定</i> 验证</strong>', 'Modbus 配置验证', {
          dangerouslyUseHTMLString: true,
          callback: action => {
            if (action === 'confirm') {
              this.$message({
                message: '验证成功!',
                type: 'success'
              })
            } else if (action === 'cancel') {
              this.$message({
                message: '验证取消!',
                type: 'info'
              })
            }
          }
        })
      },
      submitForm() {
        this.$confirm('此操作将修改Modbus的配置文件, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.$socket.emit('setting', {
            'json': JSON.stringify(this.configForm, null, 4),
            'type': 'modbus',
            'user_name': localStorage['username'],
            'user_id': localStorage['id']
          })
          let postData = `user_id=${localStorage['id']}&username=${localStorage['username']}&protocol_type=modbus&oper=${JSON.stringify(this.configForm, null)}`
          createOperate(postData).then(res => {
          this.$message({type: 'success', message: '发送成功!'})
        }).catch(err => {
          console.log('err', err)
        })
      })
      .catch(() => {
          this.$message({type: 'info', message: '已取消发送!'})
      })
      },
      getAlertData() {
        this.list = []
        fetchAlert(this.listQuery).then((res) => {
          this.total = res.data.total
          res.data.data.forEach((item, index) => {
            this.list.push({
              protocol_type: item.protocol_type,
              time: item.time,
              message: item.message
            })
          })
        })
      },
      handleSizeChange(val) {
        this.listQuery.limit = val
        this.getAlertData()
      },
      handleCurrentChange(val) {
        this.listQuery.page = val
        this.getAlertData()
      }
    },
    sockets: {
      connect() {
        this.$socket.emit('my_event', {data: 'I\'m connected!'})
      },
      alert(message) {
        if (message['type'] === 'modbus') {
          this.getAlertData()
        }
      },
      setting(message) {
        console.log('modbus', message)
      }
    }
  }
</script>

<style lang="stylus" rel="stylesheet/stylus">
  .protocol
    margin: auto 0.8rem
    .protocol-content
    .modbus-content
      margin-bottom: 20px
      border: 1px solid #333
      border-radius: 0 0 5px 5px;
    .el-transfer
      width: 1000px
      .el-transfer-panel
        width: 400px
        height: 500px
        .el-transfer-panel__body
          height: 446px
          .is-filterable
            height: 394px
    .el-form-item
      margin-bottom: 0
    .el-container
      margin: 10px 20px
      .el-aside
        background-color: #E9EEF3;
        color: #333;
        text-align: right;
        line-height: 200px;
      .el-main
        background-color: #E9EEF3;
        color: #333;
        text-align: left;
        border-radius: 5px;
    .el-header
    .el-footer
      margin: 5px 20px
      background-color: #B3C0D1;
      color: #333;
      text-align: center;
      line-height: 55px;
      border-radius: 5px;

    .title
      line-height: 4rem
      border-radius: 0.5rem 0.5rem 0 0
      padding-left: 1rem
      color: rgb(238, 238, 238)
      background: rgb(13, 1, 49)
      font-size: 2rem
      .el-icon-setting
        font-size: 2.5rem
        margin-right: 1rem
      .el-icon-arrow-up
        float: right
        margin: 1rem 2rem
        font-size: 3rem
    .command
      margin: 1rem 1.5rem 0
      border-top: 1px solid rgb(14, 32, 108);
      button
        margin: 1rem auto
        padding: 0.5rem 2rem
        font-size: 1.7rem
        border-radius: 1rem
        color: #fff
        background: rgb(9, 145, 143)
      button + button
        margin-left: 3rem

  .config
    margin: 1rem 1.5rem 0
    font-size: 2rem
    .config-titile
      line-height: 3rem
      border-radius: 0.5rem
      padding: 0 2rem
      background: rgb(145, 181, 231)
      .el-icon-arrow-up
        float: right
        margin: 1rem 1rem
    .content
      padding: 0 2rem

  .in-line
    margin: 10px auto

  .el-range-input
    width: 43% !important
</style>
