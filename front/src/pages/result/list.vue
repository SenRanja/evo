<template>
    <el-card shadow="never" class="border-0">
      <!-- 新增|刷新 -->
      <!-- <div class="flex items-center justify-between mb-4">
        <el-button type="primary" size="small" @click="handleCreate">新增</el-button>
        <el-tooltip effect="dark" content="刷新数据" placement="top">
          <el-button text @click="getData">
            <el-icon :size="20">
              <Refresh />
            </el-icon>
          </el-button>
        </el-tooltip>
      </div> -->

          <!-- 搜索 -->
    <el-form :model="searchForm" label-width="80px" class="mb-3" size="small">
      <el-row :gutter="20">
        <el-col :span="8" :offset="0">
          <el-form-item label="搜索关键词">
            <el-input v-model="searchForm.search" placeholder="考试名|姓名|学号" clearable></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="8" :offset="8">
          <div class="flex items-center justify-end">
            <el-button type="primary" @click="getData">搜索</el-button>
            <el-button @click="resetSearchForm">重置</el-button>
          </div>
        </el-col>
      </el-row>
    </el-form>
  
      <el-table :data="tableData" stripe style="width: 100%" v-loading="loading">
        
        <el-table-column prop="exam_manage" label="考试" width="200" />
        <el-table-column prop="stu_id" label="学号" width="150" />
        <el-table-column prop="name" label="姓名" width="100" />
        <el-table-column prop="objective_score" label="客观" width="100" />
        <el-table-column prop="subjective_score" label="主观" width="100" />
        <el-table-column prop="score" label="总分" width="100" />
  
        <el-table-column label="操作" width="180" align="center" v-if="user_role == 'admin'">
          <template #default="scope">
            <el-button type="primary" size="small" text @click="handleEdit(scope.row)">修改</el-button>
  
            <!-- <el-popconfirm title="是否要删除该成绩？" confirmButtonText="确认" cancelButtonText="取消" @confirm="handleDelete(scope.row.id)">
                  <template #reference>
                      <el-button text type="primary" size="small">删除</el-button>
                  </template>
              </el-popconfirm> -->
          </template>
        </el-table-column>
  
      </el-table>
  
      
      <div class="flex items-center justify-center mt-5">
          <el-pagination background layout="prev, pager ,next" :total="total" :current-page="currentPage" :page-size="limit"
            @current-change="getData" />
        </div>
    
  
      <FormDrawer ref="formDrawerRef" :title="drawerTitle" @submit="handleSubmit">
        <el-form :model="form" ref="formRef" label-width="80px" :inline="false">
          <!-- <el-form-item label="姓名" prop="name">
            <el-input v-model="form.name"></el-input>
          </el-form-item>
          <el-form-item label="学号" prop="stu_id">
            <el-input v-model="form.stu_id"></el-input>
          </el-form-item> -->
          <el-form-item label="客观分" prop="objective_score">
            <el-input v-model="form.objective_score"></el-input>
          </el-form-item>
          <el-form-item label="主观分" prop="subjective_score">
            <el-input v-model="form.subjective_score"></el-input>
          </el-form-item>
          <el-form-item label="总分" prop="score">
            <el-input v-model="form.score" ></el-input>
          </el-form-item>
          <!-- <el-form-item label="用户id" prop="user">
            <el-input v-model="form.user" ></el-input>
          </el-form-item>
          <el-form-item label="考试id" prop="exam_manage">
            <el-input v-model="form.exam_manage"></el-input>
          </el-form-item> -->
        </el-form>
      </FormDrawer>
  
    </el-card>
  </template>
  <script setup>
  import { ref,reactive,computed } from "vue"
  import FormDrawer from "~/components/FormDrawer.vue";
  import {
    getNoticeList,
    createNotice,
    updateNotice,
    deleteNotice
  } from "~/api/result"
  import {
    toast
  } from "~/composables/util"
  import {useStore} from 'vuex'
  

  const store = useStore()
  const user_role = store.state.user.role

  const tableData = ref([])
  const loading = ref(false)

// 搜索
const searchForm = reactive({
  search: "" 
})
const resetSearchForm = () => {
  searchForm.search = ""
  getData()
}
  
  // 分页
  const currentPage = ref(1)
  const total = ref(0)
  const limit = ref(30)
  
  // 获取数据
  function getData(p = null){
    if (typeof p == "number") {
        currentPage.value = p
      }
  
    loading.value = true
    getNoticeList(currentPage.value, searchForm)
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
    // name:null,
    // stu_id:null,
    objective_score:null,
    subjective_score:null,
    score:null,
    // sub_block:null,
    // user:null,
    // exam_manage:null,
  })
  const rules = {
    title:[{
        required: true,
        message: '不能为空',
        trigger: 'blur'
    }],
    description:[{
        required: true,
        message: '不能为空',
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
      description:""
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