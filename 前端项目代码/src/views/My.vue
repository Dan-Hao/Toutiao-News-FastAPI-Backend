<template>
  <div class="my-container page-shell">
    <van-nav-bar :title="$t('my.title')" fixed class="my-nav" />

    <div class="user-info neon-panel" @click="goToProfile" v-if="isLogin">
      <div class="avatar-shell">
        <van-image
          round
          width="80"
          height="80"
          src="https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg"
        />
      </div>
      <div class="info">
        <div class="eyebrow">PROFILE</div>
        <div class="username">{{ isLogin ? userInfo.username : $t('my.notLoggedIn') }}</div>
        <div class="desc">{{ userBio || $t('profile.bio') }}</div>
      </div>
      <van-icon name="arrow" class="arrow-icon" />
    </div>

    <div class="user-info neon-panel" v-else>
      <div class="avatar-shell">
        <van-image
          round
          width="80"
          height="80"
          src="https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg"
        />
      </div>
      <div class="info">
        <div class="eyebrow">PROFILE</div>
        <div class="username">{{ $t('my.notLoggedIn') }}</div>
        <div class="action-row">
          <van-button type="primary" size="small" class="neon-button" @click="goToLogin">{{ $t('my.goToLogin') }}</van-button>
          <van-button type="default" size="small" class="neon-ghost-button" @click="goToRegister">{{ $t('my.goToRegister') }}</van-button>
        </div>
      </div>
    </div>

    <div class="menu-list neon-panel">
      <div class="menu-title">
        <div class="neon-section-title">PERSONAL HUB</div>
        <div class="neon-section-subtitle">常用功能和账号入口。</div>
      </div>

      <button class="menu-entry" type="button" @click="goToFavorite">
        <span>{{ $t('my.myFavorite') }}</span>
        <van-icon name="arrow" />
      </button>
      <button class="menu-entry" type="button" @click="goToHistory">
        <span>{{ $t('my.browsingHistory') }}</span>
        <van-icon name="arrow" />
      </button>
      <div class="menu-entry static-entry">
        <span>{{ $t('my.notifications') }}</span>
      </div>
      <button class="menu-entry" type="button" @click="goToSettings">
        <span>{{ $t('my.settings') }}</span>
        <van-icon name="arrow" />
      </button>
      <button v-if="isLogin" class="menu-entry logout-entry" type="button" @click="handleLogout">
        <span>{{ $t('my.logout') }}</span>
      </button>
    </div>

    <tab-bar />
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useUserStore } from '../store/user';
import { useRouter } from 'vue-router';
import { computed } from 'vue';
import { showDialog, showToast } from 'vant';
import TabBar from '../components/TabBar.vue';
import { useI18n } from 'vue-i18n';

const userStore = useUserStore();
const router = useRouter();
const { t } = useI18n();

const userInfo = computed(() => userStore.userInfo);
const isLogin = computed(() => userStore.getLoginStatus);
const userBio = computed(() => userStore.getUserBio || t('profile.bio'));

const goToLogin = () => {
  router.push('/login');
};

const goToRegister = () => {
  router.push('/register');
};

const goToProfile = () => {
  if (isLogin.value) {
    router.push('/profile');
  }
};

const goToHistory = () => {
  if (isLogin.value) {
    router.push('/history');
  } else {
    showToast(t('common.login'));
    router.push('/login');
  }
};

const goToFavorite = () => {
  if (isLogin.value) {
    router.push('/favorite');
  } else {
    showToast(t('common.login'));
    router.push('/login');
  }
};

const goToSettings = () => {
  router.push('/settings');
};

const handleLogout = () => {
  showDialog({
    title: t('common.confirm'),
    message: t('my.logout') + '?',
    showCancelButton: true,
  }).then((action) => {
    if (action === 'confirm') {
      userStore.logout();
      router.push('/login');
    }
  });
};

onMounted(async () => {
  try {
    await userStore.getUserInfoDetail();
  } catch (error) {
    console.error('获取用户信息失败:', error);
  }
});
</script>

<style scoped>
.page-shell {
  min-height: 100vh;
  padding: 74px 16px 118px;
  color: var(--text-primary);
  box-sizing: border-box;
}

.my-nav {
  width: min(calc(100% - 32px), 718px);
  left: 50%;
  transform: translateX(-50%);
  top: 12px;
  border-radius: 24px;
  overflow: hidden;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.045), rgba(255, 255, 255, 0.015)), var(--nav-background);
  border: 1px solid var(--nav-border);
  box-shadow: var(--shadow-soft);
  backdrop-filter: blur(var(--backdrop-blur));
  -webkit-backdrop-filter: blur(var(--backdrop-blur));
}

.user-info {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 24px;
  border-radius: 30px;
  margin-bottom: 16px;
  position: relative;
}

.arrow-icon {
  color: var(--text-secondary);
}

.avatar-shell {
  padding: 4px;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.08), rgba(200, 155, 83, 0.35));
  box-shadow: var(--shadow-glow);
}

.info {
  flex: 1;
}

.eyebrow {
  margin-bottom: 8px;
  color: var(--accent-primary);
  font-size: 11px;
  letter-spacing: 0.16em;
}

.username {
  font-size: 22px;
  font-weight: 700;
  margin-bottom: 8px;
}

.desc {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.7;
}

.action-row {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 12px;
}

.menu-list {
  padding: 18px;
  border-radius: 28px;
}

.menu-title {
  margin-bottom: 12px;
}

.menu-entry {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px;
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06);
  color: var(--text-primary);
}

.menu-entry + .menu-entry {
  margin-top: 12px;
}

.static-entry {
  color: var(--text-secondary);
}

.logout-entry {
  justify-content: center;
  color: #d58b7f;
}
</style>
