<template>
    <el-switch
            style="display: block"
            v-model="value"
            active-color="#13ce66"
            inactive-color="#13ce66"
            active-text="按日期添加"
            inactive-text="按星期添加">
    </el-switch>
</template>

<script type="text/ecmascript-6">
    export default {
        data() {
            return {
                value: true
            };
        }
    };
</script>

<style lang="stylus" rel="stylesheet/stylus">

</style>