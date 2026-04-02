<template>
  <div class="tabbar-shell">
    <van-tabbar v-model="active" route class="floating-tabbar">
      <van-tabbar-item to="/home" icon="home-o">{{ $t('nav.home') }}</van-tabbar-item>
      <van-tabbar-item to="/aichat" icon="chat-o">{{ $t('nav.aiChat') }}</van-tabbar-item>
      <van-tabbar-item to="/my" icon="user-o">{{ $t('nav.my') }}</van-tabbar-item>
    </van-tabbar>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const active = ref(0)

const setActiveTab = () => {
  const path = route.path
  if (path.includes('/home')) {
    active.value = 0
  } else if (path.includes('/aichat')) {
    active.value = 1
  } else if (path.includes('/my')) {
    active.value = 2
  }
}

setActiveTab()
watch(() => route.path, setActiveTab)
</script>

<style scoped>
.tabbar-shell {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1200;
  pointer-events: none;
}

.floating-tabbar {
  pointer-events: auto;
  width: min(100% - 24px, 420px);
  margin: 0 auto calc(12px + var(--safe-area-inset-bottom));
  padding: 8px 10px calc(8px + var(--safe-area-inset-bottom));
  border-radius: 28px;
  overflow: hidden;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.04), rgba(255, 255, 255, 0.015)), var(--nav-background);
  border: 1px solid var(--nav-border);
  box-shadow: var(--shadow-soft);
  backdrop-filter: blur(var(--backdrop-blur));
  -webkit-backdrop-filter: blur(var(--backdrop-blur));
}

:deep(.van-tabbar) {
  height: auto;
}

:deep(.van-tabbar-item) {
  position: relative;
  min-height: 54px;
  color: var(--tab-inactive);
  transition: color 0.2s ease, transform 0.2s ease;
}

:deep(.van-tabbar-item--active) {
  color: var(--tab-active);
  transform: translateY(-1px);
}

:deep(.van-tabbar-item__icon) {
  font-size: 22px;
  margin-bottom: 4px;
}

:deep(.van-tabbar-item__text) {
  font-size: 12px;
  letter-spacing: 0.02em;
}
</style>
