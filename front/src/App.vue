<script setup>
// import HelloWorld from './components/HelloWorld.vue'
// import TheWelcome from './components/TheWelcome.vue'

</script>

<template>

  <router-view></router-view>
</template>

<style>
body {
  @apply bg-gray-100;
}

.btn {
  @apply bg-purple-500 text-light-700 px-4 py-2 rounded-full transition-all duration-500 hover:( bg-pink-900) focus:( ring-8 ring-purple-900);
}

#nprogress .bar {
  background: #406e89 !important;
  position: fixed;
  z-index: 1031;
  top: 0;
  left: 0;
  width: 100%;
  height: 3px !important;
}

/* 全局滚动条变细 */
::-webkit-scrollbar {
  width: 4px;
  height: 6px;
}

::-webkit-scrollbar-corner {
  display: block;
}

::-webkit-scrollbar-thumb {
  background-color: rgba(0, 0, 0, 0.2);
  border-radius: 8px;
}

::-webkit-scrollbar-thumb,
::-webkit-scrollbar-track {
  border-left-color: transparent;
  border-right-color: transparent;
  background-color: rgba(0, 0, 0, 0.1);
}
</style>
