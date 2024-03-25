import { createStore } from 'vuex'
import { getinfo, login_api, get_system_setting } from '~/api/manager'
import { removeToken } from '~/composables/auth'

// 创建一个新的 store 实例
const store = createStore({
    state() {
        return {
            // 用户信息
            user: {},

            // 侧边宽度
            asideWidth: "250px",

            // 菜单
            menus: [],
            // 菜单权限规则
            ruleNames: [],

            // 是否处于考试状态
            isExamMode: false,

            // 考试id
            ExamId: 0,

            // 系统参数
            settings: {},
        }
    },
    mutations: {
        // 记录用户信息
        SET_USERINFO(state, user) {
            state.user = user
        },

        // 展开/缩起 侧边
        handleAsideWidth(state) {
            // state.asideWidth = state.asideWidth == "250px" ? "64px" : "250px"
            // 如果处于考试状态，侧边栏宽度为 0
            state.asideWidth = state.isExamMode ? "0px" : state.asideWidth === "250px" ? "64px" : "250px";
        },

        SET_MENUS(state, menus) {
            state.menus = menus
        },

        SET_RULENAMES(state, ruleNames) {
            state.ruleNames = ruleNames
        },

        // 设置是否处于考试状态
        SET_EXAM_MODE(state, isExamMode) {
            state.isExamMode = isExamMode;
        },

        // 设置考试id
        SET_EXAM_ID(state, examId) {
            state.ExamId = examId;
        },

        // 设置系统参数
        SET_SETTINGS(state, data) {
            state.settings = data;
        },
    },
    actions: {
        // 获取系统参数
        getSystemSetting({ commit }) {
            return new Promise((resolve, reject) => {
                get_system_setting()
                    .then(res => {
                        commit('SET_SETTINGS', res)
                        resolve(res)
                    })
                    .catch(err => reject)
            })
        },

        // 登录
        login({ commit }, { login_name, password }) {
            return new Promise((resolve, reject) => {
                login_api(login_name, password)
                    .then(res => {
                        resolve(res.data)
                    })
                    .catch(err => reject)
            })
        },

        // 获取当前登录用户信息
        getinfo({ commit }) {

            // 改使用 async 声明，可直接使用 await 等待 getinfo 方法的执行结果，因此无须返回 Promise
            return new Promise((resolve, reject) => {
                getinfo()
                    .then(res => {
                        commit('SET_USERINFO', res.data)
                        commit('SET_MENUS', res.data.menus)
                        commit('SET_RULENAMES', res.data.ruleNames)

                        resolve(res.data)
                    })
                    .catch(err => reject)
            })
        },

        // 退出登录
        logout({ commit }) {
            // 移除cookie的token
            removeToken()

            // 清除当前用户状态 vuex
            commit('SET_USERINFO', {})
        },

        // 新增 action 用于设置考试模式状态
        setExamMode({ commit }, isExamMode) {
            commit("SET_EXAM_MODE", isExamMode);
            // 根据考试模式状态，调整 Aside 宽度
            commit("handleAsideWidth");
        },

        // 设置考试id
        setExamId({ commit }, examId) {
            commit("SET_EXAM_ID", examId);
        },
    }
})

export default store

