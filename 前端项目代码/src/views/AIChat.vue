<template>
  <div class="ai-chat-container page-shell">
    <van-nav-bar title="AI问答" fixed class="chat-nav" />

    <div class="chat-hero neon-panel">
      <div>
        <div class="chat-eyebrow">EDITORIAL AI DESK</div>
        <h2>AI 问答</h2>
        <p>在统一的深色阅读界面中进行提问，让对话区也保持沉静、清晰、易读。</p>
      </div>
    </div>

    <div class="chat-content neon-panel-strong">
      <div class="messages-container" ref="messagesContainer">
        <div
          v-for="(message, index) in messages"
          :key="index"
          :class="['message', message.role === 'user' ? 'user-message' : 'ai-message']"
        >
          <div class="message-content">
            <div v-if="message.role === 'assistant' && message.content === ''" class="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
            <div v-else v-html="formatMessage(message.content)"></div>
          </div>
        </div>
      </div>

      <div class="input-container">
        <van-field
          v-model="userInput"
          rows="1"
          autosize
          type="textarea"
          placeholder="请输入问题..."
          class="chat-input"
          @keypress.enter.prevent="sendMessage"
        />
        <van-button
          type="primary"
          class="send-button neon-button"
          :disabled="isLoading || !userInput.trim()"
          @click="sendMessage"
        >
          发送
        </van-button>
      </div>
    </div>

    <tab-bar />
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch } from 'vue';
import TabBar from '../components/TabBar.vue';
import { showToast } from 'vant';
import * as marked from 'marked';
import DOMPurify from 'dompurify';
import { aiChatConfig } from '../config/api';

const messages = ref([
  { role: 'assistant', content: '你好！我是AI助手，有什么可以帮助你的吗？' }
]);
const userInput = ref('');
const messagesContainer = ref(null);
const isLoading = ref(false);

const apiEndpoint = ref(aiChatConfig.apiEndpoint);
const apiKey = ref(aiChatConfig.apiKey);
const model = ref(aiChatConfig.model);

const formatMessage = (content) => {
  if (!content) return '';
  return DOMPurify.sanitize(marked.parse(content));
};

const sendMessage = async () => {
  if (!userInput.value.trim() || isLoading.value) return;

  if (!apiKey.value || apiKey.value === 'your-api-key-here') {
    showToast('API Key未配置，请联系管理员');
    return;
  }

  const userMessage = userInput.value.trim();
  messages.value.push({ role: 'user', content: userMessage });
  userInput.value = '';
  messages.value.push({ role: 'assistant', content: '' });

  await nextTick();
  scrollToBottom();

  isLoading.value = true;
  try {
    await fetchAIResponse(userMessage);
  } catch (error) {
    console.error('Error fetching AI response:', error);
    messages.value[messages.value.length - 1].content = `发生错误: ${error.message || '请检查网络连接和API设置'}`;
  } finally {
    isLoading.value = false;
    await nextTick();
    scrollToBottom();
  }
};

const fetchAIResponse = async (userMessage) => {
  const allMessages = messages.value
    .slice(0, -1)
    .map(msg => ({ role: msg.role, content: msg.content }));

  try {
    const response = await fetch(apiEndpoint.value, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey.value}`,
        'X-DashScope-SSE': 'enable'
      },
      body: JSON.stringify({
        model: model.value,
        messages: allMessages,
        stream: true
      })
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.error?.message || `HTTP error! status: ${response.status}`);
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';
    let aiResponse = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n');
      buffer = lines.pop() || '';

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = line.slice(6);
          if (data === '[DONE]') continue;

          try {
            const json = JSON.parse(data);
            const content = json.choices?.[0]?.delta?.content ||
                           json.output?.text ||
                           json.choices?.[0]?.message?.content || '';
            if (content) {
              aiResponse += content;
              messages.value[messages.value.length - 1].content = aiResponse;
              await nextTick();
              scrollToBottom();
            }
          } catch (e) {
            console.error('Error parsing SSE data:', e);
          }
        }
      }
    }

    if (!aiResponse) {
      messages.value[messages.value.length - 1].content = '抱歉，我无法生成回复。请检查API设置或稍后再试。';
    }
  } catch (error) {
    console.error('Fetch error:', error);
    throw error;
  }
};

const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
  }
};

watch(messages, () => {
  nextTick(scrollToBottom);
}, { deep: true });

onMounted(() => {
  scrollToBottom();
});
</script>

<style scoped>
.page-shell {
  min-height: 100vh;
  padding: 74px 16px 118px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  color: var(--text-primary);
  box-sizing: border-box;
}

.chat-nav {
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

.chat-hero {
  padding: 24px;
  border-radius: 30px;
}

.chat-eyebrow {
  margin-bottom: 12px;
  color: var(--accent-primary);
  font-size: 11px;
  letter-spacing: 0.18em;
}

.chat-hero h2 {
  margin: 0 0 10px;
  font-size: 28px;
}

.chat-hero p {
  margin: 0;
  color: var(--text-secondary);
  font-size: 14px;
  line-height: 1.8;
}

.chat-content {
  flex: 1;
  min-height: 0;
  display: flex;
  flex-direction: column;
  padding: 16px;
  border-radius: 30px;
  overflow: hidden;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 4px 2px 18px;
}

.message {
  margin-bottom: 14px;
  max-width: 88%;
}

.user-message {
  margin-left: auto;
}

.ai-message {
  margin-right: auto;
}

.message-content {
  padding: 15px 16px;
  border-radius: 22px;
  word-break: break-word;
  line-height: 1.8;
}

.user-message .message-content {
  background: var(--button-primary-bg);
  color: var(--button-primary-text);
  box-shadow: var(--shadow-glow);
}

.ai-message .message-content {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.05);
  color: var(--text-primary);
}

.input-container {
  display: flex;
  gap: 10px;
  padding-top: 14px;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.chat-input {
  flex: 1;
  border-radius: 18px;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06);
}

:deep(.chat-input .van-field__control) {
  color: var(--text-primary);
}

:deep(.chat-input .van-field__control::placeholder) {
  color: var(--text-muted);
}

.send-button {
  align-self: flex-end;
  border-radius: 16px;
}

.message-content pre,
:deep(pre) {
  background-color: rgba(255, 255, 255, 0.05);
  padding: 10px;
  border-radius: 12px;
  overflow-x: auto;
}

.message-content code,
:deep(code) {
  font-family: monospace;
  background-color: rgba(255, 255, 255, 0.05);
  padding: 2px 4px;
  border-radius: 6px;
}

.message-content img {
  max-width: 100%;
}

.typing-indicator {
  display: flex;
  padding: 5px;
}

.typing-indicator span {
  height: 7px;
  width: 7px;
  background-color: var(--accent-primary);
  border-radius: 50%;
  margin: 0 2px;
  display: inline-block;
  animation: bounce 1.5s infinite ease-in-out;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes bounce {
  0%, 60%, 100% {
    transform: translateY(0);
  }
  30% {
    transform: translateY(-4px);
  }
}

:deep(p) {
  margin: 8px 0;
}

:deep(ul), :deep(ol) {
  padding-left: 20px;
}

:deep(a) {
  color: var(--accent-primary);
  text-decoration: none;
}
</style>
