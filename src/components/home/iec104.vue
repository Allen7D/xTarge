<template>
  <div class="protocol iec104">
    <nav class="title">
      <i class="el-icon-setting"></i>
      配置 <span>(配置方式：选择限制的功能，完成后选择发送)</span>
    </nav>
    <div class="protocol-content">
      <el-form :model="configForm" ref="configForm" label-width="10px" class="demo-dynamic">
        <!--报警连接 开始-->
        <v-connection :connection="configForm.connection"></v-connection>
        <!--报警连接 结束-->

        <!--功能码限制 开始-->
        <i-limit :fc_options="fc_options" :restrictions="configForm.restrictions"
                 :connection="configForm.connection"></i-limit>
        <!--功能码限制 结束-->

        <!-- 总提交按钮 -->
      </el-form>
      <div class="command">
        <el-button type="text" @click="showForm = true">显示</el-button>
        <el-button type="text" @click="verifyForm">验证</el-button>
        <el-button type="text" @click="submitForm">发送</el-button>
      </div>
      <br>
    </div>

    <nav class="title">
      <i class="el-icon-setting"></i>
      监控 <span>(监控界面：每当设备收到不符合配置的数据包，信息将显示)</span>
    </nav>
    <div class="iec104-content">
      <alert-info :alert-data="alertData" :protocol-type="iec104"></alert-info>
      <br>
    </div>

    <!--验证配置信息，开始-->
    <el-dialog
      title="配置显示"
      :visible.sync="showForm"
      width="60%"
      :before-close="handleClose">

      <div class="check-table">
        <div class="connection border-2px">
          <h2>报警连接</h2>
          <div style="margin-left: 30px; margin-top: 15px;">
            <el-input placeholder="请输入内容" v-model="this.configForm.connection.ip" disabled>
              <template slot="prepend">IP地址</template>
            </el-input>
            <el-input placeholder="请输入内容" v-model="this.configForm.connection.port" disabled>
              <template slot="prepend">端口号</template>
            </el-input>
          </div>
        </div>

        <div class="restrictions border-2px" v-if="this.configForm.restrictions">
          <h2>限制项</h2>
          <div class="restriction border-2px" v-for="(restriction, rIndex) in this.configForm.restrictions" :key="rIndex">
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

                            <el-input placeholder="请输入内容" v-model="fc_options[function_code.id - 1].label" disabled>
                              <template slot="prepend">功能码</template>
                            </el-input>
                            <el-switch
                              v-model="function_code.default"
                              active-text="开启"
                              inactive-text="关闭"
                              disabled>
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
                                  例外{{exceptIndex + 1}}:
                                  <el-input placeholder="" v-if="except.start.year !== -1" v-model="except.start.year"
                                            style="width: 100px;" disabled>
                                    <template slot="append">年</template>
                                  </el-input>

                                  <el-input placeholder="" v-if="except.start.mon !== -1" v-model="except.start.mon"
                                            disabled>
                                    <template slot="append">月</template>
                                  </el-input>

                                  <el-input placeholder="" v-if="except.start.day !== -1" v-model="except.start.day"
                                            disabled>
                                    <template slot="append">日</template>
                                  </el-input>

                                  <el-input placeholder="" v-if="except.start.hour !== -1" v-model="except.start.hour"
                                            disabled>
                                    <template slot="append">时</template>
                                  </el-input>

                                  <el-input placeholder="" v-if="except.start.min !== -1" v-model="except.start.min"
                                            disabled>
                                    <template slot="append">分</template>
                                  </el-input>

                                  <el-input placeholder="" v-if="except.start.sec !== -1" v-model="except.start.sec"
                                            disabled>
                                    <template slot="append">秒</template>
                                  </el-input>
                                </el-form-item>
                                <span style="margin-right: 5px;">~</span>
                                <el-form-item>
                                  <el-input placeholder="" v-if="except.end.year !== -1" v-model="except.end.year"
                                            style="width: 100px;" disabled>
                                    <template slot="append">年</template>
                                  </el-input>

                                  <el-input placeholder="" v-if="except.end.mon !== -1" v-model="except.end.mon"
                                            disabled>
                                    <template slot="append">月</template>
                                  </el-input>

                                  <el-input placeholder="" v-if="except.end.day !== -1" v-model="except.end.day"
                                            disabled>
                                    <template slot="append">日</template>
                                  </el-input>

                                  <el-input placeholder="" v-if="except.end.hour !== -1" v-model="except.end.hour"
                                            disabled>
                                    <template slot="append">时</template>
                                  </el-input>

                                  <el-input placeholder="" v-if="except.end.min !== -1" v-model="except.end.min"
                                            disabled>
                                    <template slot="append">分</template>
                                  </el-input>

                                  <el-input placeholder="" v-if="except.end.sec !== -1" v-model="except.end.sec"
                                            disabled>
                                    <template slot="append">秒</template>
                                  </el-input>
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

      <span slot="footer" class="dialog-footer">
        <el-button @click="showForm = false">隐藏</el-button>
      </span>
    </el-dialog>
    <!--验证配置信息，结束-->

  </div>
</template>

<script>
  import functionCodeLimit from 'components/limit/functionCodeLimit'
  import iec104Limit from 'components/home/iLimit'
  import connection from 'components/connection/connection'
  import alertInfo from './alertInfo'
  import {sortByLabel, removeByValue} from 'common/js/util'
  import axios from 'axios'

  export default {
    components: {
      'fc-limit': functionCodeLimit,
      'i-limit': iec104Limit,
      'v-connection': connection,
      'alert-info': alertInfo
    },
    data() {
      return {
        alertData: [],
        showForm: false,
        activeName: '1',
        fcodes: [],
        fc_options: [],
        iec104_default_value: '',
        fc_ad_data: [],
        transfer_value: [],
        configForm: {
          connection: {
            ip: '127.0.0.1',
            port: 8010
          },
          restrictions: []
        },
        filterMethod(query, item) {
          return item.seq.indexOf(query) > -1
        }
      }
    },
    created() {
      this.$http.get('/api/iec104').then((response) => {
        this.iec104_data = response.body.data
        this.iec104 = this.iec104_data['function_code']

        for (let i in this.iec104) {
          this.fc_options.push({'value': parseInt(i.split(' ')[0]), 'label': i})
        }
        this.fcodes.forEach((fcode, index) => {
          this.fc_ad_data.push({
            label: fcode,
            key: index,
            seq: this.fcodes[index].split(' ')[0]
          })
        })
      })
      this.getAlertData()
    },
    methods: {
      handleClose(done) {
        this.$confirm('确认关闭？')
          .then(_ => {
            done()
          })
          .catch(_ => {
          })
      },
      verifyForm() {
        this.$alert('<strong>是否 <i>确定</i> 验证</strong>', 'IEC104 配置验证', {
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
          let postData = `user_id=${localStorage['id']}&username=${localStorage['username']}&protocol_type=iec104&op=${JSON.stringify(this.configForm, null)}`
          axios.post('/api/v1.0/ops', postData, {
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded'
            }
          }).then(res => {
            console.log(res)
            this.$message({
              type: 'success',
              message: '发送成功!'
            })
          }).catch(err => {
            console.error(err)
          })
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消发送!'
          })
        })
      },
      resetForm(formName) {
        this.$refs[formName].resetFields()
      },
      handleChange(value, direction, movedKeys) {
        if (direction === 'right') {
          for (let i in movedKeys) {
            this.fc_options.push(
              {
                'value': parseInt(this.fc_ad_data[movedKeys[i]]['label'].split(' ')[0]),
                'label': this.fc_ad_data[movedKeys[i]]['label']
              }
            )
          }
          this.$notify({
            title: '添加',
            message: '提示消息：添加成功',
            type: 'success'
          })
        } else {
          for (let i in movedKeys) {
            removeByValue(this.fc_options, this.fc_ad_data[movedKeys[i]]['label'].split(' ')[0])
          }
          this.$notify({
            title: '删除',
            message: '提示消息：删除成功',
            type: 'success'
          })
        }
        this.fc_options.sort(sortByLabel)
      },
      getAlertData() {
//        this.alertData = []
        axios.get('/api/v1.0/alerts/iec104')
          .then((res) => {
            res.data.alerts.forEach((item, index) => {
              this.alertData.push({
                protocol_type: item.protocol_type,
                time: item.time,
                message: item.message
              })
            })
          })
      }
    },
    sockets: {
      connect() {
        this.$socket.emit('my_event', {data: 'I\'m connected!'})
      },
      alert(message) {
        if (message['type'] === 'iec104') {
          console.log(message)
          this.alertData.push({
            protocol_type: message['type'],
            time: message['time'],
            message: message['message']
          })
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

  /*表单检查*/
  .check-table
    .border-2px
      border: solid 2px #409dff
      border-radius: 5px
    .connection
      padding: 10px
    .restrictions
      margin-top: 10px
      padding: 10px
      .restriction
        margin: 10px
        padding: 10px
        .function-code
          .fc-except
            margin: 5px
            .el-input
              width: 75px
              .el-input-group__append
                padding: 0 5px
    .el-input
      width: 300px

</style>
