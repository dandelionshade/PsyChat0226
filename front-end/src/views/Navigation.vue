<template>
  <div class="navigation-container">
    <div class="navigation-header">
      <h2>心理健康资源导航</h2>
      <button @click="showAddForm = true" v-if="isAdmin">添加导航</button>
    </div>

    <!-- 添加导航表单 -->
    <div class="navigation-form" v-if="showAddForm">
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="title">标题</label>
          <input
            type="text"
            id="title"
            v-model="form.title"
            required
            placeholder="请输入标题"
            minlength="2"
            maxlength="50"
          />
        </div>
        <div class="form-group">
          <label for="description">描述</label>
          <textarea
            id="description"
            v-model="form.description"
            placeholder="请输入描述"
            maxlength="200"
          ></textarea>
        </div>
        <div class="form-group">
          <label for="url">链接</label>
          <input
            type="url"
            id="url"
            v-model="form.url"
            required
            placeholder="请输入链接地址"
          />
        </div>
        <div class="form-actions">
          <button type="submit" :disabled="loading">{{ loading ? '提交中...' : '提交' }}</button>
          <button type="button" @click="cancelAdd" class="cancel-button">取消</button>
        </div>
      </form>
    </div>

    <!-- 导航列表 -->
    <div v-if="loading && navigationItems.length === 0" class="loading-container">
      <p>加载中...</p>
    </div>
    <div v-else-if="navigationItems.length === 0" class="empty-container">
      <p>暂无导航内容</p>
    </div>
    <div v-else class="navigation-list">
      <div v-for="item in navigationItems" :key="item.id" class="navigation-item">
        <div class="navigation-content">
          <h3>{{ item.title }}</h3>
          <p>{{ item.description || '暂无描述' }}</p>
          <a :href="item.url" target="_blank" rel="noopener noreferrer" @click.prevent="visitLink(item.url)">访问链接</a>
        </div>
        <div class="navigation-actions" v-if="canEdit(item)">
          <button @click="editItem(item)" class="edit-button">编辑</button>
          <button @click="deleteItem(item.id)" class="delete-button" :disabled="loadingItems.has(item.id)">
            {{ loadingItems.has(item.id) ? '删除中...' : '删除' }}
          </button>
        </div>
      </div>
    </div>

    <!-- 编辑导航表单 -->
    <div class="navigation-form edit-form" v-if="showEditForm">
      <form @submit.prevent="handleEdit">
        <div class="form-group">
          <label for="edit-title">标题</label>
          <input
            type="text"
            id="edit-title"
            v-model="editForm.title"
            required
            placeholder="请输入标题"
            minlength="2"
            maxlength="50"
          />
        </div>
        <div class="form-group">
          <label for="edit-description">描述</label>
          <textarea
            id="edit-description"
            v-model="editForm.description"
            placeholder="请输入描述"
            maxlength="200"
          ></textarea>
        </div>
        <div class="form-group">
          <label for="edit-url">链接</label>
          <input
            type="url"
            id="edit-url"
            v-model="editForm.url"
            required
            placeholder="请输入链接地址"
          />
        </div>
        <div class="form-actions">
          <button type="submit" :disabled="loading">{{ loading ? '更新中...' : '更新' }}</button>
          <button type="button" @click="cancelEdit" class="cancel-button">取消</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axiosInstance from '../utils/axios';

export default {
  name: 'Navigation',
  data() {
    return {
      navigationItems: [],
      showAddForm: false,
      showEditForm: false,
      loading: false,
      isAdmin: false,
      userId: null,
      form: {
        title: '',
        description: '',
        url: ''
      },
      editForm: {
        id: null,
        title: '',
        description: '',
        url: ''
      },
      deleteLoading: false,
      loadingItems: new Set()
    };
  },
  methods: {
    async visitLink(url) {
      if (!url) {
        this.$message.warning('链接地址不能为空');
        return;
      }
      try {
        window.open(url, '_blank');
      } catch (error) {
        this.$message.error('打开链接失败，请检查链接是否正确');
        console.error('打开链接失败:', error);
      }
    },
    async loadNavigations() {
      this.loading = true;
      try {
        const response = await axiosInstance.get('/navigation/');
        this.navigationItems = response.data;
      } catch (error) {
        console.error('加载导航内容失败:', error);
        this.$message.error(error.response?.data?.detail || '加载导航内容失败，请重试');
      } finally {
        this.loading = false;
      }
    },
    validateForm(formData) {
      if (!formData.title || formData.title.trim().length === 0) {
        this.$message.warning('标题不能为空');
        return false;
      }
      if (!formData.url || formData.url.trim().length === 0) {
        this.$message.warning('链接地址不能为空');
        return false;
      }
      try {
        new URL(formData.url);
      } catch (error) {
        this.$message.warning('请输入有效的链接地址');
        return false;
      }
      return true;
    },
    async handleSubmit() {
      if (this.loading) return;
      if (!this.validateForm(this.form)) return;

      this.loading = true;
      try {
        await axiosInstance.post('/navigation/', this.form);
        this.$message.success('添加成功');
        await this.loadNavigations();
        this.showAddForm = false;
        this.form = { title: '', description: '', url: '' };
      } catch (error) {
        console.error('添加导航内容失败:', error);
        this.$message.error(error.response?.data?.detail || '添加导航内容失败，请重试');
      } finally {
        this.loading = false;
      }
    },
    editItem(item) {
      if (!this.canEdit(item)) {
        this.$message.warning('您没有权限编辑此导航');
        return;
      }
      this.editForm = { ...item };
      this.showEditForm = true;
    },
    async handleEdit() {
      if (this.loading) return;
      if (!this.validateForm(this.editForm)) return;

      this.loading = true;
      try {
        await axiosInstance.put(`/navigation/${this.editForm.id}`, {
          title: this.editForm.title,
          description: this.editForm.description,
          url: this.editForm.url
        });
        
        this.$message.success('更新成功');
        await this.loadNavigations();
        this.showEditForm = false;
      } catch (error) {
        console.error('更新导航内容失败:', error);
        this.$message.error(error.response?.data?.detail || '更新导航内容失败，请重试');
      } finally {
        this.loading = false;
      }
    },
    canEdit(item) {
      return this.isAdmin || item.created_by === this.userId;
    },
    async deleteItem(id) {
      if (this.deleteLoading) return;
      
      try {
        await this.$confirm('确定要删除这个导航内容吗？此操作不可恢复', '警告', {
          confirmButtonText: '确定删除',
          cancelButtonText: '取消',
          type: 'warning',
          confirmButtonClass: 'el-button--danger'
        });
        
        this.loadingItems.add(id);
        this.deleteLoading = true;
        
        await axiosInstance.delete(`/navigation/${id}`);
        this.$message.success('删除成功');
        await this.loadNavigations();
      } catch (error) {
        if (error !== 'cancel') {
          this.$message.error(error.response?.data?.detail || '删除导航内容失败');
          console.error('删除导航内容失败:', error);
        }
      } finally {
        this.loadingItems.delete(id);
        this.deleteLoading = false;
      }
    },
    cancelAdd() {
      this.showAddForm = false;
      this.form = { title: '', description: '', url: '' };
    },
    cancelEdit() {
      this.showEditForm = false;
      this.editForm = { id: null, title: '', description: '', url: '' };
    },
    async checkUserRole() {
      try {
        const response = await axiosInstance.get('/me');
        this.isAdmin = response.data.role === 'admin';
        this.userId = response.data.id;
      } catch (error) {
        console.error('获取用户信息失败:', error);
        this.$message.error(error.response?.data?.detail || '获取用户信息失败');
      }
    }
  },
  created() {
    this.loadNavigations();
    this.checkUserRole();
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
.navigation-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.navigation-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.navigation-form {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  color: #666;
}

input,
textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

textarea {
  height: 100px;
  resize: vertical;
}

input:focus,
textarea:focus {
  outline: none;
  border-color: #4CAF50;
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

button {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

button[type="submit"] {
  background-color: #4CAF50;
  color: white;
}

button[type="submit"]:hover:not(:disabled) {
  background-color: #45a049;
}

.cancel-button {
  background-color: #f5f5f5;
  color: #666;
}

.cancel-button:hover {
  background-color: #e0e0e0;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.navigation-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.navigation-item {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
}

.navigation-content h3 {
  margin: 0 0 0.5rem;
  color: #333;
}

.navigation-content p {
  color: #666;
  margin: 0 0 1rem;
}

.navigation-content a {
  color: #4CAF50;
  text-decoration: none;
}

.navigation-content a:hover {
  text-decoration: underline;
}

.navigation-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
}

.edit-button,
.delete-button {
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
}

.edit-button {
  background-color: #2196F3;
  color: white;
}

.edit-button:hover {
  background-color: #1976D2;
}

.delete-button {
  background-color: #f44336;
  color: white;
}

.delete-button:hover:not(:disabled) {
  background-color: #d32f2f;
}

.loading-container,
.empty-container {
  text-align: center;
  padding: 3rem 0;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.loading-container p,
.empty-container p {
  color: #666;
  font-size: 1.1rem;
}
</style>