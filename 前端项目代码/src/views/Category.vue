<template>
  <div class="category page-shell">
    <van-nav-bar
      :title="$t('common.allCategories')"
      :left-text="$t('common.back')"
      left-arrow
      fixed
      class="category-nav"
      @click-left="onClickLeft"
    />

    <div class="category-hero neon-panel">
      <div>
        <div class="category-eyebrow">CHANNEL INDEX</div>
        <h2>{{ $t('common.allCategories') }}</h2>
        <p>按主题浏览新闻内容，用更安静的层次组织你的阅读入口。</p>
      </div>
    </div>

    <div class="category-container neon-panel-strong">
      <van-grid :column-num="3" :border="false" gutter="12">
        <van-grid-item
          v-for="category in displayCategories"
          :key="category.id"
          class="category-grid-item"
          :text="getCategoryTranslation(category.name)"
          icon="newspaper-o"
          @click="goToCategoryNews(category.id)"
        />
      </van-grid>
    </div>

    <tab-bar />
  </div>
</template>

<script setup>
import { useNewsStore } from '../store/modules/news'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import TabBar from '../components/TabBar.vue'
import { computed } from 'vue'

const newsStore = useNewsStore()
const router = useRouter()
const { t } = useI18n()

const displayCategories = computed(() => {
  return newsStore.categories.filter(category => category.name !== '更多')
})

const onClickLeft = () => {
  router.back()
}

const goToCategoryNews = (categoryId) => {
  newsStore.changeCategory(categoryId)

  router.push({
    path: '/home',
    query: { categoryId: categoryId }
  })
}

const getCategoryTranslation = (categoryName) => {
  const categoryMap = {
    '头条': 'headline',
    '社会': 'society',
    '国内': 'domestic',
    '国际': 'international',
    '娱乐': 'entertainment',
    '体育': 'sports',
    '军事': 'military',
    '科技': 'technology',
    '财经': 'finance',
    '更多': 'more'
  }

  const key = categoryMap[categoryName]
  return key ? t(`home.categories.${key}`) : categoryName
}
</script>

<style scoped>
.page-shell {
  min-height: 100vh;
  padding: 74px 16px 118px;
  color: var(--text-primary);
}

.category-nav {
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

.category-hero {
  padding: 24px;
  border-radius: 30px;
  margin-bottom: 18px;
}

.category-eyebrow {
  margin-bottom: 12px;
  color: var(--accent-primary);
  font-size: 11px;
  letter-spacing: 0.18em;
}

.category-hero h2 {
  margin: 0 0 10px;
  font-size: 28px;
  line-height: 1.2;
}

.category-hero p {
  margin: 0;
  color: var(--text-secondary);
  font-size: 14px;
  line-height: 1.8;
}

.category-container {
  padding: 18px;
  border-radius: 30px;
}

:deep(.van-grid-item__content) {
  min-height: 108px;
  border-radius: 22px;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.035), rgba(255, 255, 255, 0.015)), var(--surface-base);
  border: 1px solid rgba(255, 255, 255, 0.06);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.025);
  color: var(--text-primary);
  transition: transform var(--duration-fast) ease, border-color var(--duration-fast) ease, background-color var(--duration-fast) ease;
}

:deep(.van-grid-item__content:active) {
  transform: translateY(1px);
}

:deep(.van-grid-item__icon) {
  font-size: 28px;
  color: var(--accent-primary);
}

:deep(.van-grid-item__text) {
  margin-top: 10px;
  color: var(--text-secondary);
  font-size: 13px;
}
</style>
