<template>
    <el-card shadow="never" class="border-0">
        <!-- 新增|刷新 -->
        <div class="flex items-center justify-between mb-4">
            <el-button type="primary" size="small" @click="handleCreate"
                v-if="user_role === 'admin'">新增</el-button>
            <el-tooltip effect="dark" content="刷新数据" placement="top">
                <el-button text @click="getData">
                    <el-icon :size="20">
                        <Refresh />
                    </el-icon>
                </el-button>
            </el-tooltip>
        </div>

        <el-table :data="tableData" stripe style="width: 100%" v-loading="loading">

            <el-table-column prop="subject" label="学科" width="150" />
            <el-table-column prop="description" label="描述" width="550" />

            <el-table-column label="操作" width="380" align="center">
                <template #default="scope">

                    <el-button type="primary" size="small" text @click="handleVideo(scope.row)">视频学习</el-button>
                    <el-button type="primary" size="small" text @click="handleDownload(scope.row)">资料下载</el-button>

                    <el-button type="primary" size="small" text @click="handleEdit(scope.row)" v-if="user_role === 'admin'">修改</el-button>

                    <el-popconfirm title="是否要删除该学科条目？" confirmButtonText="确认" cancelButtonText="取消"
                        @confirm="handleDelete(scope.row.id)" v-if="user_role === 'admin'">
                        <template #reference>
                            <el-button text type="primary" size="small">删除</el-button>
                        </template>
                    </el-popconfirm>

                </template>
            </el-table-column>

        </el-table>


        <div class="flex items-center justify-center mt-5">
            <el-pagination background layout="prev, pager ,next" :total="total" :current-page="currentPage"
                :page-size="limit" @current-change="getData" />
        </div>



        <FormDrawer ref="formDrawerRef" :title="drawerTitle" @submit="handleSubmit('create')">
            <el-form :model="form" ref="formRef" label-width="80px" :inline="false">
                <el-form-item label="学科名" prop="subject">
                    <el-input v-model="form.subject"></el-input>
                </el-form-item>
                <el-form-item label="描述" prop="description">
                    <el-input v-model="form.description" type="textarea" :rows="5"></el-input>
                </el-form-item>

            </el-form>
        </FormDrawer>

        <FormDrawer ref="formDrawerRef2" :title="drawerTitle" @submit="handleSubmit('download')">
            <template v-for="(item, index) in tableData2" :key="index">
                <!-- <el-input v-model="item.filename" style="width: 600px" disabled>
            </el-input> -->
                <el-card style="width: 500px;">
                    <span>{{ item.filename }}</span>
                </el-card>
                <el-button @click="downloadFile(item.filename)">下载</el-button>
                <el-button @click="deleteFile(item.id)" v-if="user_role === 'admin' || user_role === 'tea'">删除</el-button>
            </template>
            <hr><br>
            <div v-if="user_role === 'admin' || user_role === 'tea'">
                <input type="file" @change="getFile($event)" />
                <el-button @click="uploadFile()">上传</el-button>
            </div>
        </FormDrawer>

        <FormDrawer ref="formDrawerRef3" :title="drawerTitle" @submit="handleSubmit('update')">
            <!-- <template v-for="(item, index) in form" :key="index">
                <el-card style="width: 500px;">
                    <span>{{ item.filename }}</span>
                </el-card>
                <el-button @click="downloadFile(item.filename)">下载</el-button>
            </template> -->
            <el-form :model="form" ref="formRef" label-width="80px" :inline="false">
                <el-form-item label="学科名" prop="subject">
                    <el-input v-model="form.subject"></el-input>
                </el-form-item>
                <el-form-item label="描述" prop="description">
                    <el-input v-model="form.description"></el-input>
                </el-form-item>
                <el-form-item label="班级可见" prop="groups" v-if="drawerTitle === '修改'">
                    <el-select v-model="form.groups" multiple>
                        <el-option v-for="item in form.groups" :key="item" :label="item" :value="item">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="班级可见" width="200" prop="groups"  v-if="drawerTitle === '修改'">
                    <el-input v-model="form.groups" placeholder=""></el-input>
                </el-form-item>
            </el-form>
        </FormDrawer>

    </el-card>
</template>
<script setup>
import { getFtpDataBySid } from "~/api/subject";
import { deleteFtpDataBySid } from "~/api/subject";
import {
    getNoticeList, createNotice, updateNotice, deleteNotice, uploadFtpDocBySid,
    getSubjectWithGroupList,
} from "~/api/subject";
import { ref, reactive, computed, watch } from "vue"
import FormDrawer from "~/components/FormDrawer.vue";
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';
import {
    toast
} from "~/composables/util";
import { ElMessage, ElMessageBox } from 'element-plus'

const store = useStore()
const user_role = store.state.user.role
const loading = ref(false)
const router = useRouter()


// 监听路由跳转，如果是从 考试页面 跳转到本页，则重新渲染VUE，防止考试页面重复渲染破坏功能
watch(
    () => router.currentRoute.value,
    (to, from) => {
        //当路由变化时，执行数据获取
        if (from.path === "/video_study/list") {
            console.log("from.path === '/video_study/list'")
            location.reload();
        }
    },
    { immediate: false, deep: true }
);


// 分页
const currentPage = ref(1)
const total = ref(0)
const limit = ref(30)

//   【学科部分】
const tableData = ref([])

// 获取数据
function getData(p = null) {
    if (typeof p == "number") {
        currentPage.value = p
    }

    loading.value = true
    if (user_role == 'admin') {
        getSubjectWithGroupList()
            .then(res => {
                tableData.value = res.msg.data
            })
            .finally(() => {
                loading.value = false
            })
    }else{
        getNoticeList(currentPage.value)
            .then(res => {
                tableData.value = res.results
                total.value = res.count
            })
            .finally(() => {
                loading.value = false
            })
    }
}

getData()

// 学科的表单部分
const formDrawerRef = ref(null)
const formRef = ref(null)
const form = reactive({
    id: "",
    subject: "",
    description: 0,
    groups: [],
})

// editId，用来确认是修改还是新增，0是新增，其他是修改
// drawerTitle同理
const editId = ref(0)
const drawerTitle = ref(0)

// 提交表单，此处设计 新增、修改
const handleSubmit = (method) => {
    formDrawerRef.value.showLoading()
    if (method == "create") {
        createNotice(form)
            .then(res => {
                toast(drawerTitle.value + "成功")
                // 修改刷新当前页，新增刷新第一页
                getData()
                formDrawerRef.value.close()
            })
            .finally(() => {
                formDrawerRef.value.hideLoading()
            })
    }
    if (method == "update") {
        console.log(form)
        updateNotice(editId.value, form)
            .then(res => {
                toast(drawerTitle.value + "成功")
                // 修改刷新当前页，新增刷新第一页
                getData()
                formDrawerRef.value.close()
            })
            .finally(() => {
                formDrawerRef.value.hideLoading()
            })
    }
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

//   【下载文件部分】
const file = ref(null)
const subject_id_ref = ref(0)
//  下载
const getFtpData = (id) => {
    loading.value = true
    getFtpDataBySid(id)
        .then(res => {
            tableData2.value = res.data
        })
        .finally(() => {
            loading.value = false
        })
}

const handleDownload = (row) => {
    drawerTitle.value = "资料下载"

    editId.value = row.id
    console.log(editId.value)
    // 获取数据
    getFtpData(editId.value)
    // resetForm(row)
    formDrawerRef2.value.open()
}

const tableData2 = ref([])
const formDrawerRef2 = ref(null)

// 下载文档文件
function downloadFile(filename) {
    const downloadLink = `/static/media/documents/${filename}`;
    const link = document.createElement('a');
    link.href = downloadLink;
    // 设置下载属性，确保浏览器在点击时下载文件
    link.setAttribute('download', filename);
    // 将链接元素插入到文档中
    document.body.appendChild(link);
    // 模拟点击链接
    link.click();
    // 清理临时链接元素
    document.body.removeChild(link);
}

// 删除文档文件
function deleteFile(id) {
    deleteFtpDataBySid(id)
        .then(() => {
            toast("删除成功");
            getFtpData(editId.value)
        })
        .catch(() => {
            toast("删除失败");
            getFtpData(editId.value)
        })
}

// 上传文档文件
const getFile = (event) => {
    file.value = event.target.files[0]
    subject_id_ref.value = editId.value
}
function uploadFile() {
    uploadFtpDocBySid(subject_id_ref.value, file.value)
        .then(() => {
            toast("上传成功");
            getFtpData(editId.value)
        })
        .catch(() => {
            toast("上传失败");
            getFtpData(editId.value)
        })
}

// ======================================================================
// 上传视频、上传资料、改学科名
// formDrawerRef3

const tableData3 = ref([])
const formDrawerRef3 = ref(null)


// ======================================================================
// 删除
const handleDelete = (id) => {
    loading.value = true
    deleteNotice(id)
        .then(res => {
            toast("删除成功")
            getData()
        })
        .finally(() => {
            loading.value = false
        })
}


// 新增
const handleCreate = () => {
    editId.value = 0
    resetForm({
        subject: "",
        description: "",
    })
    formDrawerRef.value.open()
}

// 编辑
const handleEdit = (row) => {
    drawerTitle.value = "修改"
    editId.value = row.id
    resetForm(row)
    formDrawerRef3.value.open()
}

//   视频学习
const handleVideo = (row) => {
    editId.value = row.id
    router.push({ name: "/video_study/list", query: { subjectId: editId.value } });
}


</script>