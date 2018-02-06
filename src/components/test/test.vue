<template>
    <div>
        <el-radio v-model="radio" label="1">备选项</el-radio>
        <el-radio v-model="radio" label="2">备选项</el-radio>
        <el-radio v-model="radio" label="3">备选项</el-radio>
    </div>
</template>

<script type="text/ecmascript-6">
    export default {
        data () {
            return {
                radio: '2',
                address: {
                    ip: '192.168.3.84',
                    mac: '08:d4:0c:a9:44:85',
                    default: true
                }
            };
        },
        watch: {
            raido: function(val, oldVal) {
                console.log('hehe');
            }
        }
    };
</script>

<style lang="stylus" rel="stylesheet/stylus">

</style>
