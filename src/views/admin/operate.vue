<template>
    <div class="operate">
      <el-table :data="list" stripe border height="700">
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
      <div class="pagination-container">
        <el-pagination background @size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page.sync="listQuery.page"
                       :page-sizes="[10, 20, 30, 50]" :page-size="listQuery.limit" layout="total, sizes, prev, pager, next, jumper" :total="total">
        </el-pagination>
      </div>

      <config-detail :isShow.sync="show" :configForm="tempDetail"
                     :currentCode="totalCode" :modbusMemory="memory"></config-detail>

    </div>
</template>

<script type="text/ecmascript-6">
  import { fetchOperate } from '@/api/operate'
  import ConfigDetail from 'components/home/components/configDetail'
  export default {
    components: {
      ConfigDetail
    },
    data() {
      return {
        show: false,
        total: null,
        listQuery: {
          limit: 10,
          page: 1
        },
        list: [],
        tempDetail: {},
        totalCode: [],
        memory: this.$store.state.modbus.memory
      }
    },
    methods: {
      getData() {
        this.list = []
        fetchOperate(this.listQuery).then(res => {
          res.data.data.forEach((item, index) => {
            this.total = res.data.total
            this.list.push({
              user_id: item.user_id,
              username: item.username,
              time: item.time,
              type: item.protocol_type || '未知',
              detail: item.oper
            })
          })
        })
      },
      handleSizeChange(val) {
        this.listQuery.limit = val
        this.getData()
      },
      handleCurrentChange(val) {
        this.listQuery.page = val
        this.getData()
      },
      showDetail(row) {
        this.tempDetail = Object.assign({}, row.detail)
        if (row.type === 'iec104') {
          this.totalCode = this.$store.getters.totalIec104Code
        } else {
          this.totalCode = this.$store.getters.totalModbusCode
        }
        this.show = true
      }
    },
    mounted() {
      this.getData()
    },
    sockets: {
      alert(message) {
        this.getAlertData()
      }
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
    .pagination-container
      margin-top: 30px
</style>