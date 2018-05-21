<template>
    <div class="config">
        <el-collapse accordion>
            <el-collapse-item>
                <template slot="title">
                    <nav class="config-titile">
                        内存限制
                    </nav>
                </template>

                <el-form v-for="memory in memories" :key="memory.key">
                    <el-container>
                        <el-main>
                            <el-form-item :inline="true">
                                内存类型:
                                <!--<v-selection :remote_value.sync="memory.m_id" :options="m_options"></v-selection>-->
                                <el-select v-model="memory.id" placeholder="请选择">
                                    <el-option
                                            v-for="item in m_options"
                                            :key="item.id"
                                            :value="item.id"
                                            :label="item.value"
                                    >
                                    </el-option>
                                </el-select>
                                功能码：
                                <el-select v-model="memory.id2" placeholder="请选择">
                                    <el-option
                                            v-for="item in fc_options"
                                            :key="item.id"
                                            :value="item.id"
                                            :label="item.value"
                                    >
                                    </el-option>
                                </el-select>
                                默认打开：
                                <el-switch
                                        v-model="memory.default"
                                        active-text="默认打开"
                                        inactive-text="关闭">
                                </el-switch>
                            </el-form-item>
                            <el-form-item>
                                <el-form class="in-line" :inline="true"
                                         v-for="(except, index) in memory.excepts"
                                         :label="'例外 ' + index + ' :'"
                                         :key="except.key">
                                    开始地址:
                                    <el-form-item :rules="[]">
                                        <el-input v-model="except.start"></el-input>
                                    </el-form-item>

                                    结束地址:
                                    <el-form-item :rules="[]">
                                        <el-input v-model="except.end"></el-input>
                                    </el-form-item>
                                    <el-button type="danger" @click="removeArray(memory.excepts, except)">删除
                                    </el-button>
                                </el-form>

                            </el-form-item>
                        </el-main>
                        <el-aside width="20%">
                            <el-form-item :inline="true">
                                <el-button @click="addMemoryExcept(memory.excepts)">新增例外</el-button>
                                <el-button type="danger" @click="removeArray(memories, memory)">x
                                </el-button>
                            </el-form-item>
                        </el-aside>
                    </el-container>
                </el-form>

                <el-footer>
                    <el-button @click="addMemory(memories)"><i class="el-icon-plus">添加内存类型</i></el-button>
                </el-footer>
            </el-collapse-item>
        </el-collapse>
    </div>
</template>

<script type="text/ecmascript-6">
    import selection from 'base/selection.vue'
    import uniSwitch from 'base/uniSwitch'
    export default {
        components: {
            'v-selection': selection,
            'v-uni-switch': uniSwitch
        },
        props: {
            memories: {
                type: Array
            },
            fc_options: {
                type: Array
            },
            m_options: {
                type: Array
            }
        },
        methods: {
            addMemoryExcept(arr) {
                arr.push({
                    start: '',
                    end: ''
                })
            },
            addMemory(arr) {
                arr.push({
                    id: 1,
                    id2: 1,
                    default: true,
                    excepts: [
                    ]
                })
            },
            removeArray(arr, item) {
                var index = arr.indexOf(item)
                if (index !== -1) {
                    arr.splice(index, 1)
                }
            }
        }
    }
</script>

<style lang="stylus" rel="stylesheet/stylus">

</style>
