import axios from '~/axios'


export function getNoticeList(page, query = {}){
    let q = []
    for (const key in query) {
        if(query[key]){
            q.push(`${key}=${encodeURIComponent(query[key])}`)
        }
    }
    let r = q.join("&")
    // r = r ? ("?"+r) : ""
    return axios.get(`/api/exam_score/?format=json&page=${page}&${r}`)
    
}

export function createNotice(form){
    const data = {
        title: form.title,
        description: form.description,
    }
    return axios.post('/api/exam_score/', JSON.stringify(data), {
        headers: {
            'Content-Type': 'application/json'
        }
    });
}

export function updateNotice(id,data){
    return axios.put(`/api/exam_score/${id}/`,data)
}

export function deleteNotice(id){
    return axios.delete(`/api/exam_score/${id}/`)
}