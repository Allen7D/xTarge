<template>
    <div class="header">
        <nav class="top clearfix">
            <a href="/modbus" class="brand"><img src="./logo.jpg" alt="首页"></a>
            <h2>安全协议栈配置与监控界面</h2>
            <ul>
                <li><router-link to="/admin/user">用户: {{username}}</router-link></li>
                <li><router-link to="/modbus">协议设置</router-link></li>
                <li ><a @click="logout">退出</a></li>
            </ul>
        </nav>
    </div>
</template>


<script type="text/ecmascript-6">
    import {mapState} from 'vuex';
    export default {
        computed: {
            ...mapState(['isLogin', 'username'])
        },
        methods: {
            logout() {
                localStorage['username'] = '';
                localStorage['isLogin'] = false;
                this.$router.push('/login');
            }
        }
    };
</script>

<style lang="stylus" rel="stylesheet/stylus">

</style>