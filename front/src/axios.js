import axios from "axios"
import { toast } from '~/composables/util'

const service = axios.create({
    // 【开发调试，npm run build 全部注释】
    // baseURL: "/api",  // 若此处使用 /api 则使用到vite.config.js中的proxy代理
    // 如果此处不使用 vite 配置的proxy代理，需要配置 withCredentials
    // baseURL: "http://127.0.0.1:8000/",

    // 打包，不注释
    withCredentials: true
});

// 添加请求拦截器
service.interceptors.request.use(function (config) {
    // 在发送请求之前做些什么

    return config;
}, function (error) {
    // 对请求错误做些什么
    return Promise.reject(error);
});

// 添加响应拦截器
service.interceptors.response.use(function (response) {
    // 对响应数据做点什么
    return response.data;
}, function (error) {
    // 对响应错误做点什么

    let msg = error.response.data.msg
    if (msg == "unauth") {
        msg = "未登录或登录已过期，请重新登录"
        //   logout 会移除cookie，清空vuex
        store.dispatch('logout').finally(() => location.reload())
        toast(msg, "error")
    }


    return Promise.reject(error);
});

export default service;