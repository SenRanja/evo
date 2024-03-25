<template>
    <el-main class="image-main">
      <videoPlay v-bind="options" poster="http://localhost:81/poster/1.png"
                 :src="videoSource" logo=""/>
    </el-main>
  </template>
  
  <script>
  // 视频播放组件
  import "vue3-video-play/dist/style.css";
  import Vue3VideoPlay from "vue3-video-play";
  
  export default {
    components: {
      videoPlay: Vue3VideoPlay,
    },
    props: {
        videoSource: String,// 海报地址
        // poster: String, // 海报地址
    },
    data() {
      const options = {
        width: "800px", //播放器宽度
        height: "500px", //播放器高度
        color: "#409eff", //主题色
        title: "", //视频名称
        muted: false, //静音
        webFullScreen: false,
        speedRate: ["0.75", "1.0", "1.25", "1.5", "2.0"], //播放倍速
        autoPlay: false, //自动播放
        loop: true, //循环播放
        mirror: false, //镜像画面
        ligthOff: false, //关灯模式
        volume: 0.3, //默认音量大小
        control: true, //是否显示控制
        controlBtns: [
          "audioTrack",
          "quality",
          "speedRate",
          "volume",
          "setting",
          "pip",
          "pageFullScreen",
          "fullScreen",
        ], //显示所有按钮,
      };
      return {
        // videoSource: "http://localhost:81/1-文件下载组件.mp4",
        options,
      };
    },
  };
  
  </script>
  
  <style>
  .image-main {
    position: relative;
  }
  
  
  .image-main .top {
    position: absolute;
    top: 0;
    right: 0;
    left: 0;
    bottom: 50px;
    overflow-y: auto;
  }
  
  .image-main .bottom {
    position: absolute;
    bottom: 0;
    height: 0;
    left: 0;
    right: 0;
    @apply flex items-center justify-center;
  }
  </style>