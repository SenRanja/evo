<template>
    <el-card shadow="never" class="border-0">
        <strong>License剩余天数：</strong><span>{{ left_days }}</span>
    </el-card>
    <br>
    <el-card shadow="never" class="border-0">
        <strong>可用性安全性告警：</strong><span>{{ license_valid_bool }}</span>
    </el-card>

    <el-card shadow="never" class="border-0">
        <strong>可用性安全性告警原因：</strong><span>{{ license_valid_reason }}</span>
    </el-card>
    <br>
    <el-form-item label="license提交" width="200">
        <el-input v-model="licenseForm" placeholder="license" clearable></el-input>
    </el-form-item>
    <el-button type="primary" @click="submit">提交</el-button>
</template>
<script setup>
import { ref } from "vue"
import {
    getLicenseList,
    submitLicense,
} from "~/api/license"
import {
    toast
} from "~/composables/util"

const licenseForm = ref("")

const loading = ref(false)

const total = ref(0)
const left_days = ref(0)
const license_valid_bool = ref(true)
const license_valid_reason = ref("")

// 获取数据
getLicenseList()
    .then(res => {
        total.value = res.total
        // license剩余可用时间
        left_days.value = res.msg.left_days
        // license安全文件是否被关闭
        license_valid_bool.value = res.msg.license_valid_bool
        license_valid_reason.value = res.msg.license_valid_reason
    })


// 提交license
function submit() {
    loading.value = true
    submitLicense(licenseForm.value)
        .then(res => {
            if (res.err_code == 8000) {
                toast("无效license", "error")
            } else {
                toast("提交成功")
            }
        })
        .finally(() => {
            loading.value = false
            getLicenseList()
                .then(res => {
                    total.value = res.total
                    // license剩余可用时间
                    left_days.value = res.msg.left_days
                    // license安全文件是否被关闭
                    license_valid_bool.value = res.msg.license_valid_bool
                    license_valid_reason.value = res.msg.license_valid_reason
                }
                )
        })
}


</script>