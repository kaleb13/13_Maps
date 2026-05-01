<template>
  <div class="drawer-page">
    <div class="drawer-header">
      <button @click="$router.back()" class="close-drawer-btn">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
      </button>
    </div>

    <main class="drawer-content">
      <div class="container reveal active">
        <p class="hero-tag">Legal</p>
        <h1 class="hero-title">Terms & <br /><span class="text-thin">Conditions.</span></h1>
        
        <div class="legal-content">
          <section class="legal-section">
            <h2>Acceptance of Terms</h2>
            <p>By accessing and using 13 Maps, you agree to be bound by these Terms and Conditions. If you do not agree, please refrain from using our services.</p>
          </section>

          <section class="legal-section">
            <h2>Service Usage</h2>
            <p>Our routing engine is provided for commercial logistics optimization. Misuse of our API or attempts to reverse engineer our algorithms are strictly prohibited.</p>
          </section>

          <section class="legal-section">
            <h2>Account Responsibility</h2>
            <p>You are responsible for maintaining the confidentiality of your account credentials and for all activities that occur under your account.</p>
          </section>
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
  max-width: 800px;
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
  margin-bottom: 60px;
}

.text-thin { font-weight: 300; font-style: italic; }

.legal-section {
  margin-bottom: 60px;
}

.legal-section h2 {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 20px;
  letter-spacing: -0.01em;
}

.legal-section p {
  color: #666;
  line-height: 1.8;
  font-size: 1.1rem;
}

@keyframes slideUp {
  from { transform: translateY(100%); }
  to { transform: translateY(0); }
}

.reveal.active {
  opacity: 1;
  transform: translateY(0);
}
</style>

