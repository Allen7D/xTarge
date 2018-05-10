<template>
  <div class="admin">
    <x-header></x-header>
    <div class="link">
      <nav class="tab">
        <div class="tab-item" :class="{ active: isIec104 }" @click="toIec104">
          <router-link to="/iec104">IEC104</router-link>
        </div>
        <div class="tab-item" :class="{ active: isModbus }" @click="toModbus">
          <router-link to="/modbus">Modbus</router-link>
        </div>
      </nav>
      <div class="detail">{{protocol}}安全协议栈配置与监控界面</div>
    </div>
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
    data() {
      return {
        protocol: 'Modbus',
        isIec104: false,
        isModbus: true
      }
    },
    computed: {
      ...mapState(['isLogin'])
    },
    mounted () {
      if (this.$route.path === '/iec104') {
        this.isIec104 = true
        this.isModbus = false
        this.protocol = 'IEC104'
      } else if (this.$route.path === '/modbus') {
        this.isIec104 = false
        this.isModbus = true
        this.protocol = 'Modbus'
      }
    },
    created() {
      // 如果已经登陆了，则进入协议栈页面
      if (!this.isLogin) {
        this.$router.push('/login')
      }
    },
    methods: {
      toIec104() {
        this.$router.push('/iec104')
      },
      toModbus() {
        this.$router.push('/modbus')
      },
      logout() {
        localStorage['username'] = ''
        localStorage['isLogin'] = false
        localStorage['level'] = ''
        this.$router.push('/login')
      },
      modifyTitle() {
        if (this.$route.path === '/iec104') {
          this.isIec104 = true
          this.isModbus = false
          this.protocol = 'IEC104'
        } else {
          this.isIec104 = false
          this.isModbus = true
          this.protocol = 'Modbus'
        }
      }
    },
    watch: {
      '$route': 'modifyTitle'
    }
  }
</script>

<style lang="stylus" rel="stylesheet/stylus">
  .link
    .tab
      display: flex
      background: rgb(13, 1, 49)
      font-size: 1.8rem
      .tab-item
        text-align: center
        padding: 0.8rem 3rem
        a
          text-decoration: none
          color: rgb(238, 238, 238)
      .active
        background: rgb(238, 238, 238)
        a
          color: rgb(13, 1, 49)

    .detail
      line-height: 4rem
      font-size: 1.8rem
      background: rgb(238, 238, 238)
      color: rgb(14, 32, 108)
      text-indent: 45px

</style>
