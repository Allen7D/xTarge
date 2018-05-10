<template>
    <div class="oplog">
      <el-table :data="operateData" stripe border height="1200">
        <el-table-column label="操作记录列表">
          <el-table-column fixed type="index" label="序号" width="80"></el-table-column>
          <el-table-column sortable prop="time" label="时间" width="200"></el-table-column>
          <el-table-column sortable prop="username" label="操作者" width="150"></el-table-column>
          <el-table-column sortable prop="type" label="协议类型" width="150"></el-table-column>
          <el-table-column prop="detail" label="操作记录" width="">
            <template slot-scope="scope">
              <el-button type="text" @click="showDetail(scope.row)" size="small">详细显示</el-button>
            </template>
          </el-table-column>
        </el-table-column>
      </el-table>
      <operate-detail :show.sync="show" :dataForm="tempDetail"></operate-detail>
    </div>
</template>

<script>
  import { fetchOperate } from '@/api/operate'
  import OperateDetail from './components/operateDetail.vue'

  export default {
    components: {
      OperateDetail
    },
    data() {
      return {
        show: false,
        operateData: [],
        tempDetail: {},
        fc_options: [],
        m_options: []
      }
    },
    methods: {
      getOperateData() {
        fetchOperate().then(res => {
          res.data.ops.forEach((item, index) => {
            this.operateData.push({
              user_id: item.user_id,
              username: item.username,
              time: item.time,
              type: item.protocol_type || '未知',
              detail: item.op
            })
          })
        })
      },
      showDetail(row) {
        let data = JSON.parse(row.detail)
        if (typeof data === 'string') {
          data = JSON.parse(data)
        }
        this.tempDetail = Object.assign({}, row)
        this.show = true
      }
    },
    mounted() {
      this.getOperateData()
    }
  }
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