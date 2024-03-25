<template>
  <el-row :gutter="20" class=" mt-5">
    <el-col :span="3" :offset="0" v-for="(item, index) in iconNavs" :key="index">
      <el-card shadow="hover" @click="$router.push(item.path)">
        <div class="flex flex-col items-center justify-center cursor-pointer">
          <el-icon :size="16" :class="item.color">
            <component :is="item.icon"/>
          </el-icon>
          <span class="text-sm mt-2">{{ item.title }}</span>
        </div>
      </el-card>

    </el-col>
  </el-row>
</template>


<script setup>

const iconNavs = [
  {
    icon: "user",
    color: "text-light-blue-500",
    title: "用户",
    path: "/user/manage"
  },
  {
    icon: "set-up",
    color: "text-grey-500",
    title: "公告",
    path: "/notice/list"
  },
  {
    icon: "tickets",
    color: "text-fuchsia-500",
    title: "考试",
    path: "/exam/manage"
  },
  {
    icon: "chat-dot-square",
    color: "text-teal-500",
    title: "成绩单",
    path: "/result/manage"
  },
  {
    icon: "picture",
    color: "text-rose-500",
    title: "题库",
    path: "/question/change"
  },
  {
    icon: "bell",
    color: "text-green-500",
    title: "视频（待做）",
    path: "/notice/list"
  },
  {
    icon: "files",
    color: "/setting/base",
    title: "系统",
    path: "/coupon/list"
  },
  {
    icon: "chat-dot-square",
    color: "text-teal-500",
    title: "AI判分（待做）",
    path: "/comment/list"
  }
]
</script>