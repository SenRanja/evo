import {ElMessage, ElMessageBox, ElNotification} from 'element-plus'
import nProgress from 'nprogress'

// 消息提示
export function toast(message, type = "success", duration = 3000, dangerouslyUseHTMLString = false) {
    ElNotification({
        message: message,
        type: type,
        duration: duration
    })
}

// 退出登录按钮
export function showModal(content = "提示内容", type = "warning", title = "", dangerouslyUseHTMLString = false) {
    return ElMessageBox.confirm(
        content,
        {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type,
        }
    )
        .then(() => {
            return true
            // ElMessage({
            //     type: 'success',
            //     message: 'Delete completed',
            // })
        })
        .catch(() => {
            return false
            // ElMessage({
            //     type: 'info',
            //     message: 'Delete canceled',
            // })
        })
}

// 显示全屏loading
export function showFullLoading() {
    nProgress.start()
}

// 隐藏全屏loading
export function hideFullLoading() {
    nProgress.done()
}