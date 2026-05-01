<template>
  <div class="drawer-page">
    <div class="drawer-header">
      <button @click="$router.back()" class="close-drawer-btn">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
      </button>
    </div>

    <main class="drawer-content">
      <div class="container reveal active">
        <p class="hero-tag">Help Center</p>
        <h1 class="hero-title">How can we <br /><span class="text-thin">support you?</span></h1>
        
        <div class="support-grid">
          <div class="support-card">
            <h3>Documentation</h3>
            <p>Deep dive into our API references and integration guides.</p>
            <a href="#" class="support-link">Browse Docs</a>
          </div>
          <div class="support-card">
            <h3>Technical Support</h3>
            <p>Our engineers are ready to help with complex routing logic.</p>
            <router-link to="/contact" class="support-link">Open Ticket</router-link>
          </div>
          <div class="support-card">
            <h3>Status Page</h3>
            <p>Monitor our global engine performance in real-time.</p>
            <a href="#" class="support-link">Check Status</a>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');

.drawer-page {
  font-family: 'Outfit', sans-serif;
  background-color: white;
  color: #1a1a1a;
  min-height: 100vh;
  position: relative;
  animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

.drawer-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding: 0 40px;
  z-index: 100;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
}

.close-drawer-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: #1a1a1a;
  padding: 10px;
  border-radius: 50%;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-drawer-btn:hover {
  background-color: #f5f5f5;
  transform: rotate(90deg);
}

.drawer-content {
  padding-top: 120px;
  padding-bottom: 100px;
}

.container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 40px;
}

.hero-tag {
  font-size: 0.85rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.3em;
  color: var(--clr-primary);
  margin-bottom: 20px;
}

.hero-title {
  font-size: clamp(3rem, 6vw, 4.5rem);
  font-weight: 700;
  line-height: 1;
  letter-spacing: -0.04em;
  margin-bottom: 80px;
}

.text-thin { font-weight: 300; font-style: italic; }

.support-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 40px;
}

.support-card {
  padding: 40px;
  background: white;
  border: 1px solid #eee;
  border-radius: 20px;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.support-card:hover {
  transform: translateY(-10px);
  border-color: var(--clr-primary);
  box-shadow: 0 20px 40px rgba(0,0,0,0.05);
}

.support-card h3 {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 15px;
  letter-spacing: -0.01em;
}

.support-card p {
  color: #666;
  line-height: 1.6;
  margin-bottom: 30px;
}

.support-link {
  font-weight: 700;
  color: var(--clr-primary);
  text-decoration: none;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

@keyframes slideUp {
  from { transform: translateY(100%); }
  to { transform: translateY(0); }
}

.reveal.active {
  opacity: 1;
  transform: translateY(0);
}

@media (max-width: 768px) {
  .support-grid { grid-template-columns: 1fr; }
}
</style>

