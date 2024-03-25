import store from "~/store"

// 权限相关，依据 store.stat.ruleNames 判断是否有权限
function hasPermission(value, el = false) {
    if (!Array.isArray(value)) {
        throw new Error(`需要配置权限，例如 v-permission="['getStatistics3,GET']"`)
    }

    // 如果找到，返回索引，如果没有找到，返回 -1
    // hasAuth 变量用于存储这个检查的结果，如果找到权限，hasAuth 将是 true
    const hasAuth = value.findIndex(v => store.state.ruleNames.includes(v)) != -1
    if (el && !hasAuth) {
        // 如果传入了 DOM 元素 el 且用户没有相应权限，通过删除这个 DOM 元素来隐藏相应的内容
        el.parentNode && el.parentNode.removeChild(el)
    }

    // 返回权限检查的结果，即用户是否具有相应的权限
    return hasAuth
}

// 此部分创造 v-permission 指令,用于在 pages/index.vue 中使用 v-permission 根据ruleNames来是否展示不同组件
export default {
    install(app) {
        app.directive("permission", {
            mounted(el, binding) {
                // el 是获取的dom元素，binding 是指令的参数， binding.value 是指令的值
                hasPermission(binding.value, el)
            }
        })
    }
}