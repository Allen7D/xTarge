<template>
  <el-table
    :data="alertData"
    stripe
    border
    style="width: 1200px"
    height="1200">
    <el-table-column label="报警记录列表">
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
        prop="protocol_type"
        label="类型"
        width="100">
      </el-table-column>
      <el-table-column
        prop="message"
        label="Message"
        width="">
      </el-table-column>
    </el-table-column>
  </el-table>
</template>

<script>
  import axios from 'axios';
  export default {
    data() {
      return {
        alertData: []
      };
    },
    created() {
      axios.get('/api/v1.0/alerts')
        .then((res) => {
          res.data.alerts.forEach((item, index) => {
            this.alertData.push({
              protocol_type: item.protocol_type,
              time: item.time,
              message: JSON.stringify(item.message)
            });
          });
        });
    }
  };
</script>

<style lang="stylus" rel="stylesheet/stylus">

</style>