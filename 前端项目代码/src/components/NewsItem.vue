<template>
  <div class="news-item neon-panel neon-floating click-effect" @click="goToDetail">
    <div class="news-meta-flag">
      <span class="news-channel">{{ news.author }}</span>
    </div>

    <div class="news-main">
      <div class="news-content">
        <h3 class="news-title">{{ news.title }}</h3>
        <p class="news-desc">{{ news.description }}</p>
        <div class="news-info">
          <span>{{ news.publishTime }}</span>
          <span>{{ news.views }} 阅读</span>
        </div>
      </div>

      <div class="news-image">
        <img :src="news.image" :alt="news.title">
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  news: {
    type: Object,
    required: true
  }
})

const router = useRouter()

const goToDetail = () => {
  router.push(`/news/detail/${props.news.id}`)
}
</script>

<style scoped>
.news-item {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin: 0 16px 16px;
  padding: 20px;
  border-radius: 26px;
  cursor: pointer;
}

.news-main {
  display: flex;
  align-items: stretch;
  gap: 16px;
}

.news-meta-flag {
  display: inline-flex;
  align-items: center;
  width: fit-content;
  padding: 6px 12px;
  border-radius: 999px;
  background: var(--accent-soft);
  color: var(--accent-primary);
  font-size: 11px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.news-channel {
  white-space: nowrap;
}

.news-content {
  flex: 1;
  overflow: hidden;
}

.news-title {
  font-size: 19px;
  font-weight: 600;
  margin: 0 0 12px;
  line-height: 1.45;
  color: var(--text-primary);
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.news-desc {
  font-size: 13px;
  color: var(--text-secondary);
  margin: 0 0 16px;
  line-height: 1.75;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}

.news-info {
  font-size: 12px;
  color: var(--text-muted);
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.news-image {
  width: 118px;
  height: 104px;
  flex-shrink: 0;
  border-radius: 20px;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.03);
  box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.04);
}

.news-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

@media (max-width: 420px) {
  .news-item {
    padding: 18px;
  }

  .news-title {
    font-size: 18px;
  }

  .news-image {
    width: 104px;
    height: 96px;
  }
}
</style>
