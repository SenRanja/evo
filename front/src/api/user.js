import axios from '~/axios'

export function getUserList(page, query = {}) {
    let q = []
    for (const key in query) {
        if (query[key]) {
            q.push(`${key}=${encodeURIComponent(query[key])}`)
        }
    }
    let r = q.join("&")
    // r = r ? ("?"+r) : ""

    return axios.get(`/api/user/?format=json&page=${page}&${r}`)
}
// export function updateUserStatus(){
//     return axios.put(`/api/user/?format=json`)
// }
export function createUser(data) {
    return axios.post(`/api/user/`, data)
}
export function updateUser(id, data) {
    return axios.put(`/api/user/${id}/`, data)
}
export function deleteUser(id) {
    return axios.delete(`/api/user/${id}/`)
}

// 获取全部角色
export function getRolesList() {
    return axios.delete(`/api/get_roles_list/`)
}

// 文件上传、导入
export function uploadFile(file) {
    

    const formData = new FormData();
    formData.append('excel_file', file);

    return axios.post('/api/import_user_from_excel/', formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });
}