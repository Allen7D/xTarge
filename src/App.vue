<template>
  <keep-alive>
    <router-view></router-view>
  </keep-alive>
</template>

<script type="text/ecmascript-6">
  export default {
    data() {
      return {
        iec104: {
          currentCode: [],
          reserveCode: []
        },
        modbus: {
          currentCode: [],
          reserveCode: [],
          memory: []
        }
      }
    },
    methods: {
      initIec104() {
        this.$http.get('/api/iec104').then((res) => {
          const data = res.body.data
          let {appended: current, appendable: reserve} = data.function_code
          for (let val in current) {
            this.iec104.currentCode.push({
              id: parseInt(val.split(' ')[0]),
              value: val,
              note: current[val]
            })
          }
          for (let val in reserve) {
            this.iec104.reserveCode.push({
              id: parseInt(val.split(' ')[0]),
              value: val,
              note: reserve[val]
            })
          }
        })
      },
      initModbus() {
        this.$http.get('/api/modbus').then((res) => {
          const data = res.body.data
          let {appended: current, appendable: reserve} = data.function_code
          let memory = data.memory
          for (let val in current) {
            this.modbus.currentCode.push({
              id: parseInt(val.split(' ')[0]),
              value: val,
              note: current[val]
            })
          }
          for (let val in reserve) {
            this.modbus.reserveCode.push({
              id: parseInt(val.split(' ')[0]),
              value: val,
              note: reserve[val]
            })
          }
          for (let val in memory) {
            this.modbus.memory.push({
              id: memory[val],
              value: val
            })
          }
        })
      }
    },
    created() {
      this.initModbus()
      this.$store.commit('fetchModbus', this.modbus)
      this.initIec104()
      this.$store.commit('fetchIec104', this.iec104)
    }
  }
</script>

<style lang="stylus" rel="stylesheet/stylus">
</style>
