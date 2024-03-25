import {createApp} from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import {router} from './router'
import store from './store'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import 'virtual:windi.css'

import "nprogress/nprogress.css"

import "./permission"

import permission from "~/directives/permission"


const app = createApp(App)

// 引入全局图标 icon
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}

app.use(store)

app.use(router)

app.use(ElementPlus)

app.use(permission)

app.mount('#app')
