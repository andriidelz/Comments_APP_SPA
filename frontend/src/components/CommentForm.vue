<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useVuelidate } from '@vuelidate/core'
import { required, email, url, alphaNum } from '@vuelidate/validators'
import Toolbar from './Toolbar.vue'
import PreviewModal from './PreviewModal.vue'
import { useRouter } from 'vue-router'
import { sendMessage, connectWS } from "./ws";

const API_URL = import.meta.env.VITE_API_URL
const router = useRouter() 

const form = ref({
  user_name: '',
  email: '',
  home_page: '',
  captcha: '',
  text: '',
  image: null,
  file: null,
  parent: null
})

const loginForm = ref({
  username: '',
  password: ''
})

const captchaKey = ref('')
const captchaImage = ref('')
const isAuthenticated = ref(!!localStorage.getItem('access_token'))
const loginError = ref('') 

const showPreview = ref(false)

const rules = {
  user_name: { required, alphaNum },
  email: { required, email },
  home_page: { url },
  captcha: { required, alphaNum },
  text: { required }
}

const v$ = useVuelidate(rules, form)

const fetchCaptcha = async () => {
  try {
    const response = await axios.get(`${API_URL}/api/captcha/key/`, {
      headers: { 'Content-Type': 'application/json' }
    })
    const data = response.data // axios automatically parses JSON
    captchaKey.value = data.key
    captchaImage.value = `${API_URL}/api/captcha/image/${data.key}/`
  } catch (error) {
    console.error('Failed to fetch CAPTCHA:', error.response?.data || error.message)
  }

}
onMounted(fetchCaptcha)

const login = async () => {
  try {
    const response = await axios.post(`${API_URL}/api/token/`, {
      username: loginForm.value.username,
      password: loginForm.value.password
    })
    localStorage.setItem('access_token', response.data.access)
    localStorage.setItem('refresh_token', response.data.refresh)
    isAuthenticated.value = true
    loginError.value = ''
    loginForm.value.username = ''
    loginForm.value.password = ''
    router.push('/comments') // Redirect to comment form
  } catch (error) {
    loginError.value = error.response?.data?.detail || 'Login failed'
    console.error('Login failed:', error.response?.data || error.message)
  }
}

const insertTag = (tag) => {
  form.value.text += `<${tag}></${tag}>`
}

const preview = () => {
  showPreview.value = true
}

const submit = async () => {
  if (!isAuthenticated.value) {
    loginError.value = 'Please log in to submit a comment'
    return
  }

  if (await v$.value.$validate()) {
    const formData = new FormData()
    Object.keys(form.value).forEach(key => {
      if (form.value[key] !== null) {
        formData.append(key, form.value[key])
      }
    })
    formData.append('captcha_0', captchaKey.value)
    formData.append('captcha_1', form.value.captcha)

    try {
      const token = localStorage.getItem('access_token')
      const response = await axios.post(`${API_URL}/api/comments/`, formData, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'multipart/form-data'
        }
      })

      const wsInstance = connectWS(token)
      if (wsInstance.readyState === WebSocket.OPEN) {
        sendMessage(response.data)
      } else {
      wsInstance.addEventListener('open', () => {
        sendMessage(response.data)
        }, { once: true })
      }

      form.value = {
        user_name: '',
        email: '',
        home_page: '',
        captcha: '',
        text: '',
        image: null,
        file: null,
        parent: null
      }
      v$.value.$reset()
      await fetchCaptcha() 
    } catch (e) {
      console.error('Submission error:', e.response?.data || e.message)
    }
  }
}
</script>

<template>
  <div>
    <div v-if="!isAuthenticated">
      <h3>Login</h3>
      <form @submit.prevent="login">
        <input v-model="loginForm.username" placeholder="Username" required />
        <input v-model="loginForm.password" type="password" placeholder="Password" required />
        <div v-if="loginError" class="error">{{ loginError }}</div>
        <button type="submit">Log In</button>
      </form>
    </div>

    <form v-else @submit.prevent="submit">
      <input v-model="form.user_name" placeholder="User Name" />
      <div v-if="v$.user_name.$error" class="error">{{ v$.user_name.$errors?.[0]?.$message }}</div>

      <input v-model="form.email" placeholder="Email" />
      <div v-if="v$.email.$error" class="error">{{ v$.email.$errors[0].$message }}</div>

      <input v-model="form.home_page" placeholder="Home Page" />
      <div v-if="v$.home_page.$error" class="error">{{ v$.home_page.$errors[0].$message }}</div>

      <div>
        <img :src="captchaImage" alt="CAPTCHA" v-if="captchaImage" />
        <input v-model="form.captcha" placeholder="Enter CAPTCHA" />
        <div v-if="v$.captcha.$error" class="error">{{ v$.captcha.$errors[0].$message }}</div>
      </div>

      <textarea v-model="form.text" placeholder="Text"></textarea>
      <div v-if="v$.text.$error" class="error">{{ v$.text.$errors[0].$message }}</div>

      <Toolbar @insert="insertTag" />

      <input type="file" @change="form.image = $event.target.files[0]" accept="image/*" />
      <input type="file" @change="form.file = $event.target.files[0]" accept=".txt" />

      <button type="button" @click="preview">Preview</button>
      <button type="submit">Submit</button>
    </form>

    <PreviewModal v-if="showPreview" :text="form.text" @close="showPreview = false" />
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
input, textarea {
  display: block;
  margin: 10px 0;
  width: 100%;
  max-width: 400px;
}
button {
  margin-right: 10px;
}
</style>