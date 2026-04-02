<template>
  <div class="app-shell">
    <div class="app-background">
      <div class="app-glow"></div>
      <div class="app-texture"></div>
    </div>

    <div class="app">
      <router-view v-slot="{ Component, route }">
        <transition name="route-float" mode="out-in">
          <div :key="route.fullPath" class="route-stage">
            <template v-if="route.meta.keepAlive">
              <keep-alive>
                <component :is="Component" />
              </keep-alive>
            </template>
            <template v-else>
              <component :is="Component" />
            </template>
          </div>
        </transition>
      </router-view>
    </div>
  </div>
</template>

<script setup>
// App.vue 作为根组件
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Segoe UI', Roboto, Oxygen,
    Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  font-size: 16px;
  background-color: var(--page-bg);
  color: var(--text-primary);
  height: 100%;
  width: 100%;
}

#app {
  min-height: 100%;
}

.app-shell {
  position: relative;
  min-height: 100vh;
  overflow: hidden;
}

.app-background {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
  background: linear-gradient(180deg, var(--page-bg-secondary) 0%, var(--page-bg) 52%, #0b0d0f 100%);
}

.app-glow,
.app-texture {
  position: absolute;
  inset: 0;
}

.app-glow {
  background:
    radial-gradient(circle at top center, rgba(200, 155, 83, 0.09), transparent 28%),
    radial-gradient(circle at 50% 24%, rgba(255, 255, 255, 0.025), transparent 36%);
  animation: ambient-breathe 12s ease-in-out infinite;
}

.app-texture {
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.025), transparent 16%),
    linear-gradient(90deg, rgba(255, 255, 255, 0.015) 1px, transparent 1px),
    linear-gradient(rgba(255, 255, 255, 0.012) 1px, transparent 1px);
  background-size: 100% 100%, 32px 32px, 32px 32px;
  mask-image: linear-gradient(180deg, rgba(255, 255, 255, 0.16), transparent 72%);
  opacity: 0.32;
}

.app {
  position: relative;
  z-index: 1;
  max-width: 750px;
  margin: 0 auto;
  min-height: 100vh;
}

.route-stage {
  position: relative;
  min-height: 100vh;
}

@media screen and (max-width: 750px) {
  html {
    font-size: calc(100vw / 750 * 16);
  }
}
</style>
