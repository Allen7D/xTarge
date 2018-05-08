<template>
    <!--
        组件中value:label对应对象中的key:value
        「默认值local_value」是基于value值去对应label显示
    -->
    <el-select v-model="local_value" placeholder="请选择">
        <el-option
                v-for="item in options"
                :key="item.value"
                :value="item.value"
                :label="item.label"
                >
        </el-option>
    </el-select>
</template>

<script type="text/ecmascript-6">
    export default {
        props: {
            options: {
                type: Array
            },
            remote_value: {
                type: Number
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
