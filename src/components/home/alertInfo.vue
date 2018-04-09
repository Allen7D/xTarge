<template>
  <el-table
    :data="alertData"
    stripe
    border
    style="width: 100%"
    height="300">
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
  export default {
    props: {
      alertData: {
        type: Array
      },
      protocolType: {
        type: String
      }
    },
    data() {
      return {};
    },
    sockets: {
      alert(message) {
        if (message['type'] === this.protocolType) {
          console.log(message);
        }
      }
    }
  };
</script>

<style lang="stylus" rel="stylesheet/stylus">

</style>