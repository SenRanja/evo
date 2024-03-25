<template>
  <div v-if="user_role == 'admin'">
    <!-- v-permission 会检查 store.stat.ruleNames 中是否存在这个别名，如果存在，就把这个控件留下 -->
    <!-- <IndexChart v-permission="['getStatistics3,GET']"/> -->

    <!-- 模块 统计面板模块 -->
    <el-row :gutter="20">

      <!-- el-skeleton标签就是用来显示一个占位符，没大用处，当api没有数据，触发下一行的v-if，页面会仅显示一个卡片的占位符而已。此部分注释不影响实际使用 -->
      <template v-if="panels.length == 0">
        <el-col :span="6" v-for="i in 4" :key="i">
          <el-skeleton style="width: 100%;" animated loading>
            <template #template>
              <el-card shadow="hover" class="border-0">
                <template #header>
                  <div class="flex justify-between">
                    <el-skeleton-item variant="text" style="width: 50%" />
                    <el-skeleton-item variant="text" style="width: 10%" />
                  </div>
                </template>
                <el-skeleton-item variant="h3" style="width: 80%" />
                <el-divider />
                <div class="flex justify-between text-sm text-gray-500">
                  <el-skeleton-item variant="text" style="width: 50%" />
                  <el-skeleton-item variant="text" style="width: 10%" />
                </div>
              </el-card>
            </template>
          </el-skeleton>
        </el-col>
      </template>

      <!-- 区别于上一部分，此部分是实际展示模块 -->
      <el-col :span="6" :offset="0" v-for="(item, index) in panels" :key="index">
        <el-card shadow="hover" class="border-0">
          <template #header>
            <div class="flex justify-between">
              <span class="text-sm">{{ item.title }}</span>
              <el-tag :type="item.unitColor" effect="plain">
                {{ item.unit }}
              </el-tag>
            </div>
          </template>
          <span class="text-3xl font-bold text-gray-500">
            <!-- <CountTo :value="item.value"/>-->
            {{ item.value }}
          </span>
          <el-divider />
          <div class="flex justify-between text-sm text-gray-500">
            <span>{{ item.subTitle }}</span>
            <span>{{ item.subValue }}</span>
          </div>
        </el-card>

      </el-col>
    </el-row>

    <!-- License可用性 -->
    <el-card shadow="never" class="border-0">
      <strong>License剩余天数：</strong><span>{{ left_days }}</span>
    </el-card>
    <br>
    <el-card shadow="never" class="border-0">
      <el-text class="mx-1" size="large" :type="license_danger_text_type"><strong>可用性安全性告警：</strong>{{ license_valid_bool }}</el-text>
    </el-card>

    <el-card shadow="never" class="border-0">
      <strong>可用性安全性告警原因：</strong><el-text class="mx-1" :type="license_danger_text_type">{{ license_valid_reason }}</el-text>
    </el-card>

    <!-- 模块 小图标导航 -->
    <IndexNavs />

    <el-row :gutter="20" class=" mt-5">

      <el-col :span="12" :offset="0">
        <!-- 模块 图表模块 -->
        <IndexChart v-permission="['getStatistics3,GET']" />
      </el-col>
      <el-col :span="12" :offset="0" v-permission="['getStatistics1,GET']">
        <!-- 模块 提示模块 -->
        <IndexCard title="近期公告" tip="公告管理" :btns="goods" class="mb-3" />
        <IndexCard title="考试场次" tip="考试管理" :btns="order" />
      </el-col>
      <el-col :span="12" :offset="0"></el-col>
    </el-row>
  </div>
  <div>
    <el-text class="mx-1" size="large">公告</el-text>
    <NoticeNav />
  </div>
  <div>
    <!-- <ExamQuesListNav/> -->
  </div>
  <br>
  <div>
    <el-text class="mx-1" size="large">成绩单</el-text>
    <ResultsManageNav />
  </div>
</template>
<script setup>
import { ref } from "vue"
// CountTo是 取整
import CountTo from "~/components/CountTo.vue";
import IndexNavs from "~/components/IndexNavs.vue";
import IndexChart from "~/components/IndexChart.vue";
import IndexCard from "~/components/IndexCard.vue";
import NoticeNav from "~/pages/notice/list.vue";
// import ExamQuesListNav from '~/pages/exam_questions/list.vue'
import ResultsManageNav from '~/pages/result/list.vue'
import { getSystemStatusMonitor, getStatistics2 } from "~/api/index.js"
import {
  getLicenseList,
  submitLicense,
} from "~/api/license"
import { useStore } from 'vuex'

const store = useStore()
const user_role = store.state.user.role

const loading = ref(false)

const total = ref(0)
const left_days = ref(0)
const license_valid_bool = ref(true)
const license_valid_reason = ref("")
let license_danger_text_type = ref()

// 获取数据
getLicenseList()
  .then(res => {
    total.value = res.total
    // license剩余可用时间
    left_days.value = res.msg.left_days
    // license安全文件是否被关闭
    license_valid_bool.value = res.msg.license_valid_bool
    console.log(license_valid_bool.value)
    if (license_valid_bool.value==true) {
      license_danger_text_type.value = "success"
    } else {
      license_danger_text_type.value = "danger"
    }

    license_valid_reason.value = res.msg.license_valid_reason
  })

const panels = ref([])
getSystemStatusMonitor()
  .then(res => {
    panels.value = res.data.panels
  })

const goods = ref([])
const order = ref([])
getStatistics2()
  .then(res => {
    goods.value = res.goods
    order.value = res.order
  })
</script>