import axios from '~/axios'



export function getSettingsList(){
    return axios.get(`/api/system_manage/1/?format=json`)
}

export function updateSettingsList(data){
    return axios.put(`/api/system_manage/1/?format=json`, data);
}