<template>
  <div class="news-detail">
    <van-nav-bar
      title="新闻详情"
      left-text="返回"
      left-arrow
      @click-left="onClickLeft"
      fixed
      class="detail-nav"
    />

    <div class="detail-content" v-if="newsStore.newsDetail.id">
      <header class="article-header neon-panel">
        <div class="article-kicker">FEATURE STORY</div>
        <div class="title-container">
          <h1 class="title">{{ newsStore.newsDetail.title }}</h1>
          <van-button
            class="favorite-btn"
            :icon="isFavorite ? 'star' : 'star-o'"
            :class="{ 'is-favorite': isFavorite }"
            @click="toggleFavorite"
          />
        </div>

        <div class="info">
          <span>{{ newsStore.newsDetail.author }}</span>
          <span>{{ newsStore.newsDetail.publishTime }}</span>
          <span>{{ newsStore.newsDetail.views }} 阅读</span>
        </div>
      </header>

      <div class="cover" v-if="newsStore.newsDetail.image">
        <img :src="newsStore.newsDetail.image" :alt="newsStore.newsDetail.title">
      </div>

      <article class="content neon-panel-strong">
        <p v-for="(paragraph, index) in contentParagraphs" :key="index">
          {{ paragraph }}
        </p>
      </article>

      <section class="related-news neon-panel" v-if="newsStore.newsDetail.relatedNews?.length">
        <div class="related-heading">
          <h3>继续阅读</h3>
          <span>相关推荐</span>
        </div>
        <div class="related-list">
          <div
            class="related-item"
            v-for="item in newsStore.newsDetail.relatedNews"
            :key="item.id"
            @click="goToRelatedNews(item.id)"
          >
            <div class="related-image">
              <img :src="item.image" :alt="item.title">
            </div>
            <div class="related-copy">
              <div class="related-title">{{ item.title }}</div>
            </div>
          </div>
        </div>
      </section>
    </div>

    <van-empty v-else description="加载中..." />
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useNewsStore } from '../store/modules/news'
import { useHistoryStore } from '../store/modules/history'
import { useFavoriteStore } from '../store/modules/favorite'
import { useUserStore } from '../store/user'
import { showToast } from 'vant'

const route = useRoute()
const router = useRouter()
const newsStore = useNewsStore()
const historyStore = useHistoryStore()
const favoriteStore = useFavoriteStore()
const userStore = useUserStore()

const newsId = computed(() => Number(route.params.id))

const contentParagraphs = computed(() => {
  if (!newsStore.newsDetail.content) return []
  return newsStore.newsDetail.content.split('\n\n').filter(p => p.trim())
})

const onClickLeft = () => {
  router.back()
}

const goToRelatedNews = (id) => {
  router.push(`/news/detail/${id}`)
}

const isFavorite = computed(() => {
  return favoriteStore.isFavorite(newsId.value)
})

const toggleFavorite = async () => {
  if (!userStore.getLoginStatus) {
    showToast({
      message: '请先登录后再收藏',
      position: 'bottom',
    })
    router.push('/login')
    return
  }

  const status = await favoriteStore.toggleFavorite(newsStore.newsDetail)

  if (status === true) {
    showToast({
      message: '已添加到收藏',
      position: 'bottom',
    })
  } else if (status === false) {
    showToast({
      message: '已取消收藏',
      position: 'bottom',
    })
  } else {
    showToast({
      message: '操作失败，请稍后重试',
      position: 'bottom',
    })
  }
}

onMounted(async () => {
  await newsStore.getNewsDetail(newsId.value)

  if (newsStore.newsDetail.id) {
    if (userStore.getLoginStatus) {
      try {
        const result = await historyStore.addHistoryApi(newsStore.newsDetail.id)
        console.log('记录浏览历史API结果:', result)
      } catch (error) {
        console.error('记录浏览历史API失败:', error)
      }
    }
  }

  favoriteStore.loadFavorites()

  if (userStore.getLoginStatus && newsStore.newsDetail.id) {
    const result = await favoriteStore.checkFavoriteStatusApi(newsStore.newsDetail.id)
    if (result.success && !result.isLocal) {
      if (result.isFavorite && !favoriteStore.isFavorite(newsStore.newsDetail.id)) {
        favoriteStore.addFavorite(newsStore.newsDetail)
      } else if (!result.isFavorite && favoriteStore.isFavorite(newsStore.newsDetail.id)) {
        favoriteStore.removeFavorite(newsStore.newsDetail.id)
      }
    }
  }
})
</script>

<style scoped>
.news-detail {
  min-height: 100vh;
  padding: 70px 16px 48px;
  background: transparent;
}

.detail-nav {
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

.detail-content {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.article-header {
  padding: 24px;
  border-radius: 30px;
}

.article-kicker {
  margin-bottom: 14px;
  color: var(--accent-primary);
  font-size: 11px;
  letter-spacing: 0.18em;
}

.title-container {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 14px;
  margin-bottom: 14px;
}

.title {
  font-size: 31px;
  font-weight: 700;
  line-height: 1.2;
  margin: 0;
  flex: 1;
  letter-spacing: -0.02em;
}

.favorite-btn {
  flex-shrink: 0;
  padding: 0;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 1px solid var(--button-ghost-border);
  background: rgba(255, 255, 255, 0.03);
  color: var(--text-secondary);
}

.favorite-btn.is-favorite {
  color: var(--accent-primary);
}

.info {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  font-size: 12px;
  color: var(--text-muted);
}

.cover {
  overflow: hidden;
  border-radius: 30px;
  box-shadow: var(--shadow-soft);
}

.cover img {
  width: 100%;
  display: block;
  aspect-ratio: 16 / 10;
  object-fit: cover;
}

.content {
  padding: 28px 24px;
  border-radius: 30px;
}

.content p {
  margin: 0 0 20px;
  font-size: 16px;
  line-height: 2;
  color: var(--text-secondary);
  text-align: justify;
}

.content p:last-child {
  margin-bottom: 0;
}

.related-news {
  padding: 24px;
  border-radius: 30px;
}

.related-heading {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  margin-bottom: 18px;
}

.related-heading h3 {
  margin: 0;
  font-size: 20px;
}

.related-heading span {
  font-size: 12px;
  color: var(--text-muted);
}

.related-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.related-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 12px;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.025);
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.related-image {
  width: 92px;
  height: 68px;
  flex-shrink: 0;
  overflow: hidden;
  border-radius: 16px;
}

.related-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.related-copy {
  flex: 1;
}

.related-title {
  font-size: 15px;
  line-height: 1.6;
  color: var(--text-primary);
}

@media (max-width: 520px) {
  .title {
    font-size: 27px;
  }

  .content {
    padding: 24px 20px;
  }

  .content p {
    font-size: 15px;
    line-height: 1.9;
  }
}
</style>
