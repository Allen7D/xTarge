<template>
    <div class="user">
        <div>
            <el-button type="primary" icon="el-icon-circle-plus" @click="addUserVisible = true"> 添加用户</el-button>
        </div>
        <el-table
                ref="multipleTable"
                :data="userList"
                tooltip-effect="dark"
                style="width: 1000px"
                border
                @selection-change="handleSelectionChange">
            <el-table-column
                    type="selection"
                    width="55">
            </el-table-column>
            <el-table-column
                    prop="id"
                    label="ID"
                    width="80">
            </el-table-column>
            <el-table-column
                    prop="username"
                    label="登录名"
                    width="150"
                    show-overflow-tooltip>
            </el-table-column>
            <el-table-column
                    prop="pass"
                    label="密码"
                    width="150"
                    show-overflow-tooltip>
            </el-table-column>
            <el-table-column
                    prop="level"
                    label="权限"
                    width="80"
                    show-overflow-tooltip>
            </el-table-column>
            <el-table-column
                    label="注册日期">
                <template slot-scope="scope">
                    <i class="el-icon-time"></i>
                    <span style="margin-left: 10px">{{ scope.row.date }}</span>
                </template>
            </el-table-column>
            <el-table-column width="200" label="编辑">
                <template slot-scope="scope">
                    <el-button
                            size="mini"
                            @click="editUser(scope.$index, scope.row)">编辑
                    </el-button>
                    <el-button
                            size="mini"
                            type="danger"
                            @click="deleteUser(scope.$index, scope.row)">删除
                    </el-button>
                </template>
            </el-table-column>
        </el-table>

        <div class="add-user">
            <el-dialog title="添加管理员" center :visible.sync="addUserVisible">
                <el-form :model="currentUser" status-icon :rules="registerRules" ref="currentUser">
                    <el-form-item label="ID" prop="id" :label-width="formLabelWidth">
                        <el-input v-model="currentUser.id" auto-complete="off"></el-input>
                    </el-form-item>
                    <el-form-item label="用户名" prop="username" :label-width="formLabelWidth">
                        <el-input v-model="currentUser.username" auto-complete="off"></el-input>
                    </el-form-item>
                    <el-form-item label="密码" prop="pass" :label-width="formLabelWidth">
                        <el-input type="password" v-model="currentUser.pass" auto-complete="off"></el-input>
                    </el-form-item>
                    <el-form-item label="确认密码" prop="checkPass" :label-width="formLabelWidth">
                        <el-input type="password" v-model="currentUser.checkPass" auto-complete="off"></el-input>
                    </el-form-item>
                    <el-form-item label="权限级别" :label-width="formLabelWidth">
                        <el-select v-model="currentUser.level" placeholder="请选择管理员权限">
                            <el-option label="超级管理员:level A" value="A"></el-option>
                            <el-option label="高级管理员:level B" value="B"></el-option>
                            <el-option label="普通管理员:level C" value="C"></el-option>
                        </el-select>
                    </el-form-item>
                </el-form>
                <div slot="footer" class="dialog-footer">
                    <el-button @click="addUserVisible = false">取 消</el-button>
                    <el-button type="primary" @click="handleAddUser(userList, currentUser)">确 定</el-button>
                </div>
            </el-dialog>
        </div>


        <div class="edit-user">
            <el-dialog title="修改管理员" center :visible.sync="editUserVisible">
                <el-form :model="currentUser" status-icon :rules="registerRules" ref="currentUser">
                    <el-form-item label="ID" prop="id" :label-width="formLabelWidth">
                        <el-input v-model="currentUser.id" auto-complete="off" :disabled="true"></el-input>
                    </el-form-item>
                    <el-form-item label="用户名" prop="username" :label-width="formLabelWidth">
                        <el-input v-model="currentUser.username" auto-complete="off" :disabled="true"></el-input>
                    </el-form-item>
                    <el-form-item label="新密码" prop="pass" :label-width="formLabelWidth">
                        <el-input type="password" v-model="currentUser.pass" auto-complete="off"></el-input>
                    </el-form-item>
                    <el-form-item label="确认新密码" prop="checkPass" :label-width="formLabelWidth">
                        <el-input type="password" v-model="currentUser.checkPass" auto-complete="off"></el-input>
                    </el-form-item>
                    <el-form-item label="权限级别" :label-width="formLabelWidth">
                        <el-select v-model="currentUser.level" placeholder="请选择管理员权限">
                            <el-option label="超级管理员:level A" value="A"  v-show="opLevel <= 'A'"></el-option>
                            <el-option label="高级管理员:level B" value="B" v-show="opLevel <= 'B'"></el-option>
                            <el-option label="普通管理员:level C" value="C"></el-option>
                        </el-select>
                    </el-form-item>
                </el-form>
                <div slot="footer" class="dialog-footer">
                    <el-button @click="editUserVisible = false">取 消</el-button>
                    <el-button type="primary" @click="handleEditUser(123)">确 定</el-button>
                </div>
            </el-dialog>
        </div>


    </div>
</template>

<script type="text/ecmascript-6">
    import axios from 'axios';

    export default {
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
                registerRules: {
                    pass: [
                        {validator: validatePass, trigger: 'blur'}
                    ],
                    checkPass: [
                        {validator: validatePass2, trigger: 'blur'}
                    ]
                },
                formLabelWidth: '120px',
                userList: [{
                    id: '0001',
                    date: '2016/05/03 上午4:33:15',
                    username: 'super_admin',
                    pass: '159951',
                    level: 'A'
                }, {
                    id: '0002',
                    date: '2016/05/02 下午5:25:25',
                    username: 'high_level_admin',
                    pass: '000000',
                    level: 'B'
                }, {
                    id: '0003',
                    date: '2016/05/04 下午4:28:15',
                    username: 'normal_admin',
                    pass: '888888',
                    level: 'C'
                }],
                currentUser: {
                    username: '',
                    pass: '',
                    checkPass: '',
                    level: ''
                },
                multipleSelection: [],
                addUserVisible: false,
                editUserVisible: false,
                opLevel: localStorage['level']
            };
        },
        created() {
            axios.get('/api/all_users')
                    .then((res) => {
                        res.data.forEach((item, index) => {
                            this.userList.push({
                                id: item.id,
                                date: '没有注册时间',
                                username: item.username,
                                pass: '******',
                                level: item.level
                            });
                        });
                    });
        },
        methods: {
            handleSelectionChange(val) {
                this.multipleSelection = val;
            },
            editUser(index, row) {
                if (parseInt(localStorage['id']) !== parseInt(row.id)) {
                    if (localStorage['level'] && localStorage['level'] >= row.level) {
                        this.$notify({
                            title: '警告',
                            message: '当前用户的权限不够，无法进行相应的操作！',
                            type: 'warning'
                        });
                        return false;
                    }
                }

                this.currentUser.id = row.id;
                this.currentUser.username = row.username;
                this.currentUser.level = row.level;
                this.editUserVisible = true;
                console.log(this.opLevel);
            },
            deleteUser(index, row) {
                if (localStorage['level'] && localStorage['level'] >= row.level) {
                    this.$notify({
                        title: '警告',
                        message: '当前用户的权限不够，无法进行相应的操作！',
                        type: 'warning'
                    });
                    return false;
                }
                this.$confirm('此操作将永久删除该账户, 是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    this.$message({
                        type: 'success',
                        message: '删除成功!'
                    });
                    this.userList.splice(index, 1);
                }).catch(() => {
                    this.$message({
                        type: 'info',
                        message: '已取消删除'
                    });
                });
            },
            handleAddUser(arr, item) {
                if (!(item.id && item.username && item.pass && item.level)) {
                    this.$notify({
                        title: '警告',
                        message: '未填写完整信息，无法进行相应的操作！',
                        type: 'warning'
                    });
                    return false;
                }
                arr.push({
                    id: item.id,
                    date: (new Date()).toLocaleString(),
                    username: item.username,
                    pass: item.pass,
                    level: item.level || 'C'
                });
                this.addUserVisible = false;
            },
            handleEditUser(arr) {
                console.log(arr);
                this.isEditUser = false;
            }
        }
    };
</script>

<style lang="stylus" rel="stylesheet/stylus">
    .user
        .el-button
            margin-bottom: 10px

</style>