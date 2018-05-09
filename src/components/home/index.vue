<template>
  <div>
    <x-header></x-header>
    <keep-alive>
      <router-view></router-view>
    </keep-alive>
  </div>
</template>

<script type="text/ecmascript-6">
  import XHeader from 'components/header/header.vue'
  import Iec104 from './iec104.vue'
  import Modbus from './modbus.vue'

  import {mapState} from 'vuex'

  export default {
    components: {
      XHeader,
      Iec104,
      Modbus
    },
    computed: {
      ...mapState(['isLogin'])
    },
    created() {
      // 如果已经登陆了，则进入协议栈页面
      if (!this.isLogin) {
        this.$router.push('/login')
      }
    }
  }
</script>

<style lang="stylus" rel="stylesheet/stylus">

</style>
