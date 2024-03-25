import axios from '~/axios'

export function getUserList(page, query = {}){
    let q = []
    for (const key in query) {
        if(query[key]){
            q.push(`${key}=${encodeURIComponent(query[key])}`)
        }
    }
    let r = q.join("&")
    // r = r ? ("?"+r) : ""

    return axios.get(`/api/exam_question/?format=json&page=${page}&${r}`)
}
// export function updateUserStatus(){
//     return axios.put(`/api/user/?format=json`)
// }
export function createUser(data){
    return axios.post(`/api/exam_question/?format=json`, data)
}
export function updateUser(id,data){
    return axios.put(`/api/exam_question/${id}/`, data)
}
export function deleteUser(id){
    return axios.delete(`/api/exam_question/${id}/`)
}

// 文件上传、导入
export function uploadFile(file) {
    

    const formData = new FormData();
    formData.append('questions_exam_file', file);

    return axios.post('/api/import_question_from_excel/', formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });
}