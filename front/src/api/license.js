import axios from '~/axios'


// export function getNoticeList(page, query = {}){
export function getLicenseList(){
    // return axios.get(`/api/notice/?format=json&page=${page}&${r}`)
    return axios.get(`/api/get_license_time/`)
}

export function submitLicense(license){
    return axios.get(`/api/submit_license/${license}/`);
}