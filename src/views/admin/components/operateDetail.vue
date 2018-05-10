<template>
  <el-dialog title="配置显示" center :visible.sync="isVisible" width="60%" @close="hideDetail">
    {{dataForm}}
    <el-button type="info" @click="showDetail">Show Data</el-button>
    <div>
      <!--<div class="check-table" v-if="dataForm">-->
      <!--<div class="check-table">-->
        <!--<div class="connection border-2px">-->
          <!--<h2>报警连接</h2>-->
          <!--<div style="margin-left: 30px; margin-top: 15px;" v-if="dataForm.connection">-->
            <!--<el-input placeholder="请输入内容" v-model="dataForm.connection.ip" disabled>-->
              <!--<template slot="prepend">IP地址</template>-->
            <!--</el-input>-->
            <!--<el-input placeholder="请输入内容" v-model="dataForm.connection.port" disabled>-->
              <!--<template slot="prepend">端口号</template>-->
            <!--</el-input>-->
          <!--</div>-->
        <!--</div>-->

        <!--<div class="restrictions border-2px" v-if="dataForm.restrictions">-->
          <!--<h2>限制项</h2>-->
          <!--<div class="restriction border-2px" v-for="(restriction, rIndex) in dataForm.restrictions" :key="rIndex">-->
            <!--<h3>限制项 {{rIndex + 1}}</h3>-->
            <!--<div style="margin-left: 30px; margin-top: 15px;">-->
              <!--<el-input placeholder="请输入内容" v-model="restriction.address.ip" disabled>-->
                <!--<template slot="prepend">IP地址</template>-->
              <!--</el-input>-->
              <!--<el-input placeholder="请输入内容" v-model="restriction.address.mac" disabled>-->
                <!--<template slot="prepend">MAC地址</template>-->
              <!--</el-input>-->
              <!--<el-switch v-model="restriction.address.default" active-text="开启" inactive-text="关闭" disabled>-->
              <!--</el-switch>-->

              <!--<div v-if="restriction.function_codes" class="border-2px" style="margin-top: 10px; padding-left: 30px">-->
                <!--<el-collapse v-model="activeName" accordion>-->
                  <!--<el-collapse-item name="1">-->
                    <!--<template slot="title">-->
                      <!--<nav class="config-titile">-->
                        <!--功能码限制-->
                      <!--</nav>-->
                    <!--</template>-->
                    <!--<el-form-->
                      <!--v-for="(function_code, fcIndex) in restriction.function_codes"-->
                      <!--:key="function_code.key"-->
                    <!--&gt;-->
                      <!--<el-container class="function-code border-2px">-->
                        <!--<el-main class="clearfix">-->
                          <!--<el-form-item :inline="true">-->
                            <!--功能码{{fcIndex}}：-->
                            <!--<el-input placeholder="请输入内容" v-model="fc_options[function_code.id - 1].label" disabled>-->
                              <!--<template slot="prepend">功能码</template>-->
                            <!--</el-input>-->
                            <!--<el-switch-->
                              <!--v-model="function_code.default"-->
                              <!--active-text="开启"-->
                              <!--inactive-text="关闭"-->
                              <!--disabled>-->
                            <!--</el-switch>-->

                          <!--</el-form-item>-->

                          <!--<el-form-item v-if="function_code.excepts.length !== 0">-->
                            <!--<el-form class="in-line"-->
                                     <!--:inline="true"-->
                                     <!--v-for="(except, exceptIndex) in function_code.excepts"-->
                                     <!--:label="'例外 ' + exceptIndex + ' :'"-->
                                     <!--:key="except.key">-->
                              <!--<div class="fc-except">-->
                                <!--<el-form-item>-->
                                  <!--例外{{exceptIndex + 1}}:-->
                                  <!--<el-input placeholder="" v-if="except.start.year !== -1" v-model="except.start.year"-->
                                            <!--style="width: 100px;" disabled>-->
                                    <!--<template slot="append">年</template>-->
                                  <!--</el-input>-->

                                  <!--<el-input placeholder="" v-if="except.start.mon !== -1" v-model="except.start.mon"-->
                                            <!--disabled>-->
                                    <!--<template slot="append">月</template>-->
                                  <!--</el-input>-->

                                  <!--<el-input placeholder="" v-if="except.start.day !== -1" v-model="except.start.day"-->
                                            <!--disabled>-->
                                    <!--<template slot="append">日</template>-->
                                  <!--</el-input>-->

                                  <!--<el-input placeholder="" v-if="except.start.hour !== -1" v-model="except.start.hour"-->
                                            <!--disabled>-->
                                    <!--<template slot="append">时</template>-->
                                  <!--</el-input>-->

                                  <!--<el-input placeholder="" v-if="except.start.min !== -1" v-model="except.start.min"-->
                                            <!--disabled>-->
                                    <!--<template slot="append">分</template>-->
                                  <!--</el-input>-->

                                  <!--<el-input placeholder="" v-if="except.start.sec !== -1" v-model="except.start.sec"-->
                                            <!--disabled>-->
                                    <!--<template slot="append">秒</template>-->
                                  <!--</el-input>-->
                                <!--</el-form-item>-->
                                <!--<span style="margin-right: 5px;">~</span>-->
                                <!--<el-form-item>-->
                                  <!--<el-input placeholder="" v-if="except.end.year !== -1" v-model="except.end.year"-->
                                            <!--style="width: 100px;" disabled>-->
                                    <!--<template slot="append">年</template>-->
                                  <!--</el-input>-->

                                  <!--<el-input placeholder="" v-if="except.end.mon !== -1" v-model="except.end.mon"-->
                                            <!--disabled>-->
                                    <!--<template slot="append">月</template>-->
                                  <!--</el-input>-->

                                  <!--<el-input placeholder="" v-if="except.end.day !== -1" v-model="except.end.day"-->
                                            <!--disabled>-->
                                    <!--<template slot="append">日</template>-->
                                  <!--</el-input>-->

                                  <!--<el-input placeholder="" v-if="except.end.hour !== -1" v-model="except.end.hour"-->
                                            <!--disabled>-->
                                    <!--<template slot="append">时</template>-->
                                  <!--</el-input>-->

                                  <!--<el-input placeholder="" v-if="except.end.min !== -1" v-model="except.end.min"-->
                                            <!--disabled>-->
                                    <!--<template slot="append">分</template>-->
                                  <!--</el-input>-->

                                  <!--<el-input placeholder="" v-if="except.end.sec !== -1" v-model="except.end.sec"-->
                                            <!--disabled>-->
                                    <!--<template slot="append">秒</template>-->
                                  <!--</el-input>-->
                                <!--</el-form-item>-->
                              <!--</div>-->
                            <!--</el-form>-->
                          <!--</el-form-item>-->

                        <!--</el-main>-->
                      <!--</el-container>-->
                    <!--</el-form>-->
                  <!--</el-collapse-item>-->
                <!--</el-collapse>-->
              <!--</div>-->

              <!--<div v-if="restriction.memories" class="memory border-2px" style="margin-top: 10px;">-->
                <!--<el-collapse v-model="activeName" accordion>-->
                  <!--<el-collapse-item name="1">-->
                    <!--<template slot="title">-->
                      <!--<nav class="config-titile">-->
                        <!--内存限制-->
                      <!--</nav>-->
                    <!--</template>-->

                    <!--<el-form-->
                      <!--v-for="memory in restriction.memories"-->
                      <!--:key="memory.key"-->
                    <!--&gt;-->
                      <!--<el-container class="border-2px">-->
                        <!--<el-main>-->
                          <!--<el-form-item :inline="true">-->
                            <!--<el-input v-model="m_options[memory.id].label" disabled>-->
                              <!--<template slot="prepend">内存类型</template>-->
                            <!--</el-input>-->
                            <!--<el-input v-model="m_options[memory.id2].label" disabled>-->
                              <!--<template slot="prepend">功能码类型</template>-->
                            <!--</el-input>-->
                            <!--<el-switch-->
                              <!--v-model="memory.default"-->
                              <!--active-text="开启"-->
                              <!--inactive-text="关闭"-->
                              <!--disabled>-->
                            <!--</el-switch>-->
                          <!--</el-form-item>-->
                          <!--<el-form-item v-if="memory.excepts.length !== 0">-->
                            <!--<el-form class="in-line" :inline="true"-->
                                     <!--style="margin: 5px"-->
                                     <!--v-for="(except, index) in memory.excepts"-->
                                     <!--:label="'例外 ' + index + ' :'"-->
                                     <!--:key="except.key">-->
                              <!--例外{{index + 1}} :-->
                              <!--<el-input v-model="except.start" disabled>-->
                                <!--<template slot="prepend">开始地址</template>-->
                              <!--</el-input>-->

                              <!--<el-input v-model="except.end" disabled>-->
                                <!--<template slot="prepend">结束地址</template>-->
                              <!--</el-input>-->
                            <!--</el-form>-->

                          <!--</el-form-item>-->
                        <!--</el-main>-->
                      <!--</el-container>-->
                    <!--</el-form>-->
                  <!--</el-collapse-item>-->
                <!--</el-collapse>-->
              <!--</div>-->
            <!--</div>-->
          <!--</div>-->
        <!--</div>-->
      <!--</div>-->
    <!--</div>-->
    </div>
  </el-dialog>
</template>

<script type="text/ecmascript-6">
  export default {
    props: {
      dataForm: {
        type: Object
      },
      show: {
        type: Boolean,
        default: false
      }
    },
    data() {
      return {
        isVisible: this.show
      }
    },
    watch: {
      show() {
        this.isVisible = this.show
      }
    },
    methods: {
      showDetail() {
        console.log(this.dataForm)
      },
      hideDetail() {
        this.$emit('update:show', false)
      }
    }
  }
</script>

<style scoped lang="stylus" rel="stylesheet/stylus">

</style>