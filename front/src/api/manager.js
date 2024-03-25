import axios from '~/axios'

export function login_api(username, password) {
    const data = {
        "login_name": username,
        "password": password
    }

    return axios.post('/api/login/', JSON.stringify(data), {
        headers: {
            'Content-Type': 'application/json'
        }
    });
}

export function get_system_setting() {
    return axios.get('/api/system_manage/1/?format=json');
}

export function login_auth() {
    return axios.post('/api/login_check/');
}

export function getinfo() {
    return axios.post('/api/get_info/')
}

export function logout() {
    return axios.post('/api/logout/')
}

export function updatePassword(data) {
    return axios.post('/api/updatepassword/', data)
}



