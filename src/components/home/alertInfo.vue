<template>
    <el-table
            :data="alertData"
            stripe
            border
            style="width: 100%"
            height="300">
        <el-table-column
                fixed
                prop="index"
                label="序号"
                width="80">
        </el-table-column>
        <el-table-column
                prop="date"
                label="时间"
                width="200">
        </el-table-column>
        <el-table-column
                prop="message"
                label="Message"
                width="">
        </el-table-column>
        <el-table-column
                prop="code"
                label="Code"
                width="">
        </el-table-column>
    </el-table>
</template>

<script>
    export default {
        data() {
            return {
                alertData: [{
                    index: '0001',
                    date: '2016-05-03',
                    message: 'error',
                    code: '0x15 Measured value, normalized value without quality descriptor'
                }, {
                    index: '0002',
                    date: '2016-05-02',
                    message: 'error',
                    code: '0x15 Measured value, normalized value without quality descriptor'
                }, {
                    index: '0003',
                    date: '2016-05-04',
                    message: 'error',
                    code: '0x15 Measured value, normalized value without quality descriptor'
                }, {
                    index: '0004',
                    date: '2016-05-01',
                    message: 'error',
                    code: '0x15 Measured value, normalized value without quality descriptor'
                }, {
                    index: '0005',
                    date: '2016-05-08',
                    message: 'error',
                    code: '0x15 Measured value, normalized value without quality descriptor'
                }, {
                    index: '0006',
                    date: '2016-05-06',
                    message: 'error',
                    code: '0x15 Measured value, normalized value without quality descriptor'
                }, {
                    index: '0007',
                    date: '2016-05-07',
                    message: 'error',
                    code: '0x15 Measured value, normalized value without quality descriptor'
                }]
            };
        }
    };
</script>

<style lang="stylus" rel="stylesheet/stylus">

</style>