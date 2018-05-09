<template>
  <el-breadcrumb separator-class="el-icon-arrow-right">
    <el-breadcrumb-item v-for="item in levelList" :key="item.path"
                        v-if="item.name">
      <span>{{item.name}}</span>
    </el-breadcrumb-item>
  </el-breadcrumb>
</template>

<script type="text/ecmascript-6">
  export default {
    props: {},
    data() {
      return {
        levelList: null
      }
    },
    watch: {
      $route() {
        this.getBreadcrumb()
      }
    },
    methods: {
      getBreadcrumb() {
        let matched = this.$route.matched.filter(item => item.name)
        this.levelList = matched
      }
    },
    mounted() {
      this.getBreadcrumb()
    }
  }
</script>

<style lang="stylus" rel="stylesheet/stylus">

</style>
