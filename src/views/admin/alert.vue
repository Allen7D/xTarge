<template>
  <div class="alert">
    <el-table :data="list" stripe border height="600">
      <el-table-column label="报警记录列表">
        <el-table-column fixed type="index" label="序号" width="80">
        </el-table-column>
        <el-table-column sortable prop="time" label="时间" width="200">
        </el-table-column>
        <el-table-column sortable prop="type" label="类型" width="100">
        </el-table-column>
        <el-table-column prop="message" label="Message">
        </el-table-column>
      </el-table-column>
    </el-table>
    <div class="pagination-container">
      <el-pagination background @size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page.sync="listQuery.page"
                     :page-sizes="[10, 20, 30, 50]" :page-size="listQuery.limit" layout="total, sizes, prev, pager, next, jumper" :total="total">
      </el-pagination>
    </div>
  </div>
</template>

<script type="text/ecmascript-6">
  import { fetchAlert } from '@/api/alert'
  export default {
    data() {
      return {
        total: null,
        listQuery: {
          limit: 10,
          page: 1
        },
        list: []
      }
    },
    methods: {
      getAlertData() {
        this.list = []
        fetchAlert(this.listQuery).then((res) => {
          this.total = res.data.total
          res.data.data.forEach((item, index) => {
            this.list.push({
              time: item.time,
              type: item.protocol_type,
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
    mounted() {
      this.getAlertData()
    }
  }
</script>

<style lang="stylus" rel="stylesheet/stylus">
  .pagination-container
    margin-top: 30px
</style>