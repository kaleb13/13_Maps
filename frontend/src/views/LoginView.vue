<template>
  <main class="auth-page flex-center">
    <div class="auth-card card">
      <div class="auth-logo">
        <span class="logo-icon">🗺️</span>
        <h1>RouteOpt</h1>
      </div>
      <p class="auth-subtitle text-muted">AI-powered route optimization platform</p>

      <form id="login-form" class="auth-form" @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="login-email">Email address</label>
          <input
            id="login-email"
            v-model="email"
            type="email"
            class="input"
            placeholder="you@company.com"
            required
            autocomplete="email"
          />
        </div>
        <div class="form-group">
          <label for="login-password">Password</label>
          <input
            id="login-password"
            v-model="password"
            type="password"
            class="input"
            placeholder="••••••••"
            required
            autocomplete="current-password"
          />
        </div>

        <p v-if="error" class="error-msg text-danger">{{ error }}</p>

        <button id="login-submit" type="submit" class="btn btn-primary w-full" :disabled="loading">
          {{ loading ? 'Signing in…' : 'Sign in' }}
        </button>
      </form>

      <p class="auth-footer text-muted">
        Don't have an account?
        <router-link to="/register">Create one</router-link>
      </p>
    </div>
  </main>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const email    = ref('')
const password = ref('')
const error    = ref(null)
const loading  = ref(false)

const auth   = useAuthStore()
const router = useRouter()
const route  = useRoute()

async function handleLogin() {
  error.value   = null
  loading.value = true
  try {
    await auth.login(email.value, password.value)
    const redirect = route.query.redirect || '/dashboard/routes'
    router.push(redirect)
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
  background: radial-gradient(ellipse at 60% 30%, rgba(83, 70, 152, 0.08) 0%, transparent 70%),
              var(--clr-bg);
}
.auth-card  { width: 100%; max-width: 420px; }
.auth-logo  { display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.25rem; }
.auth-logo h1 { font-size: 1.5rem; font-weight: 700; }
.logo-icon  { font-size: 1.75rem; }
.auth-subtitle { margin-bottom: var(--space-xl); font-size: 0.9rem; }
.auth-form  { display: flex; flex-direction: column; gap: var(--space-md); }
.w-full     { width: 100%; justify-content: center; }
.error-msg  { font-size: 0.875rem; }
.auth-footer { margin-top: var(--space-lg); text-align: center; font-size: 0.875rem; }
</style>
