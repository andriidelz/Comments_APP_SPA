<script setup>
import { ref, onMounted, onUnmounted, getCurrentInstance } from 'vue'
import CommentItem from './CommentItem.vue'
import CommentForm from './CommentForm.vue'
import { connectWS, onMessage, sendMessage, disconnectWS } from '../components/ws.js'
import lightbox from 'lightbox2'

const { proxy } = getCurrentInstance() 

const comments = ref([])
const page = ref(1)
const sortBy = ref('-created_at')

const loadComments = async () => {
  try {
    const res = await proxy.$api.get(`/comments/?page=${page.value}&sort_by=${sortBy.value}`)
    comments.value = res.data
    lightbox.reload() 
  } catch (error) {
    console.error('Failed to load comments:', error.response?.data || error.message)
  }
}

const changeSort = () => {
  page.value = 1
  loadComments()
}

onMounted(async () => {
  await loadComments()

  const socket = connectWS(proxy)
  if (!socket) return

  onMessage((newComment) => {
    comments.value.unshift(newComment)

    lightbox.option({
      resizeDuration: 200,
      wrapAround: true
    })
  })
})

onUnmounted(() => {
  disconnectWS()
})

</script>

<template>
  <div>
    <select v-model="sortBy" @change="changeSort">
      <option value="-created_at">Date Desc</option>
      <option value="created_at">Date Asc</option>
      <option value="user_name">User Asc</option>
      <option value="-user_name">User Desc</option>
      <option value="email">Email Asc</option>
      <option value="-email">Email Desc</option>
    </select>

    <CommentItem v-for="comment in comments" :key="comment.id" :comment="comment" />
    
    <div class="pagination">
      <button @click="page--; loadComments()" :disabled="page <= 1">Prev</button>
      <button @click="page++; loadComments()">Next</button>
    </div>

    <CommentForm />
  </div>
</template>

<style scoped>
.pagination {
  margin: 10px 0;
}
</style>
