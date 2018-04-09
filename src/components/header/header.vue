<template>
    <div>
        <div class="header">
            <nav class="top clearfix">
                <a class="brand"><img src="./logo.jpg" alt="首页"></a>
                <h2>安全协议栈配置与监控界面</h2>
                <ul>
                    <li>
                        <router-link to="/admin/user">用户: {{fullName}}</router-link>
                    </li>
                    <li><a @click="logout">退出</a></li>
                </ul>
            </nav>
        </div>
        <nav class="header-tab">
            <div class="tab-item" :class="{ active: isIec104 }" @click="toIec104">
                <router-link to="/iec104">IEC104</router-link>
            </div>
            <div class="tab-item" :class="{ active: isModbus }" @click="toModbus">
                <router-link to="/modbus">Modbus</router-link>
            </div>
        </nav>
        <div class="header-detail" :style="{textIndent: tt + 'px' }">{{protocol}}安全协议栈配置与监控界面</div>
    </div>
</template>


<script type="text/ecmascript-6">
    import {mapState} from 'vuex';
    export default {
        data() {
            return {
                protocol: 'Modbus',
                isIec104: false,
                isModbus: true,
                tt: 190
            };
        },
        mounted () {
            if (this.$route.path === '/iec104') {
                this.isIec104 = true;
                this.isModbus = false;
                this.protocol = 'IEC104';
                this.tt = 45;
            }
        },
        computed: {
            ...mapState(['isLogin']),
            fullName () {
                return this.$store.getters.fullName;
            }
        },
        methods: {
            toIec104() {
                this.$router.push('/iec104');
            },
            toModbus() {
                this.$router.push('/modbus');
            },
            logout() {
                localStorage['username'] = '';
                localStorage['isLogin'] = false;
                localStorage['level'] = '';

                this.$router.push('/login');
            },
            modifyTitle() {
                if (this.$route.path === '/iec104') {
                    this.isIec104 = true;
                    this.isModbus = false;
                    this.protocol = 'IEC104';
                    this.tt = 45;
                } else {
                    this.isIec104 = false;
                    this.isModbus = true;
                    this.protocol = 'Modbus';
                    this.tt = 190;
                }
            }
        },
        watch: {
            '$route': 'modifyTitle'
        }
    };
</script>

<style lang="stylus" rel="stylesheet/stylus">
    .header
        background: rgba(14, 32, 108, 1.0)
        font-size: 1.8rem
        color: #fff
        .top
            .brand
                float: left
                padding: 1.5rem 2rem 0
                img
                    width: 210px
                    height: 50px
            h2
                text-align: center
                font-size: 3rem
                letter-spacing: 1rem
                text-indent: 1rem
                margin-right: 270px
            ul
                float: right;
                margin: -2rem 2rem
                li
                    display: inline-block
                    padding: 0 15px
                    a
                        color: #fff

    .header-tab
        display: flex
        background: rgb(13, 1, 49)
        font-size: 1.8rem
        .tab-item
            text-align: center
            padding: 0.8rem 3rem
            a
                text-decoration: none
                color: rgb(238, 238, 238)
        .active
            background: rgb(238, 238, 238)
            a
                color: rgb(13, 1, 49)

    .header-detail
        line-height: 4rem
        font-size: 1.8rem
        background: rgb(238, 238, 238)
        color: rgb(14, 32, 108)
        text-indent: 45px

</style>