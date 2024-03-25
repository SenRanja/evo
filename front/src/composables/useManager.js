import { reactive, ref } from 'vue'
import { logout, updatePassword } from "~/api/manager"
import { showModal, toast } from '~/composables/util'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'

export function userRepassword() {

    const router = useRouter()
    const store = useStore()

    // 修改密码
    const formDrawerRef = ref(null)
    // const showDrawer = ref(false)

    const form = reactive({
        oldpassword: "",
        password: "",
        repassword: ""
    })

    const rules = {
        oldpassword: [
            {
                required: true,
                message: '旧密码不能为空',
                trigger: 'blur'
            },
        ],
        password: [
            {
                required: true,
                message: '新密码不能为空',
                trigger: 'blur'
            },
        ],
        repassword: [
            {
                required: true,
                message: '确认密码不能为空',
                trigger: 'blur'
            },
        ]
    }

    const formRef = ref(null)

    // const loading = ref(false)

    const onSubmit = () => {
        formRef.value.validate((valid) => {
            if (valid) {
                // console.log('submit!')
                // loading.value = true
                formDrawerRef.value.showLoading()
                updatePassword(form)
                    .then(res => {
                        toast("修改密码成功，请重新登陆", "success");
                        store.dispatch("logout")
                            .finally(() => location.reload())
                        router.push("/login")
                    })
                    .finally(() => {
                        formDrawerRef.value.hideLoading()
                    })
            } else {
                return false
            }
        })
    }

    const openRePasswordForm = () => formDrawerRef.value.open()

    return {
        formDrawerRef,
        form,
        rules,
        formRef,
        onSubmit,
        openRePasswordForm
    }
}

export function userLogout() {
    const router = useRouter()
    const store = useStore()

    function handleLogout() {
        showModal("是否要退出登录")
            .then((confirmed) => {
                console.log("handleLogout接受的showModal返回值", confirmed)
                if (confirmed) {
                    logout()
                        .then()
                        .catch()
                        .finally(() => {
                            // 移除cookie中的token
                            // 清除当前用户状态 vuex
                            store.dispatch("logout")

                            // 跳转到登录页
                            router.push("/login")

                            // 提示退出登录成功
                            toast("退出登录成功")
                        })
                }else{
                    // toast("取消退出登录操作");
                }
            })
    }

    return { handleLogout }
}


