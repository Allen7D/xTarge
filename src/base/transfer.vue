<template>
    <el-transfer
                 :titles="['功能码(可添加)', '功能码(可移除)']"
                 filterable
                 :filter-method="filterMethod"
                 filter-placeholder="请输入功能码"
                 :button-texts="['功能码栏 添加', '功能码栏 移除']"
                 @change="handleChange"
                 v-model="transfer_value"
                 :data="data">
    </el-transfer>
</template>

<script type="text/ecmascript-6">
    export default {
        probs: {
            data: {
                type: Object
            }
        },
        data() {
            return {
                transfer_value: [],
                filterMethod(query, item) {
                    return item.seq.indexOf(query) > -1;
                }
            }
        },
        methods: {
            handleChange(value, direction, movedKeys) {
                var sortByLabel = function (a, b) {
                    return a.value - b.value;
                };

                var removeByValue = function (arr, val) {
                    for (let i = 0; i < arr.length; i++) {
                        if (arr[i].value === val) {
                            arr.splice(i, 1);
                            break;
                        }
                    }
                };

                if (direction === 'right') {
                    for (let i in movedKeys) {
                        this.fc_options.push(
                                {
                                    'value': this.fc_ad_data[movedKeys[i]]['label'].split(' ')[0],
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
        }
    };
</script>

<style lang="stylus" rel="stylesheet/stylus">

</style>