import axios from '~/axios'

export function getSystemStatusMonitor() {
    return axios.get('/api/index_statistics/')
}

export function getStatistics2() {
    return axios.get('/api/index_statistics/')
}

// GET型传参，注意后端的url后有"/"的，get传参的？写在 / 之后，url后的 / 不能省略
export function getStatistics3(type) {
    return axios.get('/api/admin_statistics3/?type=' + type)
}
