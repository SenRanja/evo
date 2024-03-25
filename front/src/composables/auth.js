import {useCookies} from '@vueuse/integrations/useCookies'
// import { ref, watchEffect } from 'vue'


// 此处是将cookie在非header中进行传递，如果cookie是HTTP Only的，那么就无法在前端获取到cookie
const TokenKey = "session_id"
const cookie = useCookies()

// 获取token
export function getToken() {
    return cookie.get(TokenKey)
}

// 设置token
export function setToken(token) {
    return cookie.set(TokenKey, token)
}

// 删除token
export function removeToken() {
    return cookie.remove(TokenKey)
}