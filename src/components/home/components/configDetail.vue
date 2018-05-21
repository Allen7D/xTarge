<template>
  <el-dialog title="配置显示" :visible.sync="isVisible" width="60%" @close="handleHide">
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
            <el-switch v-model="restriction.address.default" active-text="开启" inactive-text="关闭" disabled>
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
                    :key="function_code.id"
                  >
                    <el-container class="function-code border-2px">
                      <el-main class="clearfix">
                        <el-form-item :inline="true">
                          功能码{{fcIndex + 1}}：
                          {{matchCodeID(function_code.id)}}
                          <el-switch v-model="function_code.default" active-text="开启" inactive-text="关闭" disabled>
                          </el-switch>

                        </el-form-item>

                        <el-form-item v-if="function_code.excepts.length">
                          <el-form class="in-line"
                                   :inline="true"
                                   v-for="(except, exceptIndex) in function_code.excepts"
                                   :label="'例外 ' + exceptIndex + ' :'"
                                   :key="except.key">
                            <div class="except">
                              例外{{exceptIndex + 1}}:<format-date :time="except"></format-date>
                            </div>
                          </el-form>
                        </el-form-item>
                      </el-main>
                    </el-container>
                  </el-form>
                </el-collapse-item>
              </el-collapse>
            </div>

            <div v-if="restriction.memories" class="memory border-2px" style="margin-top: 10px;">
              <el-collapse v-model="activeName" accordion>
                <el-collapse-item name="1">
                  <template slot="title">
                    <nav class="config-titile">
                      内存限制
                    </nav>
                  </template>

                  <el-form v-for="memory in restriction.memories" :key="memory.key">
                    <el-container class="border-2px">
                      <el-main>
                        <el-form-item :inline="true">
                          内存类型: {{matchMemoryID(memory.id)}} | 功能码类型: {{matchCodeID(memory.id2)}}
                          <el-switch v-model="memory.default" active-text="开启" inactive-text="关闭" disabled></el-switch>
                        </el-form-item>
                        <el-form-item v-if="memory.excepts.length !== 0">
                          <el-form class="in-line" :inline="true"
                                   style="margin: 5px"
                                   v-for="(except, index) in memory.excepts"
                                   :label="'例外 ' + index + ' :'"
                                   :key="except.key">
                            例外{{index + 1}} :
                            <el-input v-model="except.start" disabled>
                              <template slot="prepend">开始地址</template>
                            </el-input>

                            <el-input v-model="except.end" disabled>
                              <template slot="prepend">结束地址</template>
                            </el-input>
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
</template>

<script type="text/ecmascript-6">
  import FormatDate from 'components/time/formatDate'

  export default {
    components: {
      FormatDate
    },
    props: {
      isShow: {
        type: Boolean,
        default: false
      },
      configForm: {
        type: Object
      },
      currentCode: {
        type: Array
      },
      modbusMemory: {
        type: Array
      }
    },
    data() {
      return {
        isVisible: this.isShow
      }
    },
    watch: {
      isShow() {
        this.isVisible = this.isShow
      }
    },
    methods: {
      handleHide() {
        this.$emit('update:isShow', false)
      },
      matchCodeID(id) {
        let len = this.currentCode.length
        for (let i = 0; i < len; i++) {
          if (this.currentCode[i].id === id) {
            return this.currentCode[i].value
          }
        }
      },
      matchMemoryID(id) {
        let len = this.modbusMemory.length
        for (let i = 0; i < len; i++) {
          if (this.modbusMemory[i].id === id) {
            return this.modbusMemory[i].value
          }
        }
      }
    }
  }
</script>

<style scoped lang="stylus" rel="stylesheet/stylus">
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
        .memory
          margin: 10px 0
          padding-left: 30px
    .el-input
      width: 300px
</style>