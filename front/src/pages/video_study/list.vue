<template>
  <div v-if="subjectId">
    <el-container class="bg-white rounded" :style="{ height: (h + 'px') }">
      <el-header class="image-header">
        <el-button type="primary" size="small" @click="selectVideo">选择视频</el-button>
      </el-header>

      <el-aside width="200px">

      </el-aside>
      <el-main>
        <StudyVideoMain :videoSource="newVideoSource" :poster="newPoster" />
      </el-main>
    </el-container>

    <FormDrawer ref="formDrawerRef" :title="drawerTitle" @submit="handleSubmit">
      <template v-for="(item, index) in tableData" :key="index">

        <!-- 选择什么视频 -->
        <el-button type="primary" @click="changeVideoSource(item.filename)">{{ item.title }}</el-button>


        <div v-if="!item.push && user_role === 'admin'">
          <!-- <div v-if="!item.push"> -->
          <!-- <br> -->
          视频名称：<el-input v-model="item.title" style="width: 90px">{{ item.title }}</el-input>
          次序：<el-input v-model="item.order" style="width: 90px">{{ item.order }}</el-input>
          <el-button type="info" @click="changeVideoOrder(item)">更改</el-button>
          <el-button type="danger" @click="deleteVideoSource(item.id)">删除</el-button>
        </div>
        <!-- <div v-else> -->
        <div v-else-if="item.push && user_role === 'admin'">
          <input type="file" @change="getFile($event)">视频文件</input>
          <br>
          视频名称 <el-input v-model="item.title" style="width: 300px" @change="getTitle(item.title)"></el-input>
          <br>
          次序 <el-input v-model="item.order" style="width: 90px" @change="getOrder(item.order)"></el-input>
        </div>
        <br>
      </template>
      <el-button type="text" @click="handleAddItem" v-if="user_role == 'admin'">上传视频(一次上传一个视频，点击下面“提交”)</el-button>
    </FormDrawer>
  </div>
  <div v-else>
    请从“课程管理”进入“视频学习”
  </div>
</template>

<script setup>
import { ref, reactive } from "vue";
import { useRouter } from 'vue-router';
import FormDrawer from "~/components/FormDrawer.vue";
import StudyVideoMain from "~/components/StudyVideoMain.vue";
import {
  get_video_by_subject,
  uploadFile,
  video_put,
  video_del,
} from "~/api/video";
import { useStore } from 'vuex'

const store = useStore()
const user_role = store.state.user.role

// 表单部分
const editId = ref(0)
const loading = ref(false)
const formDrawerRef = ref(null)
const formRef = ref(null)
const tableData = ref([])
const form = reactive({
  title: "",
  description: "",
  filename: "",
})

const selectVideo = () => {
  formDrawerRef.value.open()
}

const router = useRouter(); // 定义 router 常量
const subjectId = router.currentRoute.value.query.subjectId; // 获取 学科Id
console.log("接收的路由跳转来的学科Id", subjectId)
if(!subjectId) {
  router.push({name: "/subject/list"})
}


// 获取数据
function getData(subjectId) {
  loading.value = true
  get_video_by_subject(subjectId)
    .then(res => {
      tableData.value = res.data
    })
    .finally(() => {
      loading.value = false
    })
}

getData(subjectId)

// 源地址，给 视频组件 传参
// 用户更改播放源
const newVideoSource = ref("/static/media/videos/");
// const newPoster = "http://localhost:81/new-poster.png";
const changeVideoSource = (filename) => {
  console.log("播放源", filename)
  newVideoSource.value = "/static/media/videos/" + filename;
  formDrawerRef.value.close()
  // newPoster = "http://localhost:81/" + filename + ".png";
}

// 【更改】
const changeVideoOrder = (item) => {
  video_put(item)
    .then(res => {
      getData(subjectId)
      console.log(res)
    })
    .catch(err => {
      console.log(err)
    })
}

// 【删除】
const deleteVideoSource = (id) => {
  video_del(id)
    .then(res => {
      getData(subjectId)
      console.log(res)
    })
    .catch(err => {
      console.log(err)
    })
}

// 【上传视频】
const file = ref(null)
const newTitle = ref("")
const newOrder = ref(1)
// 上传视频按钮，增加上传填空选项
const handleAddItem = () => {
  tableData.value.push({
    title: "",
    order: 1,
    subject: subjectId,
    push: true,
  });
}
const getFile = (event) => {
  file.value = event.target.files[0];
  console.log(file);
}
const getTitle = (title) => {
  newTitle.value = title;
  console.log(title);
}
const getOrder = (order) => {
  newOrder.value = order
  console.log(order);
}
// 上传视频
const handleSubmit = () => {
  uploadFile(file.value, newTitle.value, newOrder.value, subjectId)
    .then(res => {
      console.log(res)
      // alert("视频上传成功")
    })
    .catch(err => {
      // alert("视频上传失败",err)
    })
    .finally(() => {
      formDrawerRef.value.close()
      getData(subjectId)
    })
}

// 展开位置计算
const windowHeight = window.innerHeight || document.body.clientHeight
const h = windowHeight - 64 - 44 - 40


</script>
<style>
.image-header {
  border-bottom: 1px solid #eeeeee;
  @apply flex items-center;
}
</style>