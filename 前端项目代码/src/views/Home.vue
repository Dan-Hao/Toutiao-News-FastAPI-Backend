<template>
  <div class="home page-shell">
    <div class="home-top-stack">
      <van-nav-bar :title="$t('home.title')" fixed class="home-nav" />

      <div class="home-intro neon-panel">
        <div>
          <div class="home-intro-label">EDITOR'S SELECTION</div>
          <h2>{{ $t('home.title') }}</h2>
          <p>以更沉静的版式整理热点内容，让浏览接近阅读杂志封面的节奏。</p>
        </div>
        <button class="home-more neon-floating" type="button" @click="goToCategory">
          <span>浏览栏目</span>
          <van-icon name="arrow" />
        </button>
      </div>
    </div>

    <div class="category-tabs neon-panel-strong">
      <van-tabs v-model:active="activeTab" sticky swipeable animated offset-top="154">
        <van-tab
          v-for="category in displayCategories"
          :key="category.id"
          :title="getCategoryTranslation(category.name)"
          @click="newsStore.changeCategory(category.id)"
        >
          <van-pull-refresh v-model="newsStore.refreshing" @refresh="onRefresh">
            <van-list
              v-model:loading="newsStore.loading"
              :finished="newsStore.finished"
              :finished-text="$t('home.noMore')"
              @load="onLoad"
            >
              <div class="feed-space"></div>
              <news-item
                v-for="item in newsStore.newsList"
                :key="item.id"
                :news="item"
              />
              <div class="feed-bottom-space"></div>
            </van-list>
          </van-pull-refresh>
        </van-tab>
      </van-tabs>
    </div>

    <tab-bar />
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { useNewsStore } from '../store/modules/news'
import { useRouter, useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import NewsItem from '../components/NewsItem.vue'
import TabBar from '../components/TabBar.vue'

const newsStore = useNewsStore()
const router = useRouter()
const route = useRoute()
const { t } = useI18n()
const activeTab = ref(0)

watch(
  () => route.query.categoryId,
  (newCategoryId) => {
    if (newCategoryId) {
      const categoryId = parseInt(newCategoryId)
      const filteredCategories = newsStore.categories.filter(category => category.name !== '更多')
      const index = filteredCategories.findIndex(cat => cat.id === categoryId)

      if (index !== -1) {
        activeTab.value = index
        newsStore.changeCategory(categoryId)
      }
    }
  },
  { immediate: true }
)

onMounted(() => {
  newsStore.getCategories().then(() => {
    newsStore.getNewsList()
  })
})

const displayCategories = computed(() => {
  return newsStore.categories.filter(category => category.name !== '更多')
})

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

const goToCategory = () => {
  router.push('/category')
}

watch(activeTab, (newVal) => {
  if (newsStore.categories[newVal]) {
    const categoryId = newsStore.categories[newVal].id
    newsStore.changeCategory(categoryId)
  }
})

const onRefresh = () => {
  newsStore.getNewsList(true)
}

const onLoad = () => {
  newsStore.getNewsList()
}
</script>

<style scoped>
.page-shell {
  min-height: 100vh;
  padding: 74px 0 118px;
  color: var(--text-primary);
}

.home-top-stack {
  padding: 0 16px 20px;
}

.home-nav {
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

.home-intro {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 18px;
  padding: 24px;
  border-radius: 30px;
}

.home-intro-label {
  margin-bottom: 12px;
  color: var(--accent-primary);
  font-size: 11px;
  letter-spacing: 0.18em;
}

.home-intro h2 {
  margin: 0 0 10px;
  font-size: 30px;
  line-height: 1.15;
}

.home-intro p {
  margin: 0;
  max-width: 430px;
  color: var(--text-secondary);
  font-size: 14px;
  line-height: 1.8;
}

.home-more {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 12px 18px;
  border: 1px solid var(--button-ghost-border);
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.03);
  color: var(--text-primary);
}

.category-tabs {
  margin: 0 16px;
  padding: 10px 10px 0;
  border-radius: 30px;
}

:deep(.van-sticky) {
  z-index: 100;
}

:deep(.van-tabs__wrap) {
  margin-bottom: 10px;
  border-radius: 18px;
}

:deep(.van-tabs__nav) {
  background: transparent;
}

:deep(.van-tab) {
  font-size: 13px;
  letter-spacing: 0.02em;
}

:deep(.van-tab--active) {
  font-weight: 700;
}

:deep(.van-tabs__content) {
  min-height: calc(100vh - 260px);
}

:deep(.van-pull-refresh__track) {
  min-height: calc(100vh - 260px);
}

.feed-space {
  height: 10px;
}

.feed-bottom-space {
  height: 102px;
}

@media (max-width: 520px) {
  .home-intro {
    flex-direction: column;
    align-items: flex-start;
  }

  .home-more {
    width: 100%;
    justify-content: center;
  }
}
</style>
