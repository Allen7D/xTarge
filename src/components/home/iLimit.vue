<template>
    <div class="config">
        <el-collapse v-model="activeNames" accordion>
            <el-collapse-item name="1">
                <template slot="title">
                    <nav class="config-titile">
                        添加限制
                    </nav>
                </template>

                <el-header>
                    <el-button @click="addRestriction(restrictions)" type="primary"><i class="el-icon-plus">添加</i></el-button>
                    <el-button @click="remoteRestriction(restrictions)" :type="removeBtnType"><i class="el-icon-delete">删除</i></el-button>
                </el-header>

                <el-main class="clearfix">
                    <el-checkbox-group v-model="checkList">
                        <el-form v-for="(restriction, rIndex) in restrictions"
                                 :key="restriction.key">

                            <el-collapse accordion>
                                <el-collapse-item>

                                    <template slot="title">

                                        <el-form :inline="true" :model="restriction.address" class="demo-form-inline">
                                            <el-form-item>
                                                <el-checkbox :label="rIndex">限制 {{rIndex + 1}}:</el-checkbox>
                                            </el-form-item>
                                            <el-form-item>
                                                <el-input v-model="restriction.address.ip" placeholder="请输入IP地址">
                                                    <template slot="prepend">IP地址:</template>
                                                </el-input>
                                            </el-form-item>
                                            <el-form-item>
                                                <el-input v-model="restriction.address.mac" placeholder="请输入MAC地址">
                                                    <template slot="prepend">MAC地址：</template>
                                                </el-input>
                                            </el-form-item>

                                            <el-form-item>
                                                <el-switch v-model="restriction.address.default" active-text="开启" inactive-text="关闭">
                                                </el-switch>
                                            </el-form-item>
                                        </el-form>
                                    </template>

                                    <el-container>
                                        <el-main>
                                            <!--功能码限制 开始-->
                                            <fc-limit :fc_options="fc_options" :function_codes="restriction.function_codes"></fc-limit>
                                            <!--功能码限制 结束-->
                                        </el-main>
                                    </el-container>

                                </el-collapse-item>
                            </el-collapse>
                        </el-form>
                    </el-checkbox-group>
                </el-main>
            </el-collapse-item>
        </el-collapse>
    </div>
</template>

<script type="text/ecmascript-6">
    import functionCodeLimit from 'components/limit/functionCodeLimit'

    export default {
        components: {
            'fc-limit': functionCodeLimit
        },
        props: {
            restrictions: {
                type: Array
            },
            fc_options: {
                type: Array
            }
        },
        data() {
            return {
                checkList: [],
                activeNames: '1',
                removeBtnType: ''
            }
        },
        methods: {
            addRestriction(arr) {
                arr.push({
                    address: {
                        ip: '',
                        mac: '',
                        default: true
                    },
                    function_codes: [
                    ]
                })
            },
            remoteRestriction(arr) {
                for (let i in this.checkList) {
                    arr.splice(this.checkList[i], 1)
                }
                this.checkList.splice(0)
            }
        },
        watch: {
            checkList(val, oldVal) {
                if (val.length !== 0) {
                    this.removeBtnType = 'danger'
                } else {
                    this.removeBtnType = ''
                }
            }
        }
    }
</script>

<style lang="stylus" rel="stylesheet/stylus">

</style>
