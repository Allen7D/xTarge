<template>

  <div class="check-table">

    <div class="connection border-2px">
      <h2>报警连接</h2>
      <div style="margin-left: 30px; margin-top: 15px;">
        <el-input placeholder="请输入内容" v-model="this.config.connection.ip" disabled>
          <template slot="prepend">IP地址</template>
        </el-input>
        <el-input placeholder="请输入内容" v-model="this.config.connection.port" disabled>
          <template slot="prepend">端口号</template>
        </el-input>
      </div>
    </div>

    <div class="restrictions border-2px" v-if="this.config.restrictions">
      <h2>限制项</h2>
      <div class="restriction border-2px" v-for="(restriction, rIndex) in this.config.restrictions">
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
          <div class="border-2px" style="margin-top: 10px; padding-left: 30px">
            功能码限制
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
                          <el-input placeholder="" v-if="except.start.year !== -1" v-model="except.start.year" style="width: 100px;" disabled>
                            <template slot="append">年</template>
                          </el-input>

                          <el-input placeholder="" v-if="except.start.mon !== -1"  v-model="except.start.mon" disabled>
                            <template slot="append">月</template>
                          </el-input>

                          <el-input placeholder="" v-if="except.start.day !== -1"  v-model="except.start.day" disabled>
                            <template slot="append">日</template>
                          </el-input>

                          <el-input placeholder="" v-if="except.start.hour !== -1"  v-model="except.start.hour" disabled>
                            <template slot="append">时</template>
                          </el-input>

                          <el-input placeholder="" v-if="except.start.min !== -1"  v-model="except.start.min" disabled>
                            <template slot="append">分</template>
                          </el-input>

                          <el-input placeholder="" v-if="except.start.sec !== -1"  v-model="except.start.sec" disabled>
                            <template slot="append">秒</template>
                          </el-input>
                        </el-form-item>
                        <span style="margin-right: 5px;">~</span>
                        <el-form-item>
                          <el-input placeholder="" v-if="except.end.year !== -1" v-model="except.end.year" style="width: 100px;" disabled>
                            <template slot="append">年</template>
                          </el-input>

                          <el-input placeholder="" v-if="except.end.mon !== -1" v-model="except.end.mon" disabled>
                            <template slot="append">月</template>
                          </el-input>

                          <el-input placeholder="" v-if="except.end.day !== -1" v-model="except.end.day" disabled>
                            <template slot="append">日</template>
                          </el-input>

                          <el-input placeholder="" v-if="except.end.hour !== -1" v-model="except.end.hour" disabled>
                            <template slot="append">时</template>
                          </el-input>

                          <el-input placeholder="" v-if="except.end.min !== -1" v-model="except.end.min" disabled>
                            <template slot="append">分</template>
                          </el-input>

                          <el-input placeholder="" v-if="except.end.sec !== -1" v-model="except.end.sec" disabled>
                            <template slot="append">秒</template>
                          </el-input>
                        </el-form-item>
                      </div>
                    </el-form>
                  </el-form-item>

                </el-main>
              </el-container>
            </el-form>
          </div>

          <div v-if="restriction.memories" class="memory border-2px" style="margin-top: 10px">
            <el-collapse v-model="activeName" accordion>
              <el-collapse-item name="1">
                <template slot="title">
                  <nav class="config-titile">
                    内存限制
                  </nav>
                </template>

                <el-form
                  v-for="(memory, index) in restriction.memories"
                  :key="memory.key"
                >
                  <el-container class="border-2px">
                    <el-main>
                      <el-form-item :inline="true">
                        <el-input v-model="memory.id" disabled>
                          <template slot="prepend">内存类型</template>
                        </el-input>
                        <el-input v-model="memory.id2" disabled>
                          <template slot="prepend">功能码类型</template>
                        </el-input>
                        <el-switch
                          v-model="memory.default"
                          active-text="开启"
                          inactive-text="关闭"
                          disabled>
                        </el-switch>
                      </el-form-item>
                      <el-form-item>
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
</template>

<script type="text/ecmascript-6">
  export default {
    data() {
      return {
        activeName: '1',
        config: {
          'connection': {
            'ip': '127.0.0.1',
            'port': 8000
          },
          'restrictions': [
            {
              'address': {
                'ip': '192.168.0.1',
                'mac': 'aa:cc:dd:ee:ff',
                'default': true
              },
              'function_codes': [
                {
                  'id': 1,
                  'default': true,
                  'excepts': [
                    {
                      'start': {
                        'year': -1,
                        'mon': 11,
                        'day': -1,
                        'hour': -1,
                        'min': -1,
                        'sec': -1,
                        'wday': -1
                      },
                      'end': {
                        'year': -1,
                        'mon': 12,
                        'day': -1,
                        'hour': -1,
                        'min': -1,
                        'sec': -1,
                        'wday': -1
                      }
                    },
                    {
                      'start': {
                        'year': 2018,
                        'mon': 11,
                        'day': 1,
                        'hour': 2,
                        'min': 4,
                        'sec': 5,
                        'wday': -1
                      },
                      'end': {
                        'year': 2019,
                        'mon': 12,
                        'day': 1,
                        'hour': 21,
                        'min': 33,
                        'sec': 11,
                        'wday': -1
                      }
                    }
                  ]
                },
                {
                  'id': 1,
                  'default': true,
                  'excepts': []
                }
              ],
              'memories': [
                {
                  'id': 1,
                  'id2': 1,
                  'default': false,
                  'excepts': [
                    {
                      'start': '11111',
                      'end': '123123'
                    },
                    {
                      'start': '11111',
                      'end': '123123'
                    },
                    {
                      'start': '11111',
                      'end': '123123'
                    }
                  ]
                }
              ]
            },
            {
              'address': {
                'ip': '192.168.0.1',
                'mac': 'aa:cc:dd:ee:ff',
                'default': true
              },
              'function_codes': [
                {
                  'id': 1,
                  'default': false,
                  'excepts': [
                    {
                      'start': {
                        'year': -1,
                        'mon': -1,
                        'day': -1,
                        'hour': -1,
                        'min': -1,
                        'sec': -1,
                        'wday': -1
                      },
                      'end': {
                        'year': -1,
                        'mon': -1,
                        'day': -1,
                        'hour': -1,
                        'min': -1,
                        'sec': -1,
                        'wday': -1
                      }
                    }
                  ]
                },
                {
                  'id': 1,
                  'default': true,
                  'excepts': []
                }
              ],
              'memories': [
                {
                  'id': 1,
                  'id2': 1,
                  'default': false,
                  'excepts': [
                    {
                      'start': '1231',
                      'end': '1231231'
                    }
                  ]
                }
              ]
            }
          ]
        }
      };
    }
  }
</script>

<style lang="stylus" rel="stylesheet/stylus">
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
          margin: 10px 0
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
