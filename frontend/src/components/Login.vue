<script setup>
import { ref, getCurrentInstance } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const { proxy } = getCurrentInstance()

const loginForm = ref({
  username: '',
  password: ''
})
const loginError = ref('')

async function login() {
  try {
    const response = await proxy.$api.post('/token/', {
      username: loginForm.value.username,
      password: loginForm.value.password
    })

    loginError.value = ''
    loginForm.value.username = ''
    loginForm.value.password = ''

    router.push('/comments')
  } catch (error) {
    loginError.value =
      error.response?.data?.detail ||
      (error.request ? 'No response from server' : error.message)
    console.error('Login failed:', error.response?.data || error.message)
  }
}
</script>

<template>
  <div>
    <h3>Login</h3>
    <form @submit.prevent="login">
      <input v-model="loginForm.username" placeholder="Username" required />
      <input v-model="loginForm.password" type="password" placeholder="Password" required />
      <div v-if="loginError" class="error">{{ loginError }}</div>
      <button type="submit">Log In</button>
    </form>
  </div>
</template>

<style scoped>
.error {
  color: red;
  font-size: 0.8em;
}
form {
  margin-bottom: 20px;
}
input {
  display: block;
  margin: 10px 0;
  width: 100%;
  max-width: 400px;
}
</style>
