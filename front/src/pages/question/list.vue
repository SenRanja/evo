<template>
    <el-card shadow="never" class="border-0">
      <!-- 搜索 -->
      <el-form :model="searchForm" label-width="80px" class="mb-3" size="small">
        <el-row :gutter="20">
          <el-col :span="8" :offset="0">
            <el-form-item label="搜索关键词" width="200">
              <el-input v-model="searchForm.search" placeholder="" clearable></el-input>
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
  
  
      <!-- 新增|刷新 -->
      <div class="flex items-center justify-between mb-4">
        <el-button type="primary" size="small" @click="handleCreate">新增</el-button>
        <el-tooltip effect="dark" content="刷新数据" placement="top">
          <el-button text @click="getData">
            <el-icon :size="20">
              <Refresh />
            </el-icon>
          </el-button>
        </el-tooltip>
      </div>
  
      <el-table :data="tableData" stripe style="width: 100%" v-loading="loading">
  
        <!-- <el-table-column label="id" align="center" width="60">
          <template #default="{ row }">
            {{ row.id }}
          </template>
        </el-table-column> -->
        
        <el-table-column label="类型" align="center" width="60">
          <template #default="{ row }">
            {{ row.question_type }}
          </template>
        </el-table-column>
  
        <!-- <el-table-column label="答案" width="80">
          <template #default="{ row }">
            {{ row.reference_answer }}
          </template>
        </el-table-column> -->
  
  
  
        <el-table-column label="题类" align="center" width="120">
          <template #default="{ row }">
            {{ row.question_name }}
          </template>
        </el-table-column>
  
        <el-table-column label="题目" align="center" width="200">
          <template #default="{ row }">
            {{ row.question_text }}
          </template>
        </el-table-column>
  
  
        <el-table-column label="选项" align="center" width="200">
          <template #default="{ row }">
            {{ row.choice_text }}
          </template>
        </el-table-column>
  
  
        <el-table-column label="难度" align="center" width="80">
          <template #default="{ row }">
            {{ row.difficulty_level }}
          </template>
        </el-table-column>

        
        <el-table-column label="描述" align="center" width="200">
          <template #default="{ row }">
            {{ row.description }}
          </template>
        </el-table-column>

        
        <el-table-column label="题库" align="center" width="150">
          <template #default="{ row }">
            {{ row.question_database }}
          </template>
        </el-table-column>

        
        <!-- <el-table-column label="作者" align="center" width="110">
          <template #default="{ row }">
            {{ row.author }}
          </template>
        </el-table-column> -->

        
        <!-- <el-table-column label="学科" align="center" width="110">
          <template #default="{ row }">
            {{ row.subject }}
          </template>
        </el-table-column> -->
  
        <!-- <el-table-column label="状态" width="120">
          <template #default="{ row }">
            <el-switch :modelValue="row.status" :active-value="1" :inactive-value="0" :loading="row.statusLoading" :disabled="row.super == 1"  @change="handleStatusChange($event,row)">
            </el-switch>
          </template>
        </el-table-column> -->
  
        <el-table-column label="操作" width="180" align="center">
          <template #default="scope">
  
            <small v-if="scope.row.super == 1" class="text-sm text-gray-500">暂无操作</small>
            <div v-else>
              <el-button type="primary" size="small" text @click="handleEdit(scope.row)">修改</el-button>
  
              <el-popconfirm title="是否要删除该题目？" confirmButtonText="确认" cancelButtonText="取消"
                @confirm="handleDelete(scope.row.id)">
                <template #reference>
                  <el-button text type="primary" size="small">删除</el-button>
                </template>
              </el-popconfirm>
            </div>
  
          </template>
        </el-table-column>
  
      </el-table>
  
      <div class="flex items-center justify-center mt-5">
        <el-pagination background layout="prev, pager ,next" :total="total" :current-page="currentPage" :page-size="limit"
          @current-change="getData" />
      </div>
  
  
      <FormDrawer ref="formDrawerRef" :title="drawerTitle" @submit="handleSubmit">
        <el-form :model="form" ref="formRef" :rules="rules" label-width="80px" :inline="false">
          <el-form-item label="题目类型" prop="question_type">
            <el-select v-model="form.question_type" placeholder="题目类型">
              <el-option v-for="item in question_types" :key="item" :label="item" :value="item">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="答案" prop="reference_answer">
            <el-input v-model="form.reference_answer"></el-input>
          </el-form-item>
          <el-form-item label="题类" prop="question_name">
            <el-input v-model="form.question_name" placeholder="题类"></el-input>
          </el-form-item>
          <el-form-item label="题目" prop="question_text">
            <el-input v-model="form.question_text"></el-input>
          </el-form-item>
          <el-form-item label="选项" prop="choice_text">
            <el-input v-model="form.choice_text" placeholder="答案依据ABCD顺序|分隔如 日本|澳大利亚|法国|韩国"></el-input>
          </el-form-item>
          <el-form-item label="图片" prop="question_image_data">
            <el-input v-model="form.question_image_data" placeholder="null"></el-input>
          </el-form-item>
          <el-form-item label="难易" prop="difficulty_level">
            <el-select v-model="form.difficulty_level" placeholder="难易">
              <el-option v-for="item in difficulty_levels" :key="item" :label="item" :value="item">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="描述" prop="description">
            <el-input v-model="form.description"></el-input>
          </el-form-item>
          <el-form-item label="题库" prop="question_database">
            <el-input v-model="form.question_database"></el-input>
          </el-form-item>
          <el-form-item label="作者" prop="author">
            <el-input v-model="form.author"></el-input>
          </el-form-item>
  

  
          <!-- <el-form-item label="状态" prop="content">
            <el-switch v-model="form.status" :active-value="1" :inactive-value="0">
            </el-switch>
          </el-form-item> -->
        </el-form>
      </FormDrawer>
  
    </el-card>
  </template>
  <script setup>
  import { ref, reactive, computed } from "vue"
  import FormDrawer from "~/components/FormDrawer.vue";
  import {
    getUserList,
    // updateUserStatus,
    createUser,
    updateUser,
    deleteUser
  } from "~/api/question"
  
  import {
    toast
  } from "~/composables/util"
  
  const searchForm = reactive({
    search: ""
  })
  const resetSearchForm = () => {
    searchForm.search = ""
    getData()
  }
  
  const difficulty_levels = ref([])
  const question_types = ref([])
  question_types.value = ['单选', '多选', '判断', '填空', '简答', '论述']

  const tableData = ref([])
  const loading = ref(false)
  
  // 分页
  const currentPage = ref(1)
  const total = ref(0)
  const limit = ref(30)
  
  // 获取数据
  function getData(p = null) {
    if (typeof p == "number") {
      currentPage.value = p
    }
  
    loading.value = true
    // getUserList(currentPage.value,searchForm)
    getUserList(currentPage.value, searchForm)
      .then(res => {
        tableData.value = res.results
        total.value = res.count
        difficulty_levels.value = ['easy', 'middle', 'hard',]
      })
      .finally(() => {
        loading.value = false
      })
  }
  
  getData()
  
  // 删除
  const handleDelete = (id) => {
    loading.value = true
    deleteUser(id).then(res => {
      toast("删除成功")
      getData()
    })
      .finally(() => {
        loading.value = false
      })
  }
  
  // 表单部分
  const formDrawerRef = ref(null)
  const formRef = ref(null)
  const form = reactive({
    id: "",
    question_type: "",
    reference_answer: "",
    question_name: null,
    question_text: 1,
    choice_text: "",
    question_image_data: "",
    difficulty_level: "",
    description: "",
    question_database: "",
    author: ""
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
  
  // 修改状态
  const handleStatusChange = (status, row) => {
    row.statusLoading = true
    updateUserStatus(row.id, status)
      .then(res => {
        toast("修改状态成功")
        row.status = status
      })
      .finally(() => {
        row.statusLoading = false
      })
  }
  
  </script>