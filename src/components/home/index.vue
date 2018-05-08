<template>
    <div>
        <v-header></v-header>
        <keep-alive>
            <router-view></router-view>
        </keep-alive>
    </div>
</template>

<script type="text/ecmascript-6">
    import header from 'components/header/header.vue';
    import iec104 from './iec104.vue';
    import modbus from './modbus.vue';

    import {mapState} from 'vuex';

    export default {
        components: {
            'v-header': header,
            'iec104': iec104,
            'modbus': modbus
        },
        computed: {
            ...mapState(['isLogin'])
        },
        created() {
            // 如果已经登陆了，则进入协议栈页面
            if (!this.isLogin) {
                this.$router.push('/login');
            }
        }
    };
</script>

<style lang="stylus" rel="stylesheet/stylus">

</style>
