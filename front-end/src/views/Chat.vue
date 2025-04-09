<template>
  <div class="chat-container">
    <div class="chat-messages" ref="messageContainer">
      <div v-for="message in messages" :key="message.id" :class="['message', message.type]">
        <div class="message-content">
          <p>{{ message.content }}</p>
          <span class="message-time">{{ formatTime(message.timestamp) }}</span>
        </div>
      </div>
    </div>
    <div class="chat-input">
      <form @submit.prevent="sendMessage">
        <textarea
          v-model="newMessage"
          placeholder="输入消息..."
          @keydown.enter.prevent="sendMessage"
          :disabled="loading"
        ></textarea>
        <button type="submit" :disabled="loading || !newMessage.trim()">
          {{ loading ? '发送中...' : '发送' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import axiosInstance from '../utils/axios';

export default {
  name: 'ChatView',
  data() {
    return {
      messages: [],
      newMessage: '',
      loading: false,
      page: 1,
      pageSize: 20
    };
  },
  methods: {
    async loadMessages() {
      try {
        const response = await axiosInstance.get(`/chat/history?page=${this.page}&limit=${this.pageSize}`);
        this.messages = [...response.data].reverse();
        this.scrollToBottom();
      } catch (error) {
        console.error('加载消息失败:', error);
        this.$message.error(error.response?.data?.detail || '加载消息失败，请重试');
      }
    },
    async sendMessage() {
      if (!this.newMessage.trim() || this.loading) return;

      this.loading = true;
      try {
        const response = await axiosInstance.post('/chat/send', {
          message: this.newMessage.trim()
        }, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });

        this.messages.push({
          id: response.data.id,
          content: this.newMessage,
          type: 'user',
          timestamp: new Date()
        });

        // 添加系统回复
        if (response.data.response) {
          this.messages.push({
            id: response.data.id + '-response',
            content: response.data.response,
            type: 'system',
            timestamp: new Date()
          });
        }

        this.newMessage = '';
        this.scrollToBottom();
      } catch (error) {
        console.error('发送消息失败:', error);
      } finally {
        this.loading = false;
      }
    },
    scrollToBottom() {
      this.$nextTick(() => {
        const container = this.$refs.messageContainer;
        container.scrollTop = container.scrollHeight;
      });
    },
    formatTime(timestamp) {
      const date = new Date(timestamp);
      return date.toLocaleTimeString('zh-CN', {
        hour: '2-digit',
        minute: '2-digit'
      });
    }
  },
  created() {
    this.loadMessages();
  },
  mounted() {
    // 检查登录状态
    const token = localStorage.getItem('token');
    if (!token) {
      this.$router.push('/login');
    }
  }
};
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #f5f5f5;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
}

.message {
  margin-bottom: 1rem;
  display: flex;
}

.message.user {
  justify-content: flex-end;
}

.message-content {
  max-width: 70%;
  padding: 0.75rem 1rem;
  border-radius: 1rem;
  position: relative;
}

.user .message-content {
  background-color: #4CAF50;
  color: white;
  border-bottom-right-radius: 0.25rem;
}

.system .message-content {
  background-color: white;
  color: #333;
  border-bottom-left-radius: 0.25rem;
}

.message-time {
  font-size: 0.75rem;
  color: #666;
  margin-top: 0.25rem;
  display: block;
}

.user .message-time {
  color: rgba(255, 255, 255, 0.8);
}

.chat-input {
  padding: 1rem;
  background-color: white;
  border-top: 1px solid #ddd;
}

form {
  display: flex;
  gap: 1rem;
}

textarea {
  flex: 1;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  resize: none;
  height: 60px;
  font-size: 1rem;
}

textarea:focus {
  outline: none;
  border-color: #4CAF50;
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
}

button {
  padding: 0 1.5rem;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover:not(:disabled) {
  background-color: #45a049;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}
</style>