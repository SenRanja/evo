import axios from '~/axios'

// 考试管理   admin视角   方法名暂未修改
export function getUserList(page, query = {}){
    let q = []
    for (const key in query) {
        if(query[key]){
            q.push(`${key}=${encodeURIComponent(query[key])}`)
        }
    }
    let r = q.join("&")
    // r = r ? ("?"+r) : ""

    return axios.get(`/api/exam_manage/?format=json&page=${page}&${r}`)
}
// export function updateUserStatus(){
//     return axios.put(`/api/user/?format=json`)
// }

export function createUser(data){
    return axios.post(`/api/exam_manage/?format=json`, data)
}
export function updateUser(id,data){
    return axios.put(`/api/exam_manage/${id}/`, data)
}
export function deleteUser(id){
    return axios.delete(`/api/exam_manage/${id}/`)
}

// 管理员视角，获取题库
export function getExamQuestionList(){
    return axios.delete(`/api/question_database_list/`)
}

// 管理员视角，设置题库
export function updateExamQuestion(id,data){
    return axios.post(`/api/update_exam_manage_question_db/${id}/`, data)
}

// 考试管理    admin视角  考试--题库 对应数据条目
// 获取 某考试 的 考试-题库 列表
export function getExamQuestion(id){
    // let q = []
    // for (const key in query) {
    //     if(query[key]){
    //         q.push(`${key}=${encodeURIComponent(query[key])}`)
    //     }
    // }
    // let r = q.join("&")
    // return axios.get(`/api/exam_manage_question_database/?format=json&${r}`)
    return axios.get(`/api/exam_manage_question_database/?format=json&exam_id=${id}`)
}

// 考试列表     学生视角
export function getStuExamList(){
    return axios.get(`/api/get_exam_manages/`)
}

export function getStuExamPaper(examId){
    return axios.get(`/api/get_exam_paper/${examId}/`)
}

// 预览试卷，下载word
export function getExamPaperOfWord(examId){
    return axios.get(`/api/generate_exam_paper_word/${examId}/`)
}

