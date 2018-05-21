<template>
  <div>
    <el-date-picker v-model="formatDate" type="datetimerange" range-separator="-" start-placeholder="开始日期" end-placeholder="结束日期" readonly></el-date-picker>
  </div>
</template>

<script type="text/ecmascript-6">
  export default {
    props: {
      time: {
        type: Object
      }
    },
    computed: {
      formatDate() {
        let {start, end} = this.time
        return [new Date(start.year, (start.mon - 1), start.day, start.hour, start.min, start.sec), new Date(end.year, end.mon, end.day, end.hour, end.min, end.sec)]
      }
    }
  }
</script>

<style scoped lang="stylus" rel="stylesheet/stylus">

</style>