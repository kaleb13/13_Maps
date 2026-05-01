<template>
  <main class="auth-page flex-center">
    <div class="auth-card card">
      <div class="auth-logo">
        <span class="logo-icon">🗺️</span>
        <h1>RouteOpt</h1>
      </div>
      <p class="auth-subtitle text-muted">Create your free account</p>

      <form id="register-form" class="auth-form" @submit.prevent="handleRegister">
        <div class="form-group">
          <label for="reg-name">Full name</label>
          <input id="reg-name" v-model="fullName" type="text" class="input" placeholder="Jane Doe" />
        </div>
        <div class="form-group">
          <label for="reg-email">Email address</label>
          <input id="reg-email" v-model="email" type="email" class="input" placeholder="you@company.com" required />
        </div>
        <div class="form-group">
          <label for="reg-password">Password <span class="text-muted">(min 8 chars)</span></label>
          <input id="reg-password" v-model="password" type="password" class="input" placeholder="••••••••" required minlength="8" />
        </div>

        <p v-if="error" class="error-msg text-danger">{{ error }}</p>
        <p v-if="success" class="success-msg text-success">{{ success }}</p>

        <button id="register-submit" type="submit" class="btn btn-primary w-full" :disabled="loading">
          {{ loading ? 'Creating account…' : 'Create account' }}
        </button>
      </form>

      <p class="auth-footer text-muted">
        Already have an account? <router-link to="/login">Sign in</router-link>
      </p>
    </div>
  </main>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const fullName = ref('')
const email    = ref('')
const password = ref('')
const error    = ref(null)
const success  = ref(null)
const loading  = ref(false)

const auth   = useAuthStore()
const router = useRouter()

async function handleRegister() {
  error.value   = null
  success.value = null
  loading.value = true
  try {
    await auth.register(email.value, password.value, fullName.value)
    success.value = 'Account created! Redirecting to login…'
    setTimeout(() => router.push('/login'), 1500)
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  background: radial-gradient(ellipse at 40% 60%, rgba(124, 58, 237, 0.07) 0%, transparent 70%),
              var(--clr-bg);
}
.auth-card  { width: 100%; max-width: 420px; }
.auth-logo  { display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.25rem; }
.auth-logo h1 { font-size: 1.5rem; font-weight: 700; }
.logo-icon  { font-size: 1.75rem; }
.auth-subtitle { margin-bottom: var(--space-xl); font-size: 0.9rem; }
.auth-form  { display: flex; flex-direction: column; gap: var(--space-md); }
.w-full     { width: 100%; justify-content: center; }
.error-msg, .success-msg { font-size: 0.875rem; }
.auth-footer { margin-top: var(--space-lg); text-align: center; font-size: 0.875rem; }
</style>
