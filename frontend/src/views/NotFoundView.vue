<template>
  <main class="not-found-page flex-center">
    <div class="content">
      <div class="error-code text-gradient">404</div>
      <h1 class="title">Lost in Transit?</h1>
      <p class="description">The page you're looking for has been rerouted or doesn't exist in our mapping system.</p>
      <div class="actions">
        <router-link to="/" class="btn btn-primary">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>
          Back to Home
        </router-link>
        <router-link to="/dashboard/help" class="btn btn-ghost">Contact Support</router-link>
      </div>
    </div>
    
    <div class="bg-decoration">
      <div class="circle circle-1"></div>
      <div class="circle circle-2"></div>
    </div>
  </main>
</template>

<style scoped>
.not-found-page {
  min-height: 100vh;
  background-color: #f8fafc;
  position: relative;
  overflow: hidden;
  text-align: center;
  padding: var(--space-xl);
}

.content {
  position: relative;
  z-index: 1;
  max-width: 480px;
}

.error-code {
  font-size: 8rem;
  font-weight: 900;
  line-height: 1;
  margin-bottom: var(--space-md);
  letter-spacing: -0.05em;
  opacity: 0.8;
}

.text-gradient {
  background: linear-gradient(135deg, var(--clr-primary), var(--clr-accent));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.title {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: var(--space-md);
  color: var(--clr-text);
}

.description {
  font-size: 1.1rem;
  color: var(--clr-muted);
  margin-bottom: var(--space-2xl);
  line-height: 1.6;
}

.actions {
  display: flex;
  gap: var(--space-md);
  justify-content: center;
}

.bg-decoration {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.circle {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.1;
}

.circle-1 {
  width: 400px;
  height: 400px;
  background: var(--clr-primary);
  top: -100px;
  right: -100px;
}

.circle-2 {
  width: 300px;
  height: 300px;
  background: var(--clr-accent);
  bottom: -50px;
  left: -50px;
}
</style>
