<template>
    <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item>{{title.h1}}</el-breadcrumb-item>
        <el-breadcrumb-item>{{title.h2}}</el-breadcrumb-item>
    </el-breadcrumb>
</template>

<script type="text/ecmascript-6">
    export default {
        props: {
            title: {
                type: Object
            }
        }
    };
</script>

<style lang="stylus" rel="stylesheet/stylus">

</style>