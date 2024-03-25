<template>
  <el-form :model="form" ref="formRef" label-width="150px" :inline="false">
    <el-form-item label="主标题" prop="main_title">
      <el-input v-model="form.main_title" placeholder=""></el-input>
    </el-form-item>

    <el-form-item label="副标题" prop="vice_title">
      <el-input v-model="form.vice_title" placeholder=""></el-input>
    </el-form-item>

    <el-form-item label="登录标题" prop="login_title">
      <el-input v-model="form.login_title" placeholder=""></el-input>
    </el-form-item>

    <el-form-item label="鼠标移出屏幕次数" prop="cheat_mouse_out">
      <el-input v-model="form.cheat_mouse_out" placeholder=""></el-input>
    </el-form-item>

    <el-form-item label="切屏次数" prop="cheat_page_out">
      <el-input v-model="form.cheat_page_out" placeholder=""></el-input>
    </el-form-item>
  </el-form>
  <el-button type="text" @click="handleSubmit">修改</el-button>
</template>

<script setup>
import { ref, reactive } from "vue"
import {
  getSettingsList,
  updateSettingsList,
} from "~/api/settings"

import {
  toast
} from "~/composables/util"

// import {useStore} from 'vuex'
// const store = useStore()
// store.dispatch("getSystemSetting")
//     .then((res) => {
//         // console.log(store.state.settings)
//     }).finally((err) => {
//         // console.log(err)
//       })
      

const form = reactive({
  main_title: "",
  vice_title: "",
  login_title: "",
  cheat_mouse_out: 0,
  cheat_page_out: 0
})

// 获取数据
getSettingsList()
  .then(res => {
    form.main_title = res.main_title
    form.vice_title = res.vice_title
    form.login_title = res.login_title
    form.cheat_mouse_out = res.cheat_mouse_out
    form.cheat_page_out = res.cheat_page_out
  })

const handleSubmit = () => {
  updateSettingsList(form)
    .then(res => {
      toast("success", "修改成功")
    })
    .catch(err => {
      toast("error", "修改失败")
    })
}

</script>