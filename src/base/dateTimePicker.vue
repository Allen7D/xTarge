<template>
    <div class="block">
        <span class="demonstration">例外</span>
        <el-date-picker
                v-model="dateValue"
                type="datetimerange"
                :picker-options="pickerOptions"
                range-separator="至"
                start-placeholder="开始日期"
                end-placeholder="结束日期"
                align="right">
        </el-date-picker>
    </div>
</template>

<script type="text/ecmascript-6">
    export default {
        props: {
            startDate: {
                type: Object
            },
            endDate: {
                type: Object
            }
        },
        data() {
            return {
                pickerOptions: {
                    shortcuts: [{
                        text: '最近一天',
                        onClick(picker) {
                            const end = new Date()
                            const start = new Date()
                            end.setTime(start.getTime() + 3600 * 1000 * 24)
                            picker.$emit('pick', [start, end])
                        }
                    }, {
                        text: '最近一周',
                        onClick(picker) {
                            const end = new Date()
                            const start = new Date()
                            end.setTime(start.getTime() + 3600 * 1000 * 24 * 7)
                            picker.$emit('pick', [start, end])
                        }
                    }, {
                        text: '最近一个月',
                        onClick(picker) {
                            const end = new Date()
                            const start = new Date()
                            end.setTime(start.getTime() + 3600 * 1000 * 24 * 30)
                            picker.$emit('pick', [start, end])
                        }
                    }, {
                        text: '最近三个月',
                        onClick(picker) {
                            const end = new Date()
                            const start = new Date()
                            end.setTime(start.getTime() + 3600 * 1000 * 24 * 90)
                            picker.$emit('pick', [start, end])
                        }
                    }]
                },
                dateValue: [
                    new Date(this.startDate.year, this.startDate.mon, this.startDate.day, this.startDate.hour, this.startDate.min, this.startDate.sec),
                    new Date(this.endDate.year, this.endDate.mon, this.endDate.day, this.endDate.hour, this.endDate.min, this.endDate.sec)
                ]
            }
        },
        watch: {
            dateValue: function (val, oldVal) {
                this.startDate.year = val[0].getYear() + 1900
                this.startDate.mon = val[0].getMonth() + 1
                this.startDate.day = val[0].getDate()
                this.startDate.hour = val[0].getHours()
                this.startDate.min = val[0].getMinutes()
                this.startDate.sec = val[0].getSeconds()

                this.endDate.year = val[1].getYear() + 1900
                this.endDate.mon = val[1].getMonth() + 1
                this.endDate.day = val[1].getDate()
                this.endDate.hour = val[1].getHours()
                this.endDate.min = val[1].getMinutes()
                this.endDate.sec = val[1].getSeconds()
            }
        }
    }
</script>

<style lang="stylus" rel="stylesheet/stylus">

</style>
