<template>
  <div>
    <el-dialog
      title="配置显示"
      :visible.sync="dialogVisible"
      width="60%"
      :before-close="handleClose">
      <div class="check-table" v-if="this.currentOp">
        <div class="check-table">
          <div class="connection border-2px">
            <h2>报警连接</h2>
            <div style="margin-left: 30px; margin-top: 15px;" v-if="this.currentOp.connection">
              <el-input placeholder="请输入内容" v-model="this.currentOp.connection.ip" disabled>
                <template slot="prepend">IP地址</template>
              </el-input>
              <el-input placeholder="请输入内容" v-model="this.currentOp.connection.port" disabled>
                <template slot="prepend">端口号</template>
              </el-input>
            </div>
          </div>

          <div class="restrictions border-2px" v-if="this.currentOp.restrictions">
            <h2>限制项</h2>
            <div class="restriction border-2px" v-for="(restriction, rIndex) in this.currentOp.restrictions">
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

                <div v-if="restriction.memories" class="memory border-2px" style="margin-top: 10px;">
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
                              <el-input v-model="m_options[memory.id].label" disabled>
                                <template slot="prepend">内存类型</template>
                              </el-input>
                              <el-input v-model="m_options[memory.id2].label" disabled>
                                <template slot="prepend">功能码类型</template>
                              </el-input>
                              <el-switch
                                v-model="memory.default"
                                active-text="开启"
                                inactive-text="关闭"
                                disabled>
                              </el-switch>
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
      </div>
      <span slot="footer" class="dialog-footer">
      </span>
    </el-dialog>

    <div class="oplog">
      <el-table
        :data="opDate"
        stripe
        border
        style="width: 1200px"
        height="1200">
        <el-table-column label="操作记录列表">
          <el-table-column
            fixed
            type="index"
            label="序号"
            width="80">
          </el-table-column>
          <el-table-column
            sortable
            prop="time"
            label="时间"
            width="200">
          </el-table-column>
          <el-table-column
            sortable
            prop="username"
            label="操作者"
            width="150">
          </el-table-column>
          <el-table-column
            sortable
            prop="protocol_type"
            label="协议类型"
            width="150">
          </el-table-column>
          <el-table-column
            prop="op"
            label="操作记录"
            width="">
            <template slot-scope="scope">
              <el-button type="text" @click="showOp(scope.$index, scope.row)" size="small">详细显示</el-button>
            </template>

          </el-table-column>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script>
  import axios from 'axios';
  export default {
    data() {
      return {
        opDate: [],
        dialogVisible: false,
        currentOp: {},
        fc_options: [],
        m_options: []
      };
    },
    created() {
      axios.get('/api/v1.0/ops')
        .then((res) => {
          res.data.ops.forEach((item, index) => {
            this.opDate.push({
              user_id: item.user_id,
              username: item.username,
              time: item.time,
              protocol_type: item.protocol_type || '未知',
              op: JSON.stringify(item.op)
            });
          });
        });
    },
    methods: {
      showOp(index, row) {
        let data = JSON.parse(row.op);
        if (typeof data === 'string') {
          data = JSON.parse(data);
        }
        console.log(data);
        this.currentOp = data;
        this.dialogVisible = true;
      }
    }
  };
</script>

<style lang="stylus" rel="stylesheet/stylus">
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