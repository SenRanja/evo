<template>
    <el-card shadow="never" class="border-0">
        <!-- 搜索 -->
        <el-form :model="searchForm" label-width="80px" class="mb-3" size="small">
            <el-row :gutter="20">
                <el-col :span="8" :offset="0">
                    <el-form-item label="搜索关键词">
                        <el-input v-model="searchForm.search" placeholder="班级名" clearable></el-input>
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

            <el-table-column label="班级名称" align="center" width="300">
                <template #default="{ row }">
                    {{ row.name }}
                </template>
            </el-table-column>


            <el-table-column label="操作" width="480" align="center">
                <template #default="scope">

                    <div>
                        <el-button type="primary" size="small" text @click="handleEdit(scope.row)" v-if="user_role === 'admin'">修改</el-button>

                        <el-popconfirm title="是否要删除该用户？" confirmButtonText="确认" cancelButtonText="取消"
                            @confirm="handleDelete(scope.row.url)" v-if="user_role === 'admin'">
                            <template #reference>
                                <el-button text type="primary" size="small">删除</el-button>
                            </template>
                        </el-popconfirm>
                        <el-button type="primary" size="small" text @click="changeUser(scope.row)">操作用户</el-button>
                    </div>


                </template>
            </el-table-column>

        </el-table>

        <div class="flex items-center justify-center mt-5">
            <el-pagination background layout="prev, pager ,next" :total="total" :current-page="currentPage"
                :page-size="limit" @current-change="getData" />
        </div>


        <FormDrawer ref="formDrawerRef" :title="drawerTitle" @submit="handleSubmit">
            <el-form :model="form" ref="formRef" label-width="80px" :inline="false">
                <el-form-item label="班级名" prop="name">
                    <el-input v-model="form.name" placeholder="班级名"></el-input>
                </el-form-item>
            </el-form>
        </FormDrawer>

        <FormDrawer ref="formDrawerRefUser" :title="drawerTitle" @submit="AddNewUser">
            <el-form :model="formuser" ref="formRefUser" width="80px" :inline="false">
                <el-form-item label="班级用户" prop="groups">
                    <el-select v-model="formuser.users" multiple>
                        <el-option v-for="item in formuser.users" :key="item.stu_id" :label="item.name" :value="item">
                        </el-option>
                    </el-select>
                </el-form-item>
                <!-- <el-form-item label="班级用户" width="200" prop="groups" v-if="drawerTitle === '修改'">
                    <el-input v-model="formuser.users" placeholder=""></el-input>
                </el-form-item> -->
            </el-form>
            <el-input v-model="new_stu_input_item" style="width: 400px" placeholder="stu_id、手机号、身份证号、邮箱"></el-input>
            <el-button type="text" @click="addUserToGroup">添加新用户</el-button>

        </FormDrawer>

    </el-card>
</template>
<script setup>
import { ref, reactive, computed } from "vue"
import FormDrawer from "~/components/FormDrawer.vue";
import {
    getUserList,
    createUser,
    updateUser,
    deleteUser,

    getClassUserList,
    addNewUserToClass,deleteUserToClass
} from "~/api/class"
import { useRouter } from 'vue-router'

import {
    toast
} from "~/composables/util"
import { useStore } from 'vuex';

const router = useRouter();
const store = useStore()
const user_role = store.state.user.role

const searchForm = reactive({
    search: ""
})
const resetSearchForm = () => {
    searchForm.search = ""
    getData()
}


const tableData = ref([])
const loading = ref(false)

// 分页
const currentPage = ref(1)
const total = ref(0)
const limit = ref(30)

// 为班级添加新用户
const new_stu_input_item = ref("")

// 获取班级成员名单
const class_users = ref([])


// 获取数据
function getData(p = null) {
    if (typeof p == "number") {
        currentPage.value = p
    }

    loading.value = true
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

// 删除
const handleDelete = (url) => {
    loading.value = true
    deleteUser(url).then(res => {
        toast("删除成功")
        getData()
    })
        .finally(() => {
            loading.value = false
        })
}

// 表单部分
// 班级名修改
const formDrawerRef = ref(null)
const formRef = ref(null)
const form = reactive({
    url: "",
    name: "",
    users: [],
})


// 操作用户
const formDrawerRefUser = ref(null)
const formRefUser = ref(null)
const formuser = reactive({
    group_name: "",
    users: [],
})


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

const AddNewUser = () => {
    deleteUserToClass(editId.value, formuser.users)
        .then(res => {
            toast("班级用户更新成功")
            getClassUserList(editId.value)
                .then(res => {
                    formuser.users = res.users
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
function resetFormUser(row = false) {
    if (row) {
        for (const key in formuser) {
            formuser[key] = row[key]
        }
    }
}

// 新增
const handleCreate = () => {
    editId.value = 0
    resetForm({
        url: "",
        name: "",
        users: [],
    })
    formDrawerRef.value.open()
}

const addUserToGroup = () => {
    addNewUserToClass(editId.value, new_stu_input_item.value)
        .then(res => {
            toast("添加成功")
            getClassUserList(editId.value)
                .then(res => {
                    formuser.users = res.users
                })
        })
    formDrawerRefUser.value.close()
}


// 编辑
const handleEdit = (row) => {
    editId.value = row.url
    resetForm(row)
    formDrawerRef.value.open()
}


// 操作用户
const changeUser = (row) => {
    editId.value = row.url
    resetFormUser(row)
    formDrawerRefUser.value.open()
    getClassUserList(row.url)
        .then(res => {
            formuser.users = res.users
    })


    //   路由跳转
    // router.push({ name: "/class/manage_users", query: { examId: row.url } });
}
</script>