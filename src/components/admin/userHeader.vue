<template>
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item v-for="(item,index) in levelList" :key="item.path"
                          v-if="item.name">
        <span v-if="index===levelList.length-1">{{item.name}}</span>
        <span v-else :to="item.path">{{item.name}}</span>
      </el-breadcrumb-item>
    </el-breadcrumb>
</template>

<script type="text/ecmascript-6">
    export default {
        props: {
        },
      data() {
          return {
            levelList: null
          };
      },
      created() {
          this.getBreadcrumb();
      },
      watch: {
          $route() {
            this.getBreadcrumb();
        }
      },
      methods: {
          getBreadcrumb() {
            let matched = this.$route.matched.filter(item => item.name);
            this.levelList = matched;
          }
      }
    };
</script>

<style lang="stylus" rel="stylesheet/stylus">

</style>
