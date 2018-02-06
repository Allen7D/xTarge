<template>
    <div class="edit-user">
        <el-dialog title="修改管理员" center :visible.sync="isEditUser">
            <el-form :model="form" status-icon :rules="registerRules" ref="form">
                <el-form-item label="用户名" prop="username" :label-width="formLabelWidth">
                    <el-input v-model="form.username" auto-complete="off"></el-input>
                </el-form-item>
                <el-form-item label="密码" prop="pass" :label-width="formLabelWidth">
                    <el-input type="password" v-model="form.pass" auto-complete="off"></el-input>
                </el-form-item>
                <el-form-item label="确认密码" prop="checkPass" :label-width="formLabelWidth">
                    <el-input type="password" v-model="form.checkPass" auto-complete="off"></el-input>
                </el-form-item>
                <el-form-item label="权限级别" :label-width="formLabelWidth">
                    <el-select v-model="form.level" placeholder="请选择管理员权限">
                        <el-option label="超级管理员:level A" value="A"></el-option>
                        <el-option label="高级管理员:level B" value="B"></el-option>
                        <el-option label="普通管理员:level C" value="C"></el-option>
                    </el-select>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click="isEditUser = false">取 消</el-button>
                <el-button type="primary" @click="handleEditUser(formArray)">确 定</el-button>
            </div>
        </el-dialog>
    </div>
</template>

<script type="text/ecmascript-6">
    export default {
        props: {
            formArray: {
                type: Array
            },
            user: {
                type: Object
            },
            remote_value: {
                type: Boolean
            }
        },
        data() {
            var validatePass = (rule, value, callback) => {
                if (value === '') {
                    callback(new Error('请输入密码'));
                } else {
                    if (this.form.checkPass !== '') {
                        this.$refs.form.validateField('checkPass');
                    }
                    callback();
                }
            };
            var validatePass2 = (rule, value, callback) => {
                if (value === '') {
                    callback(new Error('请再次输入密码'));
                } else if (value !== this.form.pass) {
                    callback(new Error('两次输入密码不一致!'));
                } else {
                    callback();
                }
            };
            return {
                isEditUser: this.remote_value,
                form: {
                    id: this.user.id,
                    username: this.user.username,
                    pass: '',
                    checkPass: '',
                    level: this.user.level
                },
                registerRules: {
                    pass: [
                        {validator: validatePass, trigger: 'blur'}
                    ],
                    checkPass: [
                        {validator: validatePass2, trigger: 'blur'}
                    ]
                },
                formLabelWidth: '120px'
            };
        },
        watch: {
            isEditUser(val) {
                console.log('hehe', val);
                this.$emit('update: remote_value', val);
            }
        },
        methods: {
            handleEditUser(arr) {
                arr.push({
                    id: this.user.id,
                    date: (new Date()).toLocaleString(),
                    username: this.user.username,
                    pass: this.form.pass,
                    level: this.form.level
                });
                this.isEditUser = false;
            }
        }
    };
</script>

<style lang="stylus" rel="stylesheet/stylus">

</style>