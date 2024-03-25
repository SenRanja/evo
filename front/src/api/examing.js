import axios from '~/axios'

// 获取考试开始、结束时间
export function exam_manage_get(id){
    return axios.get(`/api/exam_manage/${id}/`)
}

export function detect_examed(id){
    return axios.get(`/api/detect_examed/${id}/`)
}

export function get_exam_paper(id){
    return axios.get(`/api/get_exam_paper/${id}/`)
}

export function submit_exam_paper(id, data){
    return axios.post(`/api/calculate_score/${id}/`, data)
}

// 交卷验证身份证后六位
export function check_idcard_tail(id, data){
    return axios.get(`/api/check_idcard_tail/${id}/`, data)
}

export function get_old_results(id){
    return axios.post(`/api/get_old_results/${id}/`)
}
