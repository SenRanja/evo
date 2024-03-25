<template>
    <a href="/static/media/template/用户模板.xlsx" download style="color: blue;">下载模板文件</a>
    <form>
        <input type="file" @change="getFile($event)"></input>
        <el-button @click.prevent="submitForm">提交</el-button>
    </form>
</template>
  
<script>
import { uploadFile } from "~/api/user"
import { ElMessage, ElMessageBox } from 'element-plus'

export default {
    data() {
        return {
            file: null
        };
    },
    methods: {
        getFile(event) {
            this.file = event.target.files[0];
            console.log(this.file);
        },
        submitForm() {
            // let formData = new FormData();
            // formData.append('excel_file', this.file);

            uploadFile(this.file)
                .then(response => {
                    if (response.status === 200) {
                        console.log(response.data);

                        ElMessage({
                            type: 'success',
                            message: '用户文件导入处理成功',
                        })

                    }
                })
                .catch(error => {
                    console.error('Error:', error);

                    ElMessage({
                        type: 'error',
                        message: error,
                    })

                });
            ElMessage({
                        type: 'success',
                        message: '上传成功，正在处理，请等待几分钟',
                    })
        }
    }
};
</script>
  