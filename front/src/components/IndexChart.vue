<template>
  <div>
    <el-card shadow="never">
      <template #header>
        <div class="flex justify-between">
          <span class="text-lg font-bold">数据统计</span>
          <div>
            <el-check-tag v-for="(item, index) in options" :key="index" :checked="current == item.value"
                          style="margin-right: 8px" @click="handleChoose(item.value)">{{ item.text }}
            </el-check-tag>
          </div>
        </div>
      </template>

      <div ref="el" id="chart" style="width: 100%;height: 300px;">

      </div>

    </el-card>

  </div>
</template>

<script setup>
import {onBeforeMount, onMounted, ref} from 'vue'
import * as echarts from 'echarts';
import {useResizeObserver} from '@vueuse/core'

import {getStatistics3} from "~/api/index.js"

const current = ref('week')
const handleChoose = (type) => {
  current.value = type

  console.log('调用handle')
  getData()
}

const options = [
  {
    text: '近一个月',
    value: 'month'
  }, {
    text: '近一周',
    value: 'week'
  }, {
    text: '近24小时',
    value: 'day'
  }
]

// 绘制图表
var myChart = null;
onMounted(() => {
  var chartDom = document.getElementById('chart');
  if (chartDom) {
    myChart = echarts.init(chartDom);
    getData()
  }
})

// 容器销毁后，销毁实例
onBeforeMount(() => {
  if (myChart) echarts.dispose(myChart)
})

function getData() {
  let option = {
    xAxis: {
      type: 'category',
      data: []
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        data: [],
        type: 'bar',
        showBackground: true,
        backgroundStyle: {
          color: 'rgba(180, 180, 180, 0.2)'
        }
      }
    ]
  };

  myChart.showLoading();
  getStatistics3(current.value).then(res => {
    option.xAxis.data = res.x
    option.series[0].data = res.y

    myChart.setOption(option);
  }).finally(() => {
    myChart.hideLoading();
  })
}

// 图表自适应，等比缩放
const el = ref(null)
useResizeObserver(el, (entries) => {
  if (myChart) {
    myChart.resize()
  }
})

</script>