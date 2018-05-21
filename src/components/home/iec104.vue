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
        <i-limit :fc_options="fc_options" :restrictions="configForm.restrictions"
                 :connection="configForm.connection"></i-limit>
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
    <div class="iec104-content">
      <alert-info :alertData="list" protocolType="iec104"></alert-info>
      <div class="pagination-container">
        <el-pagination background @size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page.sync="listQuery.page"
                       :page-sizes="[10, 20, 30, 50]" :page-size="listQuery.limit" layout="total, sizes, prev, pager, next, jumper" :total="total">
        </el-pagination>
      </div>
    </div>

    <!--验证配置信息，开始-->
    <el-dialog title="配置显示" :visible.sync="showForm" width="60%">
      <div class="check-table">
        <div class="connection border-2px">
          <h2>报警连接</h2>
          <div style="margin-left: 30px; margin-top: 15px;">
            <el-input placeholder="请输入内容" v-model="configForm.connection.ip" disabled>
              <template slot="prepend">IP地址</template>
            </el-input>
            <el-input placeholder="请输入内容" v-model="configForm.connection.port" disabled>
              <template slot="prepend">端口号</template>
            </el-input>
          </div>
        </div>

        <div class="restrictions border-2px" v-if="configForm.restrictions">
          <h2>限制项</h2>
          <div class="restriction border-2px" v-for="(restriction, rIndex) in configForm.restrictions" :key="rIndex">
            <h3>限制项 {{rIndex + 1}}</h3>
            <div style="margin-left: 30px; margin-top: 15px;">
              <el-input placeholder="请输入内容" v-model="restriction.address.ip" disabled>
                <template slot="prepend">IP地址</template>
              </el-input>
              <el-input placeholder="请输入内容" v-model="restriction.address.mac" disabled>
                <template slot="prepend">MAC地址</template>
              </el-input>
              <el-switch
                v-model="restriction.address.default"
                active-text="开启"
                inactive-text="关闭"
                disabled>
              </el-switch>

              <div v-if="restriction.function_codes" class="border-2px" style="margin-top: 10px; padding-left: 30px">
                <el-collapse v-model="activeName" accordion>
                  <el-collapse-item name="1">
                    <template slot="title">
                      <nav class="config-titile">
                        功能码限制
                      </nav>
                    </template>
                    <el-form
                      v-for="(function_code, fcIndex) in restriction.function_codes"
                      :key="function_code.key"
                    >
                      <el-container class="function-code border-2px">
                        <el-main class="clearfix">
                          <el-form-item :inline="true">
                            功能码{{fcIndex}}：
                            <el-input placeholder="请输入内容" v-model="function_code.id" disabled>
                              <template slot="prepend">功能码</template>
                            </el-input>
                            <el-switch v-model="function_code.default" active-text="开启" inactive-text="关闭" disabled>
                            </el-switch>

                          </el-form-item>

                          <el-form-item v-if="function_code.excepts.length !== 0">
                            <el-form class="in-line"
                                     :inline="true"
                                     v-for="(except, exceptIndex) in function_code.excepts"
                                     :label="'例外 ' + exceptIndex + ' :'"
                                     :key="except.key">
                              <div class="fc-except">
                                <el-form-item>
                                  例外{{exceptIndex + 1}}:<format-date :time="except"></format-date>
                                </el-form-item>
                              </div>
                            </el-form>
                          </el-form-item>

                        </el-main>
                      </el-container>
                    </el-form>
                  </el-collapse-item>
                </el-collapse>
              </div>
            </div>
          </div>
        </div>
      </div>
    </el-dialog>
    <!--验证配置信息，结束-->

    <config-detail :isShow.sync="isShowDetail" :configForm="configForm"
                   :currentCode="currentCode"></config-detail>
    <code-transfer :isShow.sync="isShowConfig" :updateCode="updateCode"
                 :currentCode="currentCode" :reserveCode="reserveCode"
    >
    </code-transfer>
  </div>
</template>

<script type="text/ecmascript-6">
  import functionCodeLimit from 'components/limit/functionCodeLimit'
  import iec104Limit from 'components/home/iLimit'
  import connection from 'components/connection/connection'
  import AlertInfo from './components/alertInfo'
  import FormatDate from 'components/time/formatDate'
  import ConfigDetail from './components/configDetail'
  import CodeTransfer from './components/codeTransfer'
  import { fetchAlert } from '@/api/alert'
  import { createOperate } from '@/api/operate'

  export default {
    components: {
      'fc-limit': functionCodeLimit,
      'i-limit': iec104Limit,
      'v-connection': connection,
      AlertInfo,
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
          type: 'iec104'
        },
        list: [],
        isShowConfig: false,
        currentCode: this.$store.state.iec104.currentCode,
        reserveCode: this.$store.state.iec104.reserveCode,
        showForm: false,
        activeName: '1',
        isShowDetail: false,
        fcodes: [],
        iec104_default_value: '',
        fc_ad_data: [],
        transfer_value: [],
        configForm: {
          connection: {
            ip: '127.0.0.1',
            port: 8010
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
        return this.$store.state.iec104.currentCode
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
        this.$store.commit('updateIec104', data)
      },
      verifyForm() {
        this.$alert('<strong>是否 <i>确定</i> 验证</strong>', 'IEC104 配置验证', {
          dangerouslyUseHTMLString: true,
          callback: action => {
            if (action === 'confirm') {
              this.$message({message: '验证成功!', type: 'success'})
            } else if (action === 'cancel') {
              this.$message({message: '验证取消!', type: 'info'})
            }
          }
        })
      },
      submitForm() {
        this.$confirm('此操作将修改IEC104的配置文件, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.$socket.emit('setting', {
            'json': JSON.stringify(this.configForm, null, 4),
            'type': 'iec104',
            'user_name': localStorage['username'],
            'user_id': localStorage['id']
          })
          let postData = `user_id=${localStorage['id']}&username=${localStorage['username']}&protocol_type=iec104&oper=${JSON.stringify(this.configForm, null)}`
          createOperate(postData).then(res => {
            this.$message({type: 'success', message: '发送成功!'})
          }).catch(err => {
            console.error(err)
          })
        }).catch(() => {
          this.$message({type: 'info', message: '已取消发送!'})
        })
      },
      resetForm(formName) {
        this.$refs[formName].resetFields()
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
        if (message['type'] === 'iec104') {
          this.getAlertData()
        }
      },
      setting(message) {
        console.log('iec104', message)
      }
    }
  }
</script>

<style lang="stylus" rel="stylesheet/stylus">
  .protocol
    margin: auto 0.8rem
    .protocol-content
    .iec104-content
      margin-bottom: 20px
      border: 1px solid #333
      border-radius: 0 0 5px 5px
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
        background-color: #E9EEF3
        color: #333
        text-align: right
        line-height: 200px
      .el-main
        background-color: #E9EEF3
        color: #333
        text-align: left
        border-radius: 5px
    .el-header
    .el-footer
      margin: 5px 20px
      background-color: #B3C0D1
      color: #333
      text-align: center
      line-height: 55px
      border-radius: 5px

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
      border-top: 1px solid rgb(14, 32, 108)
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
