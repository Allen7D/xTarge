<template>
    <div class="admin">
        <v-header2></v-header2>
        <el-container>
            <el-aside width="200px">
                <el-row class="tac">
                    <el-menu
                            default-active="2"
                            class="el-menu-vertical-demo"
                            @open="handleOpen"
                            @close="handleClose">

                        <el-submenu index="1">
                            <template slot="title">
                                <i class="el-icon-location"></i>
                                <span>日志管理</span>
                            </template>
                            <el-menu-item-group>
                                <el-menu-item index="1-1" @click="opLogOpen">操作日志</el-menu-item>
                                <el-menu-item index="1-2" @click="alertLogOpen">报警日志</el-menu-item>
                            </el-menu-item-group>
                        </el-submenu>

                        <el-submenu index="2">
                            <template slot="title">
                                <i class="el-icon-menu"></i>
                                <span slot="title">用户管理</span>
                            </template>
                            <el-menu-item-group>
                                <el-menu-item index="2-1" @click="userOpen">用户列表</el-menu-item>
                            </el-menu-item-group>
                        </el-submenu>

                    </el-menu>
                </el-row>

            </el-aside>

            <el-container>
                <el-header>
                    <user-header :title="title"></user-header>
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
    import header2 from 'components/header/header2.vue';
    import user from './user';
    import alertLog from './alertLog';
    import opLog from './opLog';
    import userHeader from './userHeader';

    import {mapState} from 'vuex';

    export default {
        components: {
            'v-header2': header2,
            'user': user,
            'alert-log': alertLog,
            'op-log': opLog,
            'user-header': userHeader
        },
        data() {
            return {
                title: {
                    h1: '用户管理',
                    h2: '用户列表'
                }
            };
        },
        computed: {
            ...mapState(['isLogin'])
        },
        created() {
            // 如果已经登陆了，则进入协议栈页面
            if (!this.isLogin) {
                this.$router.push('/login');
            }
        },
        methods: {
            userOpen() {
                this.title.h1 = '用户管理';
                this.title.h2 = '用户列表';
                this.$router.push({path: '/admin/user'});
            },
            opLogOpen() {
                this.title.h1 = '日志管理';
                this.title.h2 = '操作日志';
                this.$router.push({path: '/admin/oplog'});
            },
            alertLogOpen() {
                this.title.h1 = '日志管理';
                this.title.h2 = '报警日志';
                this.$router.push({path: '/admin/alertlog'});
            },
            handleOpen(key, keyPath) {
                console.log(key, keyPath);
            },
            handleClose(key, keyPath) {
                console.log(key, keyPath);
            }
        }
    };
</script>

<style lang="stylus" rel="stylesheet/stylus">
    .admin
        .el-header
            background-color: white
            color: #333;
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
            /*line-height: 160px 奔溃了*/
</style>