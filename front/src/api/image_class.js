import axios from '~/axios'

export function getImageClassList(page) {
    return axios.get('http://ceshi13.dishait.cn/admin/image_class/' + page)
}