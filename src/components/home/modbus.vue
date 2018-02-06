<template>
    <div class="protocol modbus">
        <nav class="title">
            <i class="el-icon-setting"></i>
            配置 <span>(配置方式：选择限制的功能，完成后选择发送)</span>
        </nav>
        <div class="protocol-content">
            <el-form :model="configForm" ref="configForm" label-width="10px" class="demo-dynamic">
                <!--报警连接 开始-->
                <v-connection :connection="configForm.connection"></v-connection>
                <!--报警连接 结束-->

                <v-limit :fc_options="fc_options" :m_options="m_options" :restrictions="configForm.restrictions" :connection="configForm.connection"></v-limit>

                <div class="config">
                    <el-collapse accordion>
                        <el-collapse-item>
                            <template slot="title">
                                <nav class="config-titile">
                                    添加/移除 功能码
                                </nav>
                            </template>
                            <el-container>
                                <el-main>
                                    <el-transfer
                                            :titles="['功能码(可添加)', '功能码(可移除)']"
                                            filterable
                                            :filter-method="filterMethod"
                                            filter-placeholder="请输入功能码"
                                            :button-texts="['功能码栏 添加', '功能码栏 移除']"
                                            @change="handleChange"
                                            v-model="transfer_value"
                                            :data="fc_ad_data">
                                    </el-transfer>
                                </el-main>
                            </el-container>
                        </el-collapse-item>
                    </el-collapse>
                </div>
                <!-- 总提交按钮 -->
            </el-form>
            <div class="command">
                <el-button type="text" @click="showForm">显示</el-button>
                <el-button type="text" @click="verifyForm">验证</el-button>
                <el-button type="text" @click="submitForm">发送</el-button>
            </div>
        </div>

        <nav class="title">
            <i class="el-icon-setting"></i>
            监控 <span>(监控界面：每当设备收到不符合配置的数据包，信息将显示)</span>
        </nav>
        <div class="modbus-content">
            <alert-info></alert-info>
            <br>
        </div>
    </div>
</template>

<script>
    import connection from 'components/connection/connection';
    import alertInfo from './alertInfo';
    import limit from './limit';
    import {sortByLabel, removeByValue} from 'common/js/util';

    export default {
        components: {
            'v-connection': connection,
            'alert-info': alertInfo,
            'v-limit': limit
        },
        data() {
            return {
                fcodes: [],
                fc_options: [],
                m_options: [],
                memory_default_value: '',
                fc_ad_data: [],
                transfer_value: [],
                configForm: {
                    connection: {
                        ip: '127.0.0.1',
                        port: '8000'
                    },
                    restrictions: [
                        {
                            address: {
                                ip: '192.168.3.84',
                                mac: '08:d4:0c:a9:44:85',
                                default: true
                            },
                            function_codes: [
                                {
                                    fc_id: 3,
                                    default: true,
                                    excepts: [
                                        {
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
                                        }
                                    ]
                                }
                            ],
                            memories: [{
                            m_id: 2,
                            fc_id: 3,
                            default: true,
                            excepts: [
                                {
                                    start: '',
                                    end: ''
                                }
                            ]
                        }]
                        }
                    ]
                },
                filterMethod(query, item) {
                    return item.seq.indexOf(query) > -1;
                }
            };
        },
        created() {
            this.$http.get('/api/modbus').then((response) => {
                this.modbus_data = response.body.data;
                this.modbus_0 = this.modbus_data['function_code']['appendable'];
                this.modbus_1 = this.modbus_data['function_code']['appended'];
                this.modbus_m = this.modbus_data['memory'];

                for (let i in this.modbus_1) {
                    this.fc_options.push({'value': parseInt(i.split(' ')[0]), 'label': i});
                }
                ;
                for (let j in this.modbus_0) {
                    this.fcodes.push(j);
                }
                ;
                this.fcodes.forEach((fcode, index) => {
                    this.fc_ad_data.push({
                        label: fcode,
                        key: index,
                        seq: this.fcodes[index].split(' ')[0]
                    });
                });

                for (let k in this.modbus_m) {
                    this.m_options.push({'value': this.modbus_m[k], 'label': k});
                }
                ;
            });
        },
        methods: {
            showForm() {
                this.$alert('<strong>是否 <i>确定</i> 显示</strong>', 'Modbus 配置', {
                    dangerouslyUseHTMLString: true
                });
            },
            verifyForm() {
                this.$alert('<strong>是否 <i>确定</i> 验证</strong>', 'Modbus 配置', {
                    dangerouslyUseHTMLString: true
                });
            },
            submitForm() {
                this.$confirm('此操作将修改Modbus的配置文件, 是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    console.log(JSON.stringify(this.configForm, null, 4));
                    this.$socket.emit('setting', {'json': JSON.stringify(this.configForm, null, 4), 'type': 'modbus'});
                    this.$message({
                        type: 'success',
                        message: '发送成功!'
                    });
                }).catch(() => {
                    this.$message({
                        type: 'info',
                        message: '已取消发送!'
                    });
                });
            },
            resetForm(formName) {
                this.$refs[formName].resetFields();
            },
            handleChange(value, direction, movedKeys) {
                if (direction === 'right') {
                    for (let i in movedKeys) {
                        this.fc_options.push(
                                {
                                    'value': parseInt(this.fc_ad_data[movedKeys[i]]['label'].split(' ')[0]),
                                    'label': this.fc_ad_data[movedKeys[i]]['label']
                                }
                        );
                    }
                    this.$notify({
                        title: '添加',
                        message: '提示消息：添加成功',
                        type: 'success'
                    });
                } else {
                    for (let i in movedKeys) {
                        removeByValue(this.fc_options, this.fc_ad_data[movedKeys[i]]['label'].split(' ')[0]);
                    }
                    this.$notify({
                        title: '删除',
                        message: '提示消息：删除成功',
                        type: 'success'
                    });
                }
                this.fc_options.sort(sortByLabel);
            }
        },
        sockets: {
            connect() {
                this.$socket.emit('my_event', {data: 'I\'m connected!'});
            },
            alert(message) {
                if (message['type'] === 'modbus') {
                    console.log(message);
                }
            },
            setting(message) {
                console.log('设置成功or失败');
            }
        }
    };
</script>

<style lang="stylus" rel="stylesheet/stylus">
    .protocol
        margin: auto 0.8rem
        .protocol-content
        .modbus-content
            margin-bottom: 20px
            border: 1px solid #333
            border-radius: 0 0 5px 5px;
        .el-transfer
            width: 1000px
            .el-transfer-panel
                width: 400px
                height: 500px
                .el-transfer-panel__body
                    height: 446px
                    .is-filterable
                        height: 394px
        .el-form-item
            margin-bottom: 0
        .el-container
            margin: 10px 20px
            .el-aside
                background-color: #E9EEF3;
                color: #333;
                text-align: right;
                line-height: 200px;
            .el-main
                background-color: #E9EEF3;
                color: #333;
                text-align: left;
                border-radius: 5px;
        .el-header
        .el-footer
            margin: 5px 20px
            background-color: #B3C0D1;
            color: #333;
            text-align: center;
            line-height: 55px;
            border-radius: 5px;

        .title
            line-height: 4rem
            border-radius: 0.5rem 0.5rem 0 0
            padding-left: 1rem
            color: rgb(238, 238, 238)
            background: rgb(13, 1, 49)
            font-size: 2rem
            .el-icon-setting
                font-size: 2.5rem
                margin-right: 1rem
            .el-icon-arrow-up
                float: right
                margin: 1rem 2rem
                font-size: 3rem
        .command
            margin: 1rem 1.5rem 0
            border-top: 1px solid rgb(14, 32, 108);
            button
                margin: 1rem auto
                padding: 0.5rem 2rem
                font-size: 1.7rem
                border-radius: 1rem
                color: #fff
                background: rgb(9, 145, 143)
            button + button
                margin-left: 3rem

    .config
        margin: 1rem 1.5rem 0
        font-size: 2rem
        .config-titile
            line-height: 3rem
            border-radius: 0.5rem
            padding: 0 2rem
            background: rgb(145, 181, 231)
            .el-icon-arrow-up
                float: right
                margin: 1rem 1rem
        .content
            padding: 0 2rem

    .in-line
        margin: 10px auto

    .el-range-input
        width: 43% !important
</style>
