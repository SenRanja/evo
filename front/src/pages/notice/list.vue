<template>
  <el-card shadow="never" class="border-0">
    <!-- 新增|刷新 -->
    <div class="flex items-center justify-between mb-4">
      <el-button type="primary" size="small" @click="handleCreate" v-if="user_role === 'admin' || user_role === 'tea'">新增</el-button>
      <el-tooltip effect="dark" content="刷新数据" placement="top">
        <el-button text @click="getData">
          <el-icon :size="20">
            <Refresh />
          </el-icon>
        </el-button>
      </el-tooltip>
    </div>

    <el-table :data="tableData" stripe style="width: 100%" v-loading="loading">

      <el-table-column prop="title" label="标题" width="150" />
      <el-table-column prop="description" label="内容" width="550" />
      <el-table-column prop="creation_time" label="创建时间" width="110" />
      <el-table-column prop="last_modified_time" label="修改时间" width="110" />
      <el-table-column prop="valid_days" label="天数" width="70" />

      <el-table-column label="操作" width="180" align="center" v-if="user_role === 'admin' || user_role === 'tea'">
        <template #default="scope">
          <el-button type="primary" size="small" text @click="handleEdit(scope.row)">修改</el-button>

          <el-popconfirm title="是否要删除该公告？" confirmButtonText="确认" cancelButtonText="取消" @confirm="handleDelete(scope.row.id)">
                <template #reference>
                    <el-button text type="primary" size="small">删除</el-button>
                </template>
            </el-popconfirm>
        </template>
      </el-table-column>

    </el-table>

    
    <div class="flex items-center justify-center mt-5">
        <el-pagination background layout="prev, pager ,next" :total="total" :current-page="currentPage" :page-size="limit"
          @current-change="getData" />
      </div>
  

    <FormDrawer ref="formDrawerRef" :title="drawerTitle" @submit="handleSubmit">
      <el-form :model="form" ref="formRef" :rules="rules" label-width="80px" :inline="false">
        <el-form-item label="公告标题" prop="title">
          <el-input v-model="form.title" placeholder="公告标题"></el-input>
        </el-form-item>
        <el-form-item label="公告内容" prop="description">
          <el-input v-model="form.description" placeholder="公告内容" type="textarea" :rows="5"></el-input>
        </el-form-item>
        <el-form-item label="天数" prop="valid_days">
          <el-input v-model="form.valid_days"></el-input>
        </el-form-item>
        
      </el-form>
    </FormDrawer>

  </el-card>
</template>
<script setup>
import { ref,reactive,computed } from "vue"
import FormDrawer from "~/components/FormDrawer.vue";
import {useStore} from 'vuex'
import {
  getNoticeList,
  createNotice,
  updateNotice,
  deleteNotice
} from "~/api/notice"
import {
  toast
} from "~/composables/util"

const tableData = ref([])
const loading = ref(false)


// 分页
const currentPage = ref(1)
const total = ref(0)
const limit = ref(30)

const store = useStore()
const user_role = store.state.user.role
console.log(user_role)
const user_user = store.state.user
console.log(user_user)

// 获取数据
function getData(p = null){
  if (typeof p == "number") {
      currentPage.value = p
    }

  loading.value = true
  // getNoticeList(currentPage.value, searchForm)
  getNoticeList(currentPage.value)
  .then(res=>{
      tableData.value = res.results
      total.value = res.count
  })
  .finally(()=>{
      loading.value = false
  })
}

getData()

// 删除
const handleDelete = (id)=>{
  loading.value = true
  deleteNotice(id)
  .then(res=>{
    toast("删除成功")
    getData()
  })
  .finally(()=>{
    loading.value = false
  })
}

// 表单部分
const formDrawerRef = ref(null)
const formRef = ref(null)
const form = reactive({
  title:"",
  description:"",
  valid_days:0
})
const rules = {
  title:[{
      required: true,
      message: '公告标题不能为空',
      trigger: 'blur'
  }],
  description:[{
      required: true,
      message: '公告内容不能为空',
      trigger: 'blur'
  }]
}

// editId，用来确认是修改还是新增，0是新增，其他是修改
// drawerTitle同理
const editId = ref(0)
const drawerTitle = computed(()=>editId.value ? "修改" : "新增")

// 提交表单，此处设计 新增、修改
const handleSubmit = ()=>{
  formRef.value.validate((valid)=>{
    if(!valid) return 

    formDrawerRef.value.showLoading()

    const fun = editId.value ? updateNotice(editId.value,form) : createNotice(form)

    fun.then(res=>{
      toast( drawerTitle.value + "成功")
      // 修改刷新当前页，新增刷新第一页
      getData()
      formDrawerRef.value.close()
    })
    .finally(()=>{
      formDrawerRef.value.hideLoading()
    })

  })
}

// 重置表单
function resetForm(row = false){
  if(formRef.value) formRef.value.clearValidate()
  if(row){
    for(const key in form){
      form[key] = row[key]
    }
  }
}

// 新增
const handleCreate = ()=>{
  editId.value = 0
  resetForm({
    title:"",
    description:"",
    valid_days:"",
  })
  formDrawerRef.value.open()
}

// 编辑
const handleEdit = (row)=>{
  editId.value = row.id
  resetForm(row)
  formDrawerRef.value.open()
}

</script>