<template>
     <a href="/static/media/template/试题模板.xlsx" download style="color: blue;">下载模板文件</a>
    <form>
        <input type="file" @change="getFile($event)">
        <button @click.prevent="submitForm">提交</button>
    </form>
</template>
  
<script>
import { ElMessage, ElMessageBox } from 'element-plus'
import { uploadFile } from "~/api/question"

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
            uploadFile(this.file)
                .then(response => {
                    if (response.status === 200) {
                        console.log(response.data);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            ElMessage({
                type: 'success',
                message: '上传成功，正在处理，请等待几分钟',
            })
        }
    }
};
</script>
  