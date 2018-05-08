<template>
    <div class="config">
        <el-collapse v-model="activeNames" accordion>
            <el-collapse-item name="1">
                <template slot="title">
                    <nav class="config-titile">
                        报警连接
                    </nav>
                </template>
                <el-container>
                    <el-main>
                        <el-form :inline="true" :model="connection" class="demo-form-inline">
                            <el-form-item>
                                <el-input v-model="connection.ip" placeholder="请输入IP地址">
                                    <template slot="prepend">IP地址:</template>
                                </el-input>
                            </el-form-item>
                            <el-form-item>
                                <el-input v-model="connection.port" placeholder="请输入端口号">
                                    <template slot="prepend">端口号：</template>
                                </el-input>
                            </el-form-item>
                        </el-form>
                    </el-main>
                </el-container>
            </el-collapse-item>
        </el-collapse>
    </div>
</template>

<script type="text/ecmascript-6">
    export default {
        props: {
            connection: {
                type: Object
            }
        },
        data() {
            return {
                activeNames: '1'
            }
        }
    }
</script>

<style lang="stylus" rel="stylesheet/stylus">

</style>