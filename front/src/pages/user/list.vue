<template>
  <el-card shadow="never" class="border-0">
    <!-- 搜索 -->
    <el-form :model="searchForm" label-width="80px" class="mb-3" size="small">
      <el-row :gutter="20">
        <el-col :span="8" :offset="0">
          <el-form-item label="搜索关键词">
            <el-input v-model="searchForm.search" placeholder="姓名|身份证号|电话|邮箱|学号" clearable></el-input>
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

      <el-table-column label="学生号" align="center" width="140">
        <template #default="{ row }">
          {{ row.stu_id }}
        </template>
      </el-table-column>

      <el-table-column label="姓名" width="80">
        <template #default="{ row }">
          {{ row.name }}
          <!-- <div class="flex items-center"> -->
          <!-- 暂时取消头像设定 -->
          <!-- <el-avatar :size="40" :src="row.avatar">
                <img
                  src="https://cube.elemecdn.com/e/fd/0fc7d20532fdaf769a25683617711png.png"
                />
              </el-avatar> -->
          <!-- <div class="ml-3">
                <h6>{{ row.name }}</h6>
              </div> -->
          <!-- </div> -->
        </template>
      </el-table-column>

      <el-table-column label="权限" align="center" width="70">
        <template #default="{ row }">
          {{ row.role }}
        </template>
      </el-table-column>


      <!-- <el-table-column label="是否管理员" align="center" width="100">
        <template #default="{ row }">
          {{ row.is_superuser }}
        </template>
      </el-table-column> -->

      <el-table-column label="班级" align="center" width="400">
        <template #default="{ row }">
          {{ row.groups }}
        </template>
      </el-table-column>


      <el-table-column label="上次登录" align="center" width="110">
        <template #default="{ row }">
          {{ row.last_login }}
        </template>
      </el-table-column>


      <el-table-column label="创建时间" align="center" width="110">
        <template #default="{ row }">
          {{ row.create_time }}
        </template>
      </el-table-column>

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

            <el-popconfirm title="是否要删除该用户？" confirmButtonText="确认" cancelButtonText="取消"
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
        <el-form-item label="学生号" prop="stu_id">
          <el-input v-model="form.stu_id" placeholder="用户名"></el-input>
        </el-form-item>
        <el-form-item label="姓名" prop="name">
          <el-input v-model="form.name"></el-input>
        </el-form-item>
        <el-form-item label="设置密码" prop="password">
          <!-- <el-input v-model="form.password" placeholder="密码"></el-input> -->
          <el-input v-model="form.password" placeholder="密码" type="password"></el-input>
        </el-form-item>
        <el-form-item label="电话" prop="tel">
          <el-input v-model="form.tel"></el-input>
        </el-form-item>
        <el-form-item label="身份证号" prop="id_card">
          <el-input v-model="form.id_card"></el-input>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email"></el-input>
        </el-form-item>

        <el-form-item label="角色" prop="role">
          <el-select v-model="form.role" placeholder="选择所属角色">
            <el-option v-for="item in roles" :key="item" :label="item" :value="item">
            </el-option>
          </el-select>
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
  deleteUser,
  getRolesList
} from "~/api/user"

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

const roles = ref([])

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
    })
    .finally(() => {
      loading.value = false
    })
}

getData()

getRolesList()
  .then(res => {
    roles.value = res.data
  })

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
  password: "",
  name: "",
  stu_id: null,
  tel: 1,
  id_card: "",
  email: "",
  role: "",
  create_time: "",
  last_login: ""
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