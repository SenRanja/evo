import axios from '~/axios'

export function get_sub_without_score(id){
    return axios.get(`/api/get_sub_without_score/${id}/`)
}

export function submit_sub_score(data){
    return axios.post(`/api/submit_sub_score/`, data)
}