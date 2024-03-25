import axios from '~/axios'


// export function getNoticeList(page, query = {}){
export function getNoticeList(){
    return axios.get(`/api/get_video_subjects/`)
}

export function createNotice(data){
    return axios.post('/api/notice/', data);
}

export function updateNotice(id,data){
    return axios.put("/api/notice/"+id+"/",data)
}

export function deleteNotice(id){
    return axios.delete(`/api/notice/${id}/`)
}