<template>
  <el-row class="login-container">
    <el-col :lg="16" :md="12" class="left">
      <div>
        <div class="">{{ $store.state.settings.main_title }}</div>
        <div class="">{{ $store.state.settings.vice_title }}</div>
      </div>
    </el-col>

    <el-col :lg="8" :md="12" class="right">
      <h2 class="title">{{ $store.state.settings.login_title }}</h2>
      <div class="">
        <span class="line"></span>
        <span>
                    账号密码登录
                </span>
        <span class="line"></span>
      </div>
      <!-- 给form定义名字 ref="formRef"，与js的 const formRef=ref(null)对应 -->
      <el-form ref="formRef" :model="form" :rules="rules" class="w-[250px]">
        <!-- 在el-form-item中指定prop，和rule中要校验的key得一样 -->
        <el-form-item prop="login_name">
          <el-input v-model="form.login_name" placeholder="学生号|手机号">
            <template #prefix>
              <el-icon>
                <User/>
              </el-icon>
            </template>
          </el-input>
        </el-form-item>

        <el-form-item prop="password">
          <el-input v-model="form.password" placeholder="密码" type="password" show-password>
            <template #prefix>
              <el-icon>
                <Lock/>
              </el-icon>
            </template>
          </el-input>
        </el-form-item>

        <el-form-item>
          <el-button round class="w-[250px]" type="primary" @click="onSubmit" :loading="loading">登录</el-button>
        </el-form-item>
      </el-form>
    </el-col>
  </el-row>
</template>

<style scoped>
.login-container {
  @apply min-h-screen bg-blue-400;
}

.login-container .left {
  @apply flex items-center justify-center;
}

.login-container .right {
  @apply bg-light-50 flex items-center justify-center flex-col;
}

.left > div > div:first-child {
  @apply font-bold text-5xl text-light-50 mb-4;
}

.left > div > div:last-child {
  @apply text-gray-200 text-sm;
}

.right .title {
  @apply font-bold text-3xl text-gray-800;
}

.right > div {
  @apply flex items-center justify-center my-5 text-gray-300 space-x-2;
}

.right .line {
  @apply h-[1px] w-16 bg-gray-200;
}
</style>

<script setup>
import {onBeforeUnmount, onMounted, reactive, ref} from 'vue'
import {toast} from '~/composables/util'
import {useRouter} from 'vue-router'
import {useStore} from 'vuex'
import { getToken } from "~/composables/auth"

const router = useRouter()
const store = useStore()


// import {useStore} from 'vuex'
// const store = useStore()
store.dispatch("getSystemSetting")
    .then((res) => {
        // console.log(store.state.settings)
    }).finally((err) => {
      // console.log(err)
    })


// do not use same name with ref
const form = reactive({
  login_name: "",
  password: ""
})

// rules中定义的key值要和form中的key值一一对应
const rules = {
  login_name: [
    {
      required: true,
      message: '用户名不能为空',
      trigger: 'blur'
    },
  ],
  password: [
    {
      required: true,
      message: '请输入密码',
      trigger: 'blur'
    },
  ]
}

const formRef = ref(null)

const loading = ref(false)


const onSubmit = () => {
  formRef.value.validate((valid) => {
    if (valid) {

      // 验证通过后进行登录操作

      loading.value = true

      store.dispatch("login", form)
          .then(() => {
            const session_id = getToken()
            if (session_id) {
              toast("登录成功", "success");
              router.push("/")
            }else{
              toast("登陆失败", "error");
            }
          }).finally(() => {
        loading.value = false
      })

    } else {
      console.log('error submit!!')
      return false
    }
  })
}

// 监听回车事件的方法
function onKeyUp(e) {
  if (e.key == "Enter") {
    onSubmit()
  }
}

// 添加键盘监听
onMounted(() => {
  document.addEventListener('keyup', onKeyUp);
})

// 移除键盘监听
onBeforeUnmount(() => {
  document.removeEventListener('keyup', onKeyUp);
})

</script>