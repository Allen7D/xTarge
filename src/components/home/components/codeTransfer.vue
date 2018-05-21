<template>
  <el-dialog title="添加/移除 功能码" center :visible.sync="isVisible" width="1050px" @close="handleHide">
    <el-transfer
      :titles="['功能码(可添加)', '功能码(可移除)']"
      filterable :filter-method="filterMethod" filter-placeholder="请输入功能码"
      :button-texts="['功能码栏 移除', '功能码栏 添加']"
      @change="handleChange" v-model="tempValue" :data="reserveValue">
    </el-transfer>
  </el-dialog>
</template>

<script type="text/ecmascript-6">
  import { sortByID, removeByValue, convertData } from 'common/js/util'
  export default {
    props: {
      isShow: {
        type: Boolean,
        default: false
      },
      updateCode: {
        type: Function
      },
      currentCode: {
        type: Array
      },
      reserveCode: {
        type: Array
      }
    },
    data() {
      return {
        isVisible: this.isShow,
        tempValue: [],
        filterMethod(query, item) {
          return item.seq.indexOf(query) > -1
        }
      }
    },
    computed: {
      reserveValue() {
        return convertData(this.reserveCode)
      }
    },
    watch: {
      isShow() {
        this.isVisible = this.isShow
      }
    },
    methods: {
      handleHide() {
        this.$emit('update:isShow', false)
      },
      handleChange(value, direction, movedKeys) {
        // value为右侧的数据的key; movedKeys为移动中的数据的key
        if (direction === 'right') {
          for (let index in movedKeys) {
            this.currentCode.push(this.reserveCode[movedKeys[index]])
          }
          this.currentCode.sort(sortByID)
        } else {
          for (let index in movedKeys) {
            removeByValue(this.currentCode, this.reserveCode[movedKeys[index]].id)
          }
        }
        this.updateCode(this.currentCode)
      }
    }
  }
</script>

<style scoped lang="stylus" rel="stylesheet/stylus">

</style>