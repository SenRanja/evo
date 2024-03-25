import axios from '~/axios'


// 下载资料
export function getFtpDataBySid(id){
    return axios.get(`/api/get_ftps_by_subject/${id}/`);
}

// 上传资料
export function uploadFtpDocBySid(id,file){
    const formData = new FormData();
    formData.append('subject', id);
    formData.append('file', file);
    formData.append('order', 1);
    return axios.post('/api/ftp_upload/', formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });
}
// 删除资料
export function deleteFtpDataBySid(id){
    return axios.delete(`/api/ftp/${id}/`);
}

// admin使用的获取subjects的接口
export function getSubjectWithGroupList(){
    return axios.get(`/api/get_subject_list/`);
}


export function getNoticeList(page){
    return axios.get(`/api/subject/?format=json&page=${page}`);
}

export function createNotice(data){
    return axios.post('/api/subject/', data);
}

export function updateNotice(id,data){
    return axios.put(`/api/subject/${id}/`,data);
}

export function deleteNotice(id){
    return axios.delete(`/api/subject/${id}/`);
}
