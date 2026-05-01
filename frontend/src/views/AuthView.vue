<template>
  <main class="auth-page">
    <!-- Left Section: Form -->
    <section class="auth-form-container">
      <div class="form-header">
        <div class="auth-toggle">
          <button 
            :class="['toggle-btn', { active: activeTab === 'register' }]" 
            @click="activeTab = 'register'"
          >
            Create
          </button>
          <button 
            :class="['toggle-btn', { active: activeTab === 'login' }]" 
            @click="activeTab = 'login'"
          >
            Log in
          </button>
        </div>
      </div>

      <div class="form-body">
        <div class="brand-minimal">
          <svg width="32" height="32" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect width="40" height="40" rx="8" fill="black"/>
            <path d="M12 10H28V14H22V30H18V14H12V10Z" fill="white"/>
            <circle cx="28" cy="28" r="4" fill="#F5F5F5" stroke="white" stroke-width="2"/>
          </svg>
          <span class="brand-text">13 Maps</span>
        </div>

        <!-- Login Form -->
        <form v-if="activeTab === 'login'" @submit.prevent="handleLogin" class="auth-form fade-in">
          <div class="form-title">
            <h1>Welcome back</h1>
            <p>Access the 13 Maps Information System</p>
          </div>

          <div class="form-group">
            <label for="login-email">Email Address</label>
            <div class="input-wrapper">
              <svg class="input-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
              <input 
                id="login-email" 
                v-model="loginData.email" 
                type="email" 
                class="input" 
                placeholder="name@gmail.com" 
                required 
              />
            </div>
          </div>

          <div class="form-group">
            <label for="login-password">Password</label>
            <div class="input-wrapper">
              <svg class="input-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
              <input 
                id="login-password" 
                v-model="loginData.password" 
                type="password" 
                class="input" 
                placeholder="Enter password" 
                required 
              />
            </div>
          </div>

          <p v-if="error" class="error-msg text-danger">{{ error }}</p>

          <button type="submit" class="btn btn-primary w-full" :disabled="loading">
            {{ loading ? 'Authenticating...' : 'Sign in' }}
          </button>
        </form>

        <!-- Register Form -->
        <form v-else @submit.prevent="handleRegister" class="auth-form fade-in">
          <div class="form-title">
            <h1>Create your account</h1>
            <p>Join the 13 Maps logistics network</p>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="reg-first-name">First name</label>
              <input 
                id="reg-first-name" 
                v-model="regData.firstName" 
                type="text" 
                class="input" 
                placeholder="John" 
                required 
              />
            </div>
            <div class="form-group">
              <label for="reg-last-name">Last name</label>
              <input 
                id="reg-last-name" 
                v-model="regData.lastName" 
                type="text" 
                class="input" 
                placeholder="Doe" 
                required 
              />
            </div>
          </div>

          <div class="form-group">
            <label for="reg-business">Business name</label>
            <input 
              id="reg-business" 
              v-model="regData.businessName" 
              type="text" 
              class="input" 
              placeholder="Company name" 
              required 
            />
          </div>



          <div class="form-group">
            <label for="reg-email">Email Address</label>
            <div class="input-wrapper">
              <svg class="input-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
              <input 
                id="reg-email" 
                v-model="regData.email" 
                type="email" 
                class="input" 
                placeholder="name@gmail.com" 
                required 
              />
            </div>
          </div>

          <div class="form-group">
            <label for="reg-password">Password</label>
            <div class="input-wrapper">
              <svg class="input-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
              <input 
                id="reg-password" 
                v-model="regData.password" 
                type="password" 
                class="input" 
                placeholder="Create password" 
                required 
              />
            </div>
          </div>

          <p v-if="error" class="error-msg text-danger">{{ error }}</p>
          <p v-if="success" class="success-msg text-success">{{ success }}</p>

          <button type="submit" class="btn btn-primary w-full" :disabled="loading">
            {{ loading ? 'Processing...' : 'Create Account' }}
          </button>
        </form>
      </div>
    </section>

    <!-- Right Section: Info -->
    <section class="auth-info">
      <div class="info-content">
        <div class="info-visual">
          <div class="graphic-container">
            <div class="graphic-blob">
              <svg width="120" height="120" viewBox="0 0 24 24" fill="none" stroke="#E2E8F0" stroke-width="0.5">
                <circle cx="12" cy="12" r="10" />
                <path d="M12 2v20M2 12h20" />
              </svg>
            </div>
            <div class="circle c1">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v20M17 5H9.5a4.5 4.5 0 0 0 0 9H13a4.5 4.5 0 0 1 0 9H4.5"/><polyline points="12,2 12,22"/></svg>
            </div>
            <div class="circle c2">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#f7931a" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 8v8M8 12h8"/></svg>
            </div>
          </div>
        </div>

        <div class="info-text">
          <h2>13 Maps is your Logistics Hub.</h2>
          <h3>Automate your route optimization.</h3>
        </div>

        <div class="features-list">
          <div class="feature-item">
            <div class="feature-icon">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12a9 9 0 0 1-9 9m9-9a9 9 0 0 0-9-9m9 9H3m9 9a9 9 0 0 1-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9"/></svg>
            </div>
            <div class="feature-desc">
              <h4>Global Route Optimization</h4>
              <p>Set parameters to automatically optimize delivery sequences.</p>
            </div>
          </div>
          <div class="feature-item">
            <div class="feature-icon">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
            </div>
            <div class="feature-desc">
              <h4>Enterprise Security</h4>
              <p>Data integrity and multi-tenant isolation at every level.</p>
            </div>
          </div>
        </div>

        <div class="info-footer">
          <a href="#">Privacy</a>
          <span class="dot">·</span>
          <a href="#">Terms</a>
          <span class="dot">·</span>
          <a href="#">Support</a>
        </div>
      </div>
    </section>
  </main>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const activeTab = ref('register')
const loading = ref(false)
const error = ref(null)
const success = ref(null)

const loginData = reactive({
  email: '',
  password: ''
})

const regData = reactive({
  businessName: '',
  firstName: '',
  lastName: '',
  email: '',
  password: ''
})

onMounted(() => {
  if (route.name === 'Login') {
    activeTab.value = 'login'
  }
})

async function handleLogin() {
  error.value = null
  loading.value = true
  try {
    await auth.login(loginData.email, loginData.password)
    const redirect = route.query.redirect || '/dashboard/routes'
    router.push(redirect)
  } catch (err) {
    error.value = err.message || 'Authentication failed'
  } finally {
    loading.value = false
  }
}

async function handleRegister() {
  error.value = null
  success.value = null
  loading.value = true
  try {
    const fullName = `${regData.firstName} ${regData.lastName}`
    await auth.register(regData.email, regData.password, fullName)
    success.value = 'Account created. Please log in.'
    setTimeout(() => {
      activeTab.value = 'login'
      loginData.email = regData.email
      success.value = null
    }, 1500)
  } catch (err) {
    error.value = err.message || 'Registration failed'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page {
  display: flex;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  background-color: #ffffff;
}

/* --- Left Form Section --- */
.auth-form-container {
  flex: 2;
  display: flex;
  flex-direction: column;
  padding: 24px 40px;
  background: white;
  height: 100%;
}

.form-header {
  display: flex;
  justify-content: center;
  margin-bottom: 32px;
}

.auth-toggle {
  display: flex;
  background: #f1f5f9;
  padding: 3px;
  border-radius: 999px;
}

.toggle-btn {
  padding: 6px 20px;
  border-radius: 999px;
  border: none;
  font-size: 13px;
  font-weight: 600;
  color: #64748b;
  background: transparent;
  cursor: pointer;
  transition: all 0.15s;
}

.toggle-btn.active {
  background: white;
  color: #000;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.form-body {
  max-width: 400px;
  width: 100%;
  margin: 0 auto;
}

.brand-minimal {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 24px;
}

.brand-text {
  font-size: 18px;
  font-weight: 800;
  letter-spacing: -0.02em;
}

.form-title h1 {
  font-size: 20px;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 4px;
}

.form-title p {
  color: #64748b;
  font-size: 13px;
  margin-bottom: 24px;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.form-group label {
  display: block;
  font-size: 12px;
  font-weight: 600;
  color: #475569;
  margin-bottom: 6px;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 12px;
  color: #94a3b8;
}

.input {
  width: 100%;
  padding: 9px 12px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 14px;
  color: #1e293b;
  transition: all 0.2s;
}

.input-wrapper .input {
  padding-left: 36px;
}

.input:focus {
  background: white;
  border-color: #000;
  outline: none;
  box-shadow: 0 0 0 3px rgba(0,0,0,0.03);
}

.btn-primary {
  background: #000;
  color: white;
  padding: 11px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 700;
  margin-top: 8px;
}

.btn-primary:hover {
  background: #1e293b;
}

/* --- Right Info Section --- */
.auth-info {
  flex: 1;
  background-color: #F5F5F5;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
  height: 100%;
}

.info-content {
  max-width: 420px;
  width: 100%;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.info-visual {
  margin-bottom: 40px;
  flex: 0.8;
  display: flex;
  align-items: center;
  justify-content: center;
}

.graphic-container {
  position: relative;
  width: 200px;
  height: 200px;
}

.circle {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
  position: absolute;
  z-index: 2;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.c1 { left: 0; top: 20%; color: #64748b; }
.c2 { right: 0; top: 10%; }

.graphic-blob {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  opacity: 0.5;
}

.info-text h2 {
  font-size: 22px;
  font-weight: 600;
  color: #64748b;
  line-height: 1.2;
}

.info-text h3 {
  font-size: 22px;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 32px;
}

.features-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 32px;
}

.feature-item {
  background: white;
  padding: 14px 18px;
  border-radius: 12px;
  display: flex;
  gap: 16px;
  border: 1px solid rgba(0,0,0,0.03);
}

.feature-icon {
  color: #64748b;
  flex-shrink: 0;
  margin-top: 2px;
}

.feature-desc h4 {
  font-size: 13px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 2px;
}

.feature-desc p {
  font-size: 12px;
  color: #64748b;
  line-height: 1.4;
}

.info-footer {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: auto;
  padding-bottom: 10px;
}

.info-footer a {
  font-size: 12px;
  color: #94a3b8;
  font-weight: 600;
}

.dot {
  color: #e2e8f0;
}

.error-msg, .success-msg {
  font-size: 12px;
  text-align: center;
  padding: 8px;
  border-radius: 6px;
}

.fade-in {
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(5px); }
  to { opacity: 1; transform: translateY(0); }
}

@media (max-height: 700px) {
  .info-visual { display: none; }
  .form-header { margin-bottom: 20px; }
  .brand-minimal { margin-bottom: 15px; }
}
</style>
