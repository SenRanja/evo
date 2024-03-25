<template>
  <div class="f-header">
        <span class="logo">
            <el-icon class="mr-1">
                <ElemeFilled/>
            </el-icon>
            {{ $store.state.settings.main_title }}
        </span>
    <el-icon class="icon-btn" @click="$store.commit('handleAsideWidth')">
      <Fold v-if="$store.state.asideWidth == '250px'"/>
      <Expand v-else/>
    </el-icon>

    <el-tooltip effect="dark" content="刷新" placement="bottom">

      <el-icon class="icon-btn" @click="handleRefresh">
        <Refresh/>
      </el-icon>

    </el-tooltip>
    <div class="ml-auto flex items-center " style="margin-left: auto;">

      <el-tooltip effect="dark" content="切换全屏" placement="bottom">
        <el-icon class="icon-btn" @click="toggle">
          <FullScreen v-if="!isFullscreen"/>
          <Aim v-else/>
        </el-icon>
      </el-tooltip>
      <el-dropdown class="dropdown" @command="handleCommand">

                <span class="flex items-center text-light-50">
                    <el-button class=" bg-transparent text-light-200">
                        <el-avatar class="mr-2" :size="25" :src="$store.state.user.avatar"/>
                        {{ $store.state.user.username }}
                        <el-icon class="el-icon--right">
                            <arrow-down/>
                        </el-icon>
                    </el-button>
                </span>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="rePassword">修改密码</el-dropdown-item>
            <el-dropdown-item command="logout">退出登录</el-dropdown-item>
          </el-dropdown-menu>

          <form-drawer ref="formDrawerRef" title="修改密码" destroyOnClose @submit="onSubmit">

            <!-- 修改密码表单 -->
            <el-form ref="formRef" :model="form" :rules="rules" label-width="80px" size="small">
              <el-form-item prop="oldpassword" label="旧密码">
                <el-input v-model="form.oldpassword" placeholder="请输入旧密码">
                  <template #prefix>
                    <el-icon>
                      <User/>
                    </el-icon>
                  </template>
                </el-input>
              </el-form-item>

              <el-form-item prop="password" label="新密码">
                <el-input v-model="form.password" placeholder="请输入密码" type="password" show-password>
                  <template #prefix>
                    <el-icon>
                      <Lock/>
                    </el-icon>
                  </template>
                </el-input>
              </el-form-item>

              <el-form-item prop="repassword" label="确认密码">
                <el-input v-model="form.repassword" placeholder="再次输入密码" type="password" show-password>
                  <template #prefix>
                    <el-icon>
                      <Lock/>
                    </el-icon>
                  </template>
                </el-input>
              </el-form-item>

            </el-form>

          </form-drawer>

        </template>
      </el-dropdown>
    </div>
  </div>
</template>

<script setup>
import FormDrawer from '~/components/FormDrawer.vue'
import {userLogout, userRepassword} from '~/composables/useManager'

// 全屏，isFullscreen 是否全屏，toggle 切换全屏
import {useFullscreen} from '@vueuse/core'

const {isFullscreen, toggle} = useFullscreen()
const {
  formDrawerRef,
  form,
  rules,
  formRef,
  onSubmit,
  openRePasswordForm
} = userRepassword()
const {handleLogout} = userLogout()

const handleCommand = (c) => {
  switch (c) {
    case "logout":
      handleLogout()
      break
    case "rePassword":
      openRePasswordForm()
      // showDrawer.value = true
      break
  }
}

// 刷新
const handleRefresh = () => {
  // router.go(0)
  console.log("刷新")
}

</script>

<style>
.f-header {
  @apply flex items-center bg-blue-500 text-light-200 fixed top-0 left-0 right-0;
  height: 64px;
  z-index: 1000;
}

.logo {
  width: 250px;
  letter-spacing: 0;
  @apply flex items-center justify-center text-2xl font-semibold;
}

.icon-btn {
  @apply flex items-center justify-center;
  width: 42px;
  height: 64px;
  cursor: pointer;
}

.icon-btn:hover {
  @apply bg-indigo-200;
}

.f-header .dropdown {
  @apply flex items-center justify-center mx-5;
  width: 200px;
  height: 64px;
  cursor: pointer;
}
</style>