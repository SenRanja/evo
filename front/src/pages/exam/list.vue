<template>
    <el-card shadow="never" class="border-0">
        <!-- 搜索 -->
        <el-form :model="searchForm" label-width="80px" class="mb-3" size="small">
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

            <el-table-column label="结束时间" align="center" width="200">
                <template #default="{ row }">
                    {{ row.end_time }}
                </template>
            </el-table-column>

            <el-table-column label="时长" align="center" width="80">
                <template #default="{ row }">
                    {{ row.duration }}
                </template>
            </el-table-column>

            <el-table-column label="总分" align="center" width="150">
                <template #default="{ row }">
                    {{ row.max_score }}
                </template>
            </el-table-column>



            <el-table-column label="是否归档" align="center" width="150">
                <template #default="{ row }">
                    {{ row.is_archived }}
                </template>
            </el-table-column>

            <el-table-column label="操作" width="200" align="center">
                <template #default="scope">

                    <small v-if="scope.row.super == 1" class="text-sm text-gray-500">暂无操作</small>
                    <div v-else>
                        <el-button type="primary" size="small" text @click="handleEdit(scope.row)">修改</el-button>

                        <el-button type="primary" size="small" text @click="handleEdit2(scope.row)">设题</el-button>

                        <el-popconfirm title="是否要删除该考试？" confirmButtonText="确认" cancelButtonText="取消"
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
            <el-pagination background layout="prev, pager ,next" :total="total" :current-page="currentPage"
                :page-size="limit" @current-change="getData" />
        </div>


        <FormDrawer ref="formDrawerRef" :title="drawerTitle" @submit="handleSubmit">
            <el-form :model="form" ref="formRef" label-width="80px" :inline="false">

                <el-form-item label="考试名称" prop="exam_name">
                    <el-input v-model="form.exam_name"></el-input>
                </el-form-item>

                <el-form-item label="考试类型" prop="exam_type">
                    <el-select v-model="form.exam_type">
                        <el-option v-for="item in roles" :key="item" :label="item" :value="item">
                        </el-option>
                    </el-select>
                </el-form-item>


                <!-- <el-form-item label="开始时间" prop="start_time">
                    <el-input v-model="form.start_time" placeholder="如 2022-04-01 10:30:00"></el-input>
                </el-form-item>
                <el-form-item label="结束时间" prop="end_time">
                    <el-input v-model="form.end_time" placeholder="如 2022-04-01 13:30:00"></el-input>
                </el-form-item> -->



                <el-form-item label="开始时间" prop="start_time">
                    <div class="block">
                    <el-date-picker
                        v-model="form.start_time"
                        type="datetime"
                        placeholder="Pick a Date"
                        format="YYYY-MM-DD HH:mm:ss"
                        date-format="MMM DD, YYYY"
                        time-format="HH:mm"
                        :picker-options="pickerOptions"
                    />
                    </div>
                </el-form-item>
                <el-form-item label="结束时间" prop="end_time">
                    <div class="block">
                    <el-date-picker
                        v-model="form.end_time"
                        type="datetime"
                        placeholder="Pick a Date"
                        format="YYYY-MM-DD HH:mm:ss"
                        date-format="MMM DD, YYYY"
                        time-format="HH:mm"
                        :picker-options="pickerOptions"
                    />
                    </div>
                </el-form-item>



                <el-form-item label="持续时间" prop="duration">
                    <div>{{ form.duration }} 分钟</div>
                </el-form-item>

                <el-form-item label="创建时间" prop="creation_time">
                    <div>{{ form.creation_time }}</div>
                </el-form-item>

                <el-form-item label="更改时间" prop="last_modified_time">
                    <div>{{ form.last_modified_time }}</div>
                </el-form-item>

                <el-form-item label="分值" prop="max_score">
                    <div>{{ form.max_score }}</div>
                </el-form-item>

                <el-form-item label="参考班级" prop="class_groups" v-if="drawerTitle ==='修改'">
                    <el-select v-model="form.class_groups" multiple>
                        <el-option v-for="item in form.class_groups" :key="item" :label="item" :value="item">
                        </el-option>
                    </el-select>
                </el-form-item>

                <el-form-item label="修改班级" align="center" width="200" v-if="drawerTitle ==='修改'">
                    <!-- <div>{{ form.class_groups }}</div> -->
                    <el-input v-model="form.class_groups" placeholder=""></el-input>
                </el-form-item>

                <el-form-item label="归档" v-if="drawerTitle ==='修改'">
                    <el-switch v-model="form.is_archived" :active-value="true" :inactive-value="false">
                    </el-switch>
                </el-form-item>

                <el-form-item label="多选半分">
                    <el-switch v-model="form.multiple_half" :active-value="true" :inactive-value="false">
                    </el-switch>
                </el-form-item>

            </el-form>

        </FormDrawer>

        <FormDrawer ref="formDrawerRef2" :title="drawerTitle" @submit="handleSubmit2">
            <template v-for="(item, index) in tableData2" :key="index">
                <!-- 注释 multiple ，是单选而非多选。 此处el-select的index和 上一行的v-for的index不是一个东西，index是vue默认的循环关键字，不需要当成普通的变量标识符看待 -->
                题库
                <el-select v-model="item.question_database">
                    <el-option v-for="item in classes" :key="item" :label="item" :value="item">
                    </el-option>
                </el-select>
                <!-- <br> -->
                题型
                <el-select v-model="item.question_type">
                    <el-option v-for="item in question_types" :key="item" :label="item" :value="item">
                    </el-option>
                </el-select>
                <br>
                难度
                <el-select v-model="item.difficulty_level">
                    <el-option v-for="item in difficulty_levels" :key="item" :label="item" :value="item">
                    </el-option>
                </el-select>
                <!-- <br> -->
                数量
                <el-input v-model="item.question_num" style="width: 90px">
                </el-input>
                <!-- <br> -->
                分值
                <el-input v-model="item.single_question_score" style="width: 90px">
                </el-input>
                <!-- <br> -->
                <el-button class="el-icon-delete" type="danger" @click="handleRemove(item.question_database)">删除</el-button>
                <br>

            </template>
            <el-button type="text" @click="handleAddItem">添加选项</el-button>

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
    getExamQuestion,
    getExamQuestionList,
    updateExamQuestion
} from "~/api/exam"

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

// 时间选择器
const pickerOptions = {
        firstDayOfWeek: 1, // 设置周的第一天为周一
        shortcuts: [ // 添加快捷选项
          {
            text: '中国时区',
            onClick(picker) {
              const now = new Date();
              const year = now.getFullYear();
              const month = now.getMonth();
              const day = now.getDate();
              const hour = now.getHours();
              const minute = now.getMinutes();
              const second = now.getSeconds();
              picker.$emit('pick', new Date(year, month, day, hour, minute, second)); // 发送事件来设置选择器的值
            }
          }
        ]
      }

const roles = ref([])
roles.value = ["模拟", "考试"]

const difficulty_levels = ref([])
difficulty_levels.value = ['easy', 'middle', 'hard',]

const question_types = ref([])
question_types.value = ['单选', '多选', '判断', '填空', '简答', '论述']

const classes = ref([])
getExamQuestionList()
    .then(res => {
        classes.value = res.data
    })

const tableData = ref([])
const tableData2 = ref([])
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

// 获取数据
function getEQDBData(id) {

    loading.value = true
    getExamQuestion(id)
        .then(res => {
            tableData2.value = res.data
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
const formDrawerRef2 = ref(null)

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
    multiple_half: false,
})
const form2 = reactive({
    id: "",
    exam_name: "",
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

const handleSubmit2 = () => {
    formDrawerRef2.value.showLoading()

    const fun = editId.value
    updateExamQuestion(fun, tableData2.value)
        .then(res => {
            toast(drawerTitle.value + "成功")
            // 修改刷新当前页，新增刷新第一页
            getEQDBData(editId.value)
            formDrawerRef2.value.close()
            getData()
            formDrawerRef2.value.hideLoading()
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

// 新增
const handleCreate2 = () => {
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

// 编辑
const handleEdit2 = (row) => {
    editId.value = row.id
    getEQDBData(editId.value)
    // resetForm(row)
    formDrawerRef2.value.open()
}

// Drawer2 的 添加、删除
const handleAddItem = () => {
    tableData2.value.push({
        question_database: "",
        content: "",
    });
    // console.log(tableData2.value);
}


const handleRemove = (key) => {
    // 删除选项
    tableData2.value = tableData2.value.filter((item) => item.question_database !== key);
    // // 如果删除的是正确答案，清空正确答案
    // if (this.form.correctAnswer === key) {
    //     this.form.correctAnswer = "";
    // }

    // console.log(tableData2.value);
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

<style scoped>
.demo-datetime-picker {
    display: flex;
    width: 100%;
    padding: 0;
    flex-wrap: wrap;
    justify-content: space-around;
    align-items: stretch;
}

.demo-datetime-picker .block {
    padding: 30px 0;
    text-align: center;
}

.line {
    width: 1px;
    background-color: var(--el-border-color);
}
</style>