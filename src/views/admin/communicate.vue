<template>
  <el-table :data="cnmtData" stripe border height="1200">
    <el-table-column label="通讯记录列表">
      <el-table-column fixed type="index" label="序号" width="80">
      </el-table-column>
      <el-table-column sortable prop="time" label="时间" width="200">
      </el-table-column>
      <el-table-column sortable prop="ip" label="IP地址" width="200">
      </el-table-column>
      <el-table-column prop="buffer" label="Buffer">
      </el-table-column>
    </el-table-column>
  </el-table>
</template>

<script>
  import {fetchAlert} from '@/api/alert'
  export default {
    data() {
      return {
        cmntData: []
      }
    },
    methods: {
      getAlertData() {
        fetchAlert().then((res) => {
          res.data.cmnts.forEach((item, index) => {
            this.cmntData.push({
              time: item.time,
              buffer: item.buffer,
              ip: item.ip
            })
          })
        })
      }
    },
    mounted() {
      this.getCmntData()
    }
  }
</script>

<style lang="stylus" rel="stylesheet/stylus">

</style>