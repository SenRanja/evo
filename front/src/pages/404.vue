<template>
  <div>
    <el-col :sm="12" :lg="6">
      <el-result
          icon="warning"
          title="404 页面走丢了"
          sub-title="你找的页面走丢了"
      >
        <template #extra>
          <el-button type="primary" @click="$router.push('/')">回到首页</el-button>
        </template>
      </el-result>
    </el-col>
  </div>
</template>