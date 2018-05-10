<template>
  <div class="update">
    <el-collapse accordion>
      <el-collapse-item>
        <template slot="title">
          <nav class="config-titile">
            添加/移除 功能码
          </nav>
        </template>
        <el-container>
          <el-main>
            <el-transfer :titles="['功能码(可添加)', '功能码(可移除)']" filter-placeholder="请输入功能码"
                         :button-texts="['功能码栏 添加', '功能码栏 移除']" filterable :filter-method="filterMethod"
                         @change="handleChange" v-model="transfer_value" :data="fc_ad_data">
            </el-transfer>
          </el-main>
        </el-container>
      </el-collapse-item>
    </el-collapse>
  </div>
</template>

<script type="text/ecmascript-6">
  export default {

  }
</script>

<style scoped lang="stylus" rel="stylesheet/stylus">
  .update
    margin: 1rem 1.5rem 0
    font-size: 2rem
    .config-titile
      line-height: 3rem
      border-radius: 0.5rem
      padding: 0 2rem
      background: rgb(145, 181, 231)
      .el-icon-arrow-up
        float: right
        margin: 1rem 1rem
    .content
      padding: 0 2rem

</style>