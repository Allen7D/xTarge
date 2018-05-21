<template>
  <div class="communicate">
    <el-table :data="list" stripe border height="600">
      <el-table-column label="通讯记录列表">
        <el-table-column fixed type="index" label="序号" width="80">
        </el-table-column>
        <el-table-column sortable prop="time" label="时间" width="200">
        </el-table-column>
        <el-table-column sortable prop="ip" label="类型" width="150">
        </el-table-column>
        <el-table-column prop="buffer" label="Message">
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
  import { fetchCmnt } from '@/api/cmnt'
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
      getCmntData() {
        this.list = []
        fetchCmnt(this.listQuery).then((res) => {
          this.total = res.data.total
          res.data.data.forEach((item, index) => {
            this.list.push({
              time: item.time,
              buffer: item.buffer,
              ip: item.ip
            })
          })
        })
      },
      handleSizeChange(val) {
        this.listQuery.limit = val
        this.getCmntData()
      },
      handleCurrentChange(val) {
        this.listQuery.page = val
        this.getCmntData()
      }
    },
    mounted() {
      this.getCmntData()
    }
  }
</script>

<style lang="stylus" rel="stylesheet/stylus">
  .pagination-container
    margin-top: 30px
</style>