import { addRoutes, router } from "~/router"
import { toast, hideFullLoading, showFullLoading } from "~/composables/util"
import store from "~/store"
import { getToken } from "~/composables/auth"


// 全局前置守卫
// hasGetInfo 是否获取用户信息、路由信息
let hasGetInfo = false
router.beforeEach(async (to, from, next) => {
    // 显示loading
    showFullLoading()

    const session_id = getToken()

    // 没有登录，强制跳转回登录页
    if(!session_id && to.path != "/login"){
        toast("请先登录","error")
        return next({ path:"/login" })
    }

    // 防止重复登录
    if(session_id && to.path == "/login"){
        toast("请勿重复登录","error")
        return next({ path:from.path ? from.path : "/" })
    }

    // 如果用户登录了，自动获取用户信息，并存储在vuex当中
    let hasNewRoutes = false
    if (session_id && !hasGetInfo) {
        let { menus } = await store.dispatch("getinfo");
        hasGetInfo = true
        // 动态加载路由
        hasNewRoutes = addRoutes(menus);
    }

    // 设置页面标题
    let title = to.meta.title ? to.meta.title : "考试系统"
    document.title = title

    hasNewRoutes ? next(to.fullPath) : next()

})

// 全局后置钩子
router.afterEach((to, from) => {
    hideFullLoading();
})
