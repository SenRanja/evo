import axios from '~/axios'


// export function getNoticeList(page, query = {}){
export function getNoticeList(page){
    // let q = []
    // for (const key in query) {
    //     if(query[key]){
    //         q.push(`${key}=${encodeURIComponent(query[key])}`)
    //     }
    // }
    // let r = q.join("&")
    // r = r ? ("?"+r) : ""

    // return axios.get(`/api/notice/?format=json&page=${page}&${r}`)
    return axios.get(`/api/notice/?format=json&page=${page}`)
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