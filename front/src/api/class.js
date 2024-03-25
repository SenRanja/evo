import axios from '~/axios'

// 此处求开发速度，方法名虽然是User，但是接口都是Group

// 获取 Groups
export function getUserList(page, query = {}) {
    let q = []
    for (const key in query) {
        if (query[key]) {
            q.push(`${key}=${encodeURIComponent(query[key])}`)
        }
    }
    let r = q.join("&")
    // r = r ? ("?"+r) : ""

    return axios.get(`/api/group/?format=json&page=${page}&${r}`)
}

// 新建 Group
export function createUser(data) {
    return axios.post(`/api/group/`, data)
}

// 更新 Group
export function updateUser(url, data) {
    // 查找group id
    const startIndex = url.indexOf('/api/group/') + '/api/group/'.length;
    const endIndex = url.indexOf('/?');
    const id = url.substring(startIndex, endIndex !== -1 ? endIndex : undefined);

    return axios.put(`/api/group/${id}/`, data)
}

// 删除 Group
export function deleteUser(url) {
    // 查找group id
    const startIndex = url.indexOf('/api/group/') + '/api/group/'.length;
    const endIndex = url.indexOf('/?');
    const id = url.substring(startIndex, endIndex !== -1 ? endIndex : undefined);

    return axios.delete(`/api/group/${id}/`)
}

// 获取Group内全部用户
export function getClassUserList(url) {
    // 查找group id
    const startIndex = url.indexOf('/api/group/') + '/api/group/'.length;
    const endIndex = url.indexOf('/?');
    const id = url.substring(startIndex, endIndex !== -1 ? endIndex : undefined);

    return axios.get(`/api/group/${id}/`)
}

// Group加人
export function addNewUserToClass(url, stu_id) {
    // 第二个参数是学生的stu_id或身份证号
    // 查找group id
    const startIndex = url.indexOf('/api/group/') + '/api/group/'.length;
    const endIndex = url.indexOf('/?');
    const id = url.substring(startIndex, endIndex !== -1 ? endIndex : undefined);


    return axios.get(`/api/group_add_user_by_sid/${id}/${stu_id}/`)
}

// Group踢人
export function deleteUserToClass(url, data) {
    // 第二个参数是学生的stu_id或身份证号
    // 查找group id
    const startIndex = url.indexOf('/api/group/') + '/api/group/'.length;
    const endIndex = url.indexOf('/?');
    const id = url.substring(startIndex, endIndex !== -1 ? endIndex : undefined);

    console.log(id, data)
    return axios.post(`/api/group_delete_user_by_data/${id}/`, data)
}