import {createRouter, createWebHistory} from 'vue-router'

import Admin from "~/layouts/admin.vue"
import Index from '~/pages/index.vue'
import NotFound from '~/pages/404.vue'
import Login from '~/pages/login.vue'
import NoticeList from '~/pages/notice/list.vue'
import SettingBase from '~/pages/setting/base.vue'

// 用户列表
import UserList from '~/pages/user/list.vue'
// 导入用户
import UserImport from '~/pages/user/import.vue'

// 班级管理
import ClassManage from '~/pages/class/list.vue'
// 班级管理用户
import ClassManageUsers from '~/pages/class/manage_users.vue'

// 参加考试
import EnterExam from '~/pages/exam_questions/examing.vue'
// 考试管理
import ExamManage from '~/pages/exam/list.vue'
// 考试列表
import ExamQuesList from '~/pages/exam_questions/list.vue'
// 教师判分
import JudgeSubExam from '~/pages/exam_questions/judge_sub.vue'
// 成绩单管理
import ResultsManage from '~/pages/result/list.vue'

// 题库管理
import QuestionsList from '~/pages/question/list.vue'
// 导入题库
import QuestionsImport from '~/pages/question/import.vue'

// 学科管理
import SubjectList from '~/pages/subject/list.vue'
// 视频学习
import VideoStudyList from '~/pages/video_study/list.vue'

// license
import LicenseList from '~/pages/license/list.vue'

// 视频监控
import MonitorList from '~/pages/monitor/list.vue'

// 消息通知
import MessageList from '~/pages/message/list.vue'


// 默认路由，所有用户共享
const routes = [
    {
        path: '/',
        name: "admin",
        component: Admin,
    },
    // 登录页面
    {
        path: '/login',
        component: Login,
        meta: {
            title: "登录页"
        }
    },
    // 将匹配所有内容并将其放在 `$route.params.pathMatch` 下
    {
        path: '/:pathMatch(.*)*',
        name: 'NotFound',
        component: NotFound
    },

    

]

// 动态路由，用于匹配菜单动态添加路由的
// 注意，asyncRoutes 本身不会像 routes 这样直接注册到路由，仅仅是存储全部后台路径，用户登录获取个人信息和可访问菜单路径后，再由 addRoutes 匹配 注意，asyncRoutes 中路由，然后注册
// 此处不写 component 是无法跳转的
const asyncRoutes = [
    // 首页
    {
        path:"/",
        name:"/",
        component:Index,
        meta:{
            title:"首页"
        }
    },
    // 试题管理
    {
        path: "/question/change",
        name: "/question/change",
        component: QuestionsList,
        meta: {
            title: "试题管理"
        }
    },
    {
        path: "/question/import_db",
        name: "/question/import_db",
        component: QuestionsImport,
        meta: {
            title: "试题导入"
        }
    },

    // 考试管理
    {
        path: "/exam_questions/examing",
        name: "examing",
        component: EnterExam,
        meta: {
            title: "考试中"
        }
    },
    {
        path: "/exam/manage",
        name: "/exam/manage",
        component: ExamManage,
        meta: {
            title: "考试管理"
        }
    },
    {
        path: "/exam/list",
        name: "/exam/list",
        component: ExamQuesList,
        meta: {
            title: "考试列表"
        }
    },
    
    // 教师判分
    {
        path: "/exam_questions/judge_sub",
        name: "judge_sub_exam",
        component: JudgeSubExam,
        meta: {
            title: "教师判分"
        }
    },

    // 成绩单管理
    {
        path: "/result/manage",
        name: "/result/manage",
        component: ResultsManage,
        meta: {
            title: "成绩单"
        }
    },

    // 用户管理
    {
        path: "/user/manage",
        name: "/user/manage",
        component: UserList,
        meta: {
            title: "用户列表"
        }
    },
    {
        path: "/user/import",
        name: "/user/import",
        component: UserImport,
        meta: {
            title: "导入用户"
        }
    },

    // 班级管理
    {
        path: "/class/list",
        name: "/class/list",
        component: ClassManage,
        meta: {
            title: "班级管理"
        }
    },    
    // 班级管理用户
    {
        path: "/class/manage_users",
        name: "/class/manage_users",
        component: ClassManageUsers,
        meta: {
            title: "班级管理用户"
        }
    },
    

    // 公告管理
    {
        path: "/notice/list",
        name: "/notice/list",
        component: NoticeList,
        meta: {
            title: "公告列表"
        }
    },

    // 课程管理
    {
        path: "/subject/list",
        name: "/subject/list",
        component: SubjectList,
        meta: {
            title: "学科列表"
        }
    },

    // 视频管理
    {
        path: "/video_study/list",
        name: "/video_study/list",
        component: VideoStudyList,
        meta: {
            title: "视频学习"
        }
    },


    // 系统
    {
        path: "/setting/base",
        name: "/setting/base",
        component: SettingBase,
        meta: {
            title: "配置"
        }
    },

    // license
    {
        path: "/license/list",
        name: "/license/list",
        component: LicenseList,
        meta: {
            title: "license"
        }
    },

    // 视频监控
    {
        path: "/monitor/list",
        name: "/monitor/list",
        component: MonitorList,
        meta: {
            title: "monitor"
        }
    },

    // 消息通知
    {
        path: "/message/list",
        name: "/message/list",
        component: MessageList,
        meta: {
            title: "message"
        }
    },
]

export const router = createRouter({
    // 两种路由模式，hash的是url根目录后面跟#的，如http://localhost/#/user/list；history的是正常的url，如http://localhost/user/list
    // history: createWebHashHistory(),
    history: createWebHistory(),
    routes  // 默认只有静态路由
    // routes: [...routes, ...asyncRoutes] // 将静态路由和动态路由合并
})

// 动态添加路由的方法
// 在全局前置守卫中调用，核验、新增asyncRoutes中的路由
export function addRoutes(menu) {
    // 是否有新的路由
    let hasNewRoutes = false
    const findAndAddRoutesByMenu = (arr) => {
        arr.forEach(e => {
            let item = asyncRoutes.find(o => o.path == e.frontpath)

            if (item && !router.hasRoute(item.path)) {
                router.addRoute("admin", item)
                hasNewRoutes = true
            }
            if (e.child && e.child.length > 0) {
                findAndAddRoutesByMenu(e.child)
            }
        })
    }

    findAndAddRoutesByMenu(menu)

    return hasNewRoutes
}
