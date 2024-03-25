import axios from '~/axios'


export function get_video_by_subject(sid){
    return axios.get(`/api/get_video_by_subject/${sid}/`)
}

// 文件上传、导入
export function uploadFile(file, title, order, subject_id) {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('title', title);
    formData.append('order', order);
    formData.append('subject', subject_id);

    return axios.post('/api/video_upload/', formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });
}

export function video_put(item){
    const vid = item.id
    delete item.user;
    delete item.id;
    return axios.put(`/api/video/${vid}/`, item)
}

export function video_del(vid){
    return axios.delete(`/api/video/${vid}/`)
}