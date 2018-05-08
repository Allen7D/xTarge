<template>
    <div class="admin">
        <x-header></x-header>
        <el-container>
            <el-aside width="200px">
                <el-row class="tac">
                    <el-menu default-active="2" class="el-menu-vertical-demo">

                        <el-submenu index="1">
                            <template slot="title">
                                <i class="el-icon-location"></i>
                                <span>日志管理</span>
                            </template>
                            <el-menu-item-group>
                                <el-menu-item index="1-1" @click="handleToOperate">操作日志</el-menu-item>
                                <el-menu-item index="1-2" @click="handleToAlert">报警日志</el-menu-item>
                            </el-menu-item-group>
                        </el-submenu>

                        <el-submenu index="2">
                            <template slot="title">
                                <i class="el-icon-menu"></i>
                                <span slot="title">用户管理</span>
                            </template>
                            <el-menu-item-group>
                                <el-menu-item index="2-1" @click="handleToUser">用户列表</el-menu-item>
                            </el-menu-item-group>
                        </el-submenu>

                    </el-menu>
                </el-row>

            </el-aside>

            <el-container>
                <el-header>
                    <breadcrumb></breadcrumb>
                </el-header>
                <el-main>
                    <keep-alive>
                        <router-view></router-view>
                    </keep-alive>
                </el-main>
            </el-container>
        </el-container>
    </div>
</template>

<script type="text/ecmascript-6">
    import XHeader from 'components/header/header.vue'
    import User from './user'
    import Alert from './alert'
    import Operate from './operate'
    import Breadcrumb from './components/breadcrumb'

    import {mapState} from 'vuex'

    export default {
        components: {
            XHeader,
            User,
            Alert,
            Operate,
            Breadcrumb
        },
        data() {
            return {
            }
        },
        computed: {
            ...mapState(['isLogin'])
        },
        created() {
            // 如果已经登陆了，则进入协议栈页面
            if (!this.isLogin) {
                this.$router.push('/login')
            }
        },
        methods: {
            handleToUser() {
                this.$router.push({path: '/admin/user'})
            },
            handleToOperate() {
                this.$router.push({path: '/admin/operate'})
            },
            handleToAlert() {
                this.$router.push({path: '/admin/alert'})
            }
        }
    }
</script>

<style lang="stylus" rel="stylesheet/stylus">
    .admin
        .el-header
            background-color: white
            color: #333
            text-align: left
            line-height: 30px
            height: 40px !important
            padding-top: 12px

        .el-aside
            background-color: #D3DCE6
            color: #333
            text-align: left
        .el-main
            background-color: #E9EEF3
            color: #333
            text-align: left
</style>
