<template>
  <div v-if="user_role == 'stu'">
    提示：如果操作处没有“进入”字样，点击浏览器“刷新”按钮或按下“F5”。
  </div>
  <!-- <div v-if="user_role == 'admin'">管理员用户移步<strong>考试管理</strong>菜单</div> -->
  <el-card shadow="never" class="border-0">
    <!-- 搜索 -->
    <!-- <el-form :model="searchForm" label-width="80px" class="mb-3" size="small">
      <el-row :gutter="20">
        <el-col :span="8" :offset="0">
          <el-form-item label="搜索关键词" width="200">
            <el-input v-model="searchForm.search" placeholder="时间、名称" clearable></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="8" :offset="8">
          <div class="flex items-center justify-end">
            <el-button type="primary" @click="getData">搜索</el-button>
            <el-button @click="resetSearchForm">重置</el-button>
          </div>
        </el-col>
      </el-row>
    </el-form> -->


    <!-- 新增|刷新 -->
    <div class="flex items-center justify-between mb-4">
      <!-- <el-button type="primary" size="small" @click="handleCreate">新增</el-button> -->
      <el-tooltip effect="dark" content="刷新数据" placement="top">
        <el-button text @click="getData">
          <el-icon :size="20">
            <Refresh />
          </el-icon>
        </el-button>
      </el-tooltip>
    </div>

    <el-table :data="tableData" stripe style="width: 100%" v-loading="loading">

      <el-table-column label="考试名称" align="center" width="200">
        <template #default="{ row }">
          {{ row.exam_name }}
        </template>
      </el-table-column>


      <el-table-column label="类型" align="center" width="120">
        <template #default="{ row }">
          {{ row.exam_type }}
        </template>
      </el-table-column>

      <el-table-column label="开始时间" align="center" width="200">
        <template #default="{ row }">
          {{ row.start_time }}
        </template>
      </el-table-column>

      <el-table-column label="考试分钟数" align="center" width="100">
        <template #default="{ row }">
          {{ row.duration }}
        </template>
      </el-table-column>

      <el-table-column label="总分" align="center" width="150">
        <template #default="{ row }">
          {{ row.max_score }}
        </template>
      </el-table-column>


      <el-table-column label="操作" width="250" align="center">
        <template #default="scope" v-if="store.state.user.role === 'stu'">
          <div>
            <el-popconfirm title="是否要进入该考试？" confirmButtonText="确认" cancelButtonText="取消"
              @confirm="enterExamById(scope.row.id)">
              <template #reference>
                <el-button text type="primary" size="small">进入</el-button>
              </template>
            </el-popconfirm>
          </div>
        </template>

        <template #default="scope" v-if="store.state.user.role === 'tea'">
          <el-popconfirm title="下载word试卷" confirmButtonText="确认" cancelButtonText="取消"
            @confirm="downloadFile(scope.row.id)">
            <template #reference>
              <el-button text type="primary" size="small">预览</el-button>
            </template>
          </el-popconfirm>

          <el-popconfirm title="是否对该考试主观题判分？" confirmButtonText="确认" cancelButtonText="取消"
            @confirm="judgeSubExamById(scope.row.id)">
            <template #reference>
              <el-button text type="primary" size="small">判分</el-button>
            </template>
          </el-popconfirm>
        </template>

      </el-table-column>

    </el-table>

    <div class="flex items-center justify-center mt-5">
      <el-pagination background layout="prev, pager ,next" :total="total" :current-page="currentPage" :page-size="limit"
        @current-change="getData" />
    </div>
  </el-card>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { useStore } from 'vuex'
import { ref, reactive, computed, watch } from "vue"
import FormDrawer from "~/components/FormDrawer.vue";
import {
  getStuExamList,
  // updateUserStatus,
  createUser,
  updateUser,
  deleteUser,
  getExamQuestion,
  getExamPaperOfWord
} from "~/api/exam"
import { toast } from "~/composables/util"

const router = useRouter()
const store = useStore()
const user_role = store.state.user.role
console.log(user_role)
// if (user_role == "admin"){
//   router.push({name:"examing"});
// }

// 监听路由跳转，如果是从 考试页面 跳转到本页，则重新渲染VUE，防止考试页面重复渲染破坏功能
watch(
  () => router.currentRoute.value,
  (to, from) => {
    //当路由变化时，执行数据获取
    if (from.path === '/exam_questions/examing') {
      console.log("from.path === '/exam_questions/examing'")
      location.reload();
    }
  },
  { immediate: false, deep: true }
);


store.dispatch("getSystemSetting")
        .then((res) => {
            // console.log(store.state.settings)
        }).finally((err) => {
          // console.log(err)
        })

// 考试状态返回中文
function getChineseStatus(status) {
  switch (status) {
    case "doing":
      return "进行中";
    case "to do":
      return "未开始";
    case "done":
      return "结束";
    default:
      return status;
  }
}

const searchForm = reactive({
  search: ""
})
const resetSearchForm = () => {
  searchForm.search = ""
  getData()
}

const roles = ref([])
roles.value = ["模拟", "考试", "作业"]


const tableData = ref([])
const loading = ref(false)

// 分页
const currentPage = ref(1)
const total = ref(0)
const limit = ref(30)

// 获取数据
function getData() {
  loading.value = true
  getStuExamList()
    .then(res => {
      tableData.value = res.data
    })
    .finally(() => {
      loading.value = false
    })
}


getData()

// 跳转入考试
const enterExamById = (id) => {
  router.push({ name: "examing", query: { examId: id } });
}

// 老师视角 跳转入考试 判分
const judgeSubExamById = (id) => {
  router.push({ name: "judge_sub_exam", query: { examId: id } });
}

// 表单部分
const formDrawerRef = ref(null)

const formRef = ref(null)
const form = reactive({
  id: "",
  exam_name: "",
  exam_type: "",
  start_time: null,
  end_time: 1,
  duration: "",
  creation_time: "",
  last_modified_time: "",
  max_score: "",
  is_archived: "",
  class_groups: [],
})
const rules = {}
const editId = ref(0)
const drawerTitle = computed(() => editId.value ? "修改" : "新增")

const handleSubmit = () => {
  formRef.value.validate((valid) => {
    if (!valid) return

    formDrawerRef.value.showLoading()

    const fun = editId.value ? updateUser(editId.value, form) : createUser(form)

    fun.then(res => {
      toast(drawerTitle.value + "成功")
      // 修改刷新当前页，新增刷新第一页
      getData(editId.value ? false : 1)
      formDrawerRef.value.close()
    })
      .finally(() => {
        formDrawerRef.value.hideLoading()
      })

  })
}


// 重置表单
function resetForm(row = false) {
  if (formRef.value) formRef.value.clearValidate()
  if (row) {
    for (const key in form) {
      form[key] = row[key]
    }
  }
}

// 新增
const handleCreate = () => {
  editId.value = 0
  resetForm({
    password: "",
    name: "",
    stu_id: null,
    tel: "",
    id_card: "",
    email: "",
    role: "stu",
  })
  formDrawerRef.value.open()
}

// 编辑
const handleEdit = (row) => {
  editId.value = row.id
  resetForm(row)
  formDrawerRef.value.open()
}

// 下载文件
function downloadFile(id) {
    getExamPaperOfWord(id)
      .then(res => {
        const filename = res.filename;
        const downloadLink = `/static/media/documents/${filename}`;
        const link = document.createElement('a');
        link.href = downloadLink;
        // 设置下载属性，确保浏览器在点击时下载文件
        // link.setAttribute('download', filename);
        link.setAttribute('download', filename);
        // 将链接元素插入到文档中
        document.body.appendChild(link);
        // 模拟点击链接
        link.click();
        // 清理临时链接元素
        document.body.removeChild(link);
      })

}


// // 修改状态
// const handleStatusChange = (status, row) => {
//     row.statusLoading = true
//     updateUserStatus(row.id, status)
//         .then(res => {
//             toast("修改状态成功")
//             row.status = status
//         })
//         .finally(() => {
//             row.statusLoading = false
//         })
// }
</script>