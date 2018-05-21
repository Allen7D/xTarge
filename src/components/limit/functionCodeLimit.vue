<template>
    <div class="config">
        <el-collapse accordion>
            <el-collapse-item name="1">
                <template slot="title">
                    <nav class="config-titile">
                        功能码限制
                    </nav>
                </template>
                <el-form
                        v-for="(function_code, fcIndex) in function_codes"
                        :key="function_code.key"
                >
                    <el-container>
                        <el-main class="clearfix">
                            <el-form-item :inline="true">
                                功能码{{fcIndex}}：

                                <el-select v-model="function_code.id" placeholder="请选择">
                                    <el-option v-for="item in fc_options"
                                            :key="item.id" :value="item.id" :label="item.value"
                                    >
                                    </el-option>
                                </el-select>

                                默认打开：
                                <el-switch
                                        v-model="function_code.default"
                                        active-text="开启"
                                        inactive-text="关闭">
                                </el-switch>

                            </el-form-item>
                            <el-form-item>
                                <el-form class="in-line"
                                         :inline="true"
                                         v-for="(except, exceptIndex) in function_code.excepts"
                                         :label="'例外 ' + exceptIndex + ' :'"
                                         :key="except.key">
                                    <el-form-item>
                                        <v-date-time-picker :startDate="except.start"
                                                            :endDate="except.end"></v-date-time-picker>
                                    </el-form-item>
                                    <el-button type="danger"
                                               @click.prevent="removeArray(function_code.excepts, except)">删除
                                    </el-button>
                                </el-form>
                            </el-form-item>
                        </el-main>
                        <el-aside width="20%">
                            <el-form-item>
                                <el-button @click="addFunctionCodeExcept(function_code.excepts)">新增例外</el-button>
                                <el-button type="danger" @click.prevent="removeArray(function_codes, function_code)">x
                                </el-button>
                            </el-form-item>
                        </el-aside>
                    </el-container>
                </el-form>

                <el-footer>
                    <el-button @click="addFunctionCode(function_codes)"><i class="el-icon-plus">添加功能码</i></el-button>
                </el-footer>
            </el-collapse-item>
        </el-collapse>
    </div>
</template>

<script type="text/ecmascript-6">
    import selection from 'base/selection'
    import uniSwitch from 'base/uniSwitch'
    import dateTimePicker from 'base/dateTimePicker'

    export default {
        components: {
            'v-selection': selection,
            'v-uni-switch': uniSwitch,
            'v-date-time-picker': dateTimePicker
        },
        props: {
            fc_options: {
                type: Array
            },
            function_codes: {
                type: Array
            }
        },
        methods: {
            addFunctionCodeExcept(arr) {
                arr.push({
                    start: {
                        year: -1,
                        mon: -1,
                        day: -1,
                        hour: -1,
                        min: -1,
                        sec: -1,
                        wday: -1
                    },
                    end: {
                        year: -1,
                        mon: -1,
                        day: -1,
                        hour: -1,
                        min: -1,
                        sec: -1,
                        wday: -1
                    }
                })
            },
            addFunctionCode(arr) {
                arr.push({
                    id: 1,
                    default: true,
                    excepts: []
                })
            },
            removeArray(arr, item) {
                var index = arr.indexOf(item)
                if (index !== -1) {
                    arr.splice(index, 1)
                }
            }
        }
    }
</script>

<style lang="stylus" rel="stylesheet/stylus">

</style>
