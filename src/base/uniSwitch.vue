<template>
    <el-switch
            v-model="local_value"
            active-text="默认打开"
            inactive-text="关闭">
    </el-switch>
</template>

<script type="text/ecmascript-6">
    export default {
        props: {
            remote_value: {
                type: Boolean
            }
        },
        data() {
            return {
                local_value: this.remote_value
            }
        },
        watch: {
            local_value(val) {
                console.log(this.local_value, this.remote_value)
                this.$emit('update:remote_value', val)
            }
        }
    }
</script>

<style lang="stylus" rel="stylesheet/stylus">

</style>