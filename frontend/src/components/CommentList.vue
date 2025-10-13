<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import CommentItem from './CommentItem.vue'
import CommentForm from './CommentForm.vue'

const API_URL = import.meta.env.VITE_API_URL

const comments = ref([])
const page = ref(1)
const sortBy = ref('-created_at')
const token = localStorage.getItem('access_token')
const ws = ref(null)

onMounted(async () => {
  loadComments()

if (token && API_URL) { 
  ws.value = new WebSocket(`${API_URL.replace('http', 'ws')}/ws/comments/?token=${token}`)
  ws.value.onmessage = (event) => {
    const data = JSON.parse(event.data)
    comments.value.unshift(data.message)
  }
  ws.value.onclose = () => console.log('WebSocket closed')
  ws.value.onerror = (error) => console.error('WebSocket error:', error)
  }
})

const loadComments = async () => {
  try {
    const token = localStorage.getItem('access_token')
    const res = await axios.get(`${API_URL}/api/comments/?page=${page.value}&sort_by=${sortBy.value}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })
    comments.value = res.data
  } catch (error) {
    console.error('Failed to load comments:', error.response?.data || error.message)
  }
}
</script>

<template>
  <select v-model="sortBy" @change="loadComments">
    <option value="-created_at">Date Desc</option>
    <option value="created_at">Date Asc</option>
    <option value="user_name">User Asc</option>
    <option value="-user_name">User Desc</option>
    <option value="email">Email Asc</option>
    <option value="-email">Email Desc</option>
  </select>
  <CommentItem v-for="comment in comments" :key="comment.id" :comment="comment" />
  <button @click="page--; loadComments()" :disabled="page <= 1">Prev</button>
  <button @click="page++; loadComments()">Next</button>
  <CommentForm />
</template>