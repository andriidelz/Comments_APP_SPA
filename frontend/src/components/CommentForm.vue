<script setup>
import { ref, onMounted, onBeforeUnmount, getCurrentInstance, watch } from 'vue'
import { useVuelidate } from '@vuelidate/core'
import { required, email, url, alphaNum, minLength } from '@vuelidate/validators'
import { setTokens, getAccessToken } from '../utils/auth.js'
import Toolbar from './Toolbar.vue'
import PreviewModal from './PreviewModal.vue'
import { connectWS } from '../components/ws.js'

const { proxy } = getCurrentInstance()
const emit = defineEmits(['comment-submitted'])

const form = ref({
  user_name: '',
  // password: '',
  email: '',
  home_page: '',
  captcha: '',
  text: '',
  image: null,
  file: null,
  parent: null
})

const loginForm = ref({ username: '', password: '' })
const captchaKey = ref('')
const captchaImage = ref('')
const isAuthenticated = ref(!!getAccessToken())
const loginError = ref('')
const showPreview = ref(false)
// const showPassword = ref(false)

const wsInstance = ref(null)

onMounted(async () => {
  await fetchCaptcha()

  wsInstance.value = connectWS(proxy)
  if (wsInstance.value) {
    wsInstance.value.addEventListener('open', () => console.log('WebSocket connected'))
    wsInstance.value.addEventListener('close', () => {
      console.log('WebSocket closed, reconnecting...')
      setTimeout(() => { wsInstance.value = connectWS(proxy) }, 1000)
    })
  }
})

onBeforeUnmount(() => {
  if (wsInstance.value) wsInstance.value.close()
})

const rules = {
  user_name: { required, alphaNum },
  // password: { required, minLength: minLength(6) },
  email: { required, email },
  home_page: { url },
  captcha: { required, alphaNum },
  text: { required }
}
const v$ = useVuelidate(rules, form)

const fetchCaptcha = async () => {
  try {
    const response = await proxy.$api.get('/captcha/key/')
    captchaKey.value = response.data.key
    captchaImage.value = `${import.meta.env.VITE_API_URL}/captcha/image/${captchaKey.value}/`
  } catch (error) {
    console.error('Failed to fetch CAPTCHA:', error.response?.data || error.message)
  }
}
// onMounted(fetchCaptcha)

const login = async () => {
  try {
    const response = await proxy.$api.post('/token/', {
      username: loginForm.value.username,
      password: loginForm.value.password
    })
    setTokens(response.data.access, response.data.refresh)
    isAuthenticated.value = true
    loginError.value = ''
    loginForm.value.username = ''
    loginForm.value.password = ''
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
      if (form.value[key] !== null) formData.append(key, form.value[key])
    })
    formData.append('captcha_0', captchaKey.value)
    formData.append('captcha_1', form.value.captcha)

    try {
      await proxy.$api.post('/comments/', formData, {
        headers: { 
          'Content-Type': 'multipart/form-data',
          'Authorization': `Bearer ${getAccessToken()}`
        }
      })

      form.value = { user_name: '', email: '', home_page: '', captcha: '', text: '', image: null, file: null, parent: null }
      v$.value.$reset()
      await fetchCaptcha()
    } catch (e) {
      console.error('Submission error:', e.response?.data || e.message)
      alert(`Submission failed: ${JSON.stringify(e.response?.data || e.message)}`)
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
      <input v-model="form.email" placeholder="Email" />
      <input v-model="form.home_page" placeholder="Home Page" />
      <div>
        <img :src="captchaImage" alt="CAPTCHA" v-if="captchaImage" />
        <input v-model="form.captcha" placeholder="Enter CAPTCHA" />
      </div>
      <textarea v-model="form.text" placeholder="Text"></textarea>
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
