<template>
  <div class="oplog">
    <el-table
      :data="alertData"
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
          prop="op"
          label="操作记录"
          width="">
        </el-table-column>
      </el-table-column>
    </el-table>
  </div>
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
      axios.get('/api/v1.0/ops')
        .then((res) => {
          res.data.ops.forEach((item, index) => {
            this.alertData.push({
              user_id: item.user_id,
              username: item.username,
              time: item.time,
              op: JSON.stringify(item.op)
            });
          });
        });
    }
  };
</script>

<style lang="stylus" rel="stylesheet/stylus">

</style>