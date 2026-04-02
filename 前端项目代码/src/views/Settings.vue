<template>
  <div class="settings-container page-shell">
    <van-nav-bar
      :title="$t('settings.title')"
      left-arrow
      class="settings-nav"
      @click-left="onClickLeft"
    />

    <div class="settings-hero neon-panel">
      <div>
        <div class="settings-hero-label">PREFERENCES</div>
        <h2>{{ $t('settings.title') }}</h2>
        <p>管理主题与语言，让整套阅读体验保持统一、克制和舒适。</p>
      </div>
      <div class="settings-hero-chip">
        <span>{{ currentThemeName }}</span>
      </div>
    </div>

    <div class="settings-list">
      <section class="settings-section neon-panel">
        <div class="section-heading">
          <div>
            <div class="neon-section-title">{{ $t('settings.personalization') }}</div>
            <div class="neon-section-subtitle">切换主题色与界面语言。</div>
          </div>
        </div>

        <button class="settings-entry" type="button" @click="showThemePopup = true">
          <div>
            <div class="entry-title">{{ $t('settings.themeCustomization') }}</div>
            <div class="entry-desc">4 套低饱和深色主题可即时切换</div>
          </div>
          <div class="entry-preview">
            <span class="preview-swatch" :style="{ background: activeThemePreview }"></span>
            <van-icon name="arrow" />
          </div>
        </button>

        <button class="settings-entry" type="button" @click="showLanguagePopup = true">
          <div>
            <div class="entry-title">{{ $t('settings.languageSettings') }}</div>
            <div class="entry-desc">当前语言：{{ currentLanguageLabel }}</div>
          </div>
          <van-icon name="arrow" />
        </button>
      </section>

      <section class="settings-section neon-panel">
        <div class="section-heading">
          <div class="neon-section-title">{{ $t('settings.account') }}</div>
          <div class="neon-section-subtitle">账号与通用信息入口。</div>
        </div>

        <div class="info-entry">{{ $t('settings.privacySettings') }}</div>
        <div class="info-entry">{{ $t('settings.notificationSettings') }}</div>
        <div class="info-entry">{{ $t('settings.aboutUs') }}</div>
      </section>
    </div>

    <van-popup
      v-model:show="showThemePopup"
      position="bottom"
      round
      :style="{ minHeight: '54%' }"
    >
      <div class="popup-wrap">
        <div class="popup-title-row">
          <div>
            <div class="popup-eyebrow">THEMES</div>
            <div class="popup-title">{{ $t('settings.selectTheme') }}</div>
          </div>
        </div>

        <div class="theme-grid">
          <button
            v-for="theme in themeList"
            :key="theme.id"
            class="theme-card"
            :class="{ active: currentTheme === theme.id }"
            type="button"
            @click="changeTheme(theme.id)"
          >
            <div
              class="theme-preview"
              :style="{
                background: `linear-gradient(180deg, ${theme.pageBgSecondary} 0%, ${theme.pageBg} 100%)`
              }"
            >
              <span class="theme-orb" :style="{ background: theme.primaryColor }"></span>
              <span class="theme-orb secondary" :style="{ background: theme.secondaryColor }"></span>
              <span class="theme-line" :style="{ background: theme.lineColor }"></span>
              <span class="theme-mini-pill" :style="{ borderColor: theme.primaryColor }"></span>
            </div>
            <div class="theme-card-footer">
              <span>{{ theme.name }}</span>
              <span v-if="currentTheme === theme.id" class="active-tag">当前</span>
            </div>
          </button>
        </div>
      </div>
    </van-popup>

    <van-popup
      v-model:show="showLanguagePopup"
      position="bottom"
      round
      :style="{ minHeight: '40%' }"
    >
      <div class="popup-wrap">
        <div class="popup-title-row">
          <div>
            <div class="popup-eyebrow">LANGUAGE</div>
            <div class="popup-title">{{ $t('settings.selectLanguage') }}</div>
          </div>
        </div>

        <van-radio-group v-model="currentLanguage" class="language-group">
          <button
            v-for="lang in languageOptions"
            :key="lang.value"
            class="language-card"
            :class="{ active: currentLanguage === lang.value }"
            type="button"
            @click="currentLanguage = lang.value"
          >
            <span>{{ lang.label }}</span>
            <van-radio :name="lang.value" />
          </button>
        </van-radio-group>

        <div class="popup-footer">
          <van-button type="primary" block class="neon-button" @click="changeLanguage">{{ $t('common.confirm') }}</van-button>
        </div>
      </div>
    </van-popup>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { showToast } from 'vant';
import { useThemeStore } from '../store/theme';
import { useI18n } from 'vue-i18n';
import { useLanguageStore } from '../store/language';

const router = useRouter();
const themeStore = useThemeStore();
const languageStore = useLanguageStore();
const { t, locale } = useI18n();

const onClickLeft = () => {
  router.back();
};

const showThemePopup = ref(false);
const themeList = computed(() => themeStore.getAllThemes);
const currentTheme = computed(() => themeStore.getCurrentTheme);
const currentThemeName = computed(() => themeStore.getThemeConfig?.name || '主题');
const activeThemePreview = computed(() => {
  const theme = themeStore.getThemeConfig;
  return `linear-gradient(135deg, ${theme.accentSecondary} 0%, ${theme.accentPrimary} 100%)`;
});

const changeTheme = (themeId) => {
  themeStore.setTheme(themeId);
  showToast(t('settings.themeChanged'));
  showThemePopup.value = false;
};

const showLanguagePopup = ref(false);
const currentLanguage = ref(languageStore.getCurrentLanguage);
const languageOptions = [
  { label: '简体中文', value: 'zh-CN' },
  { label: 'English', value: 'en-US' }
];

const currentLanguageLabel = computed(() => {
  return languageOptions.find((lang) => lang.value === currentLanguage.value)?.label || currentLanguage.value;
});

const changeLanguage = () => {
  languageStore.setLanguage(currentLanguage.value);
  locale.value = currentLanguage.value;
  showLanguagePopup.value = false;
  showToast(t('settings.languageChanged'));
  window.location.reload();
};
</script>

<style scoped>
.page-shell {
  min-height: 100vh;
  padding: 74px 16px 36px;
  color: var(--text-primary);
}

.settings-nav {
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

.settings-hero {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 14px;
  padding: 24px;
  margin-bottom: 18px;
  border-radius: 30px;
}

.settings-hero-label,
.popup-eyebrow {
  margin-bottom: 12px;
  color: var(--accent-primary);
  font-size: 11px;
  letter-spacing: 0.18em;
}

.settings-hero h2 {
  margin: 0 0 10px;
  font-size: 28px;
}

.settings-hero p {
  margin: 0;
  max-width: 440px;
  color: var(--text-secondary);
  font-size: 14px;
  line-height: 1.8;
}

.settings-hero-chip {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 14px;
  border-radius: 999px;
  background: var(--accent-soft);
  color: var(--accent-primary);
  white-space: nowrap;
}

.settings-list {
  display: grid;
  gap: 16px;
}

.settings-section {
  padding: 18px;
  border-radius: 28px;
}

.section-heading {
  margin-bottom: 14px;
}

.settings-entry,
.info-entry,
.language-card {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 15px 16px;
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06);
  color: var(--text-primary);
}

.settings-entry + .settings-entry,
.info-entry + .info-entry {
  margin-top: 12px;
}

.entry-title {
  font-size: 15px;
  font-weight: 600;
}

.entry-desc {
  margin-top: 4px;
  font-size: 12px;
  color: var(--text-muted);
}

.entry-preview {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.preview-swatch {
  width: 28px;
  height: 28px;
  border-radius: 999px;
  box-shadow: none;
}

.popup-wrap {
  padding: 22px 18px 24px;
}

.popup-title-row {
  margin-bottom: 18px;
}

.popup-title {
  font-size: 22px;
  font-weight: 600;
  color: var(--text-primary);
}

.theme-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
}

.theme-card {
  padding: 10px;
  border-radius: 22px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  background: rgba(255, 255, 255, 0.03);
  color: var(--text-primary);
  text-align: left;
}

.theme-card.active {
  border-color: var(--border-strong);
  box-shadow: var(--shadow-glow);
}

.theme-preview {
  position: relative;
  height: 110px;
  border-radius: 18px;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.theme-orb,
.theme-line,
.theme-mini-pill {
  position: absolute;
}

.theme-orb {
  top: 18px;
  left: 14px;
  width: 52px;
  height: 52px;
  border-radius: 50%;
  filter: blur(10px);
  opacity: 0.72;
}

.theme-orb.secondary {
  top: auto;
  left: auto;
  right: 10px;
  bottom: 16px;
  width: 44px;
  height: 44px;
}

.theme-line {
  left: -8px;
  right: -8px;
  top: 52%;
  height: 2px;
  opacity: 0.55;
  transform: rotate(-10deg);
}

.theme-mini-pill {
  right: 14px;
  top: 18px;
  width: 36px;
  height: 14px;
  border-radius: 999px;
  border: 1px solid;
}

.theme-card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 10px;
  font-size: 13px;
}

.active-tag {
  padding: 4px 8px;
  border-radius: 999px;
  background: var(--accent-soft);
  color: var(--accent-primary);
  font-size: 11px;
}

.language-group {
  display: grid;
  gap: 12px;
}

.language-card.active {
  border-color: var(--border-strong);
  box-shadow: var(--shadow-glow);
}

.popup-footer {
  margin-top: 18px;
}

@media (max-width: 520px) {
  .settings-hero {
    flex-direction: column;
    align-items: flex-start;
  }

  .settings-hero-chip {
    white-space: normal;
  }

  .theme-grid {
    grid-template-columns: 1fr;
  }
}
</style>
