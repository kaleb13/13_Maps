<template>
  <div class="minimalist-page">
    <nav class="sub-nav">
      <router-link to="/" class="back-link">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
        <span>Home</span>
      </router-link>
    </nav>

    <main class="container content-area">
      <div class="reveal active">
        <p class="hero-tag">Transparent Pricing</p>
        <h1 class="hero-title">Simple. <br /><span class="text-thin">Scalable.</span></h1>
        
        <div class="pricing-minimal-grid">
          <div class="pricing-card">
            <div class="p-header">
              <span class="p-name">Individual</span>
              <div class="p-price">$0</div>
            </div>
            <p class="p-desc">Perfect for small projects and individual developers exploring our engine.</p>
            <ul class="p-list">
              <li>100 route requests / mo</li>
              <li>Basic optimization</li>
              <li>Public support</li>
            </ul>
            <router-link to="/register" class="btn-p">Get Started</router-link>
          </div>

          <div class="pricing-card active-card">
            <div class="p-header">
              <span class="p-name">Enterprise</span>
              <div class="p-price">$99</div>
            </div>
            <p class="p-desc">High-performance features for growing fleets and logistics businesses.</p>
            <ul class="p-list">
              <li>Unlimited requests</li>
              <li>Multi-stop VRP solver</li>
              <li>Dedicated cluster</li>
              <li>API support</li>
            </ul>
            <router-link to="/register" class="btn-p primary-btn">Start Trial</router-link>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');

.minimalist-page {
  font-family: 'Outfit', sans-serif;
  background-color: #fcfcfc;
  color: #1a1a1a;
  min-height: 100vh;
  padding-top: 100px;
}

.sub-nav {
  position: fixed;
  top: 40px;
  left: 40px;
  z-index: 100;
}

.back-link {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  color: #1a1a1a;
  font-weight: 500;
  font-size: 0.9rem;
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

.pricing-minimal-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
}

.pricing-card {
  padding: 40px;
  border: 1px solid #eee;
  border-radius: 20px;
  background: white;
  transition: transform 0.3s;
}

.active-card {
  border-color: var(--clr-primary);
  box-shadow: 0 20px 40px rgba(83, 70, 152, 0.05);
  transform: translateY(-10px);
}

.p-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 20px;
}

.p-name { font-weight: 600; font-size: 1.2rem; color: #666; }
.p-price { font-size: 2.5rem; font-weight: 700; }

.p-desc { color: #888; font-size: 0.95rem; margin-bottom: 30px; line-height: 1.5; }

.p-list {
  list-style: none;
  padding: 0;
  margin: 0 0 40px 0;
}

.p-list li {
  padding: 10px 0;
  border-bottom: 1px solid #fafafa;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 10px;
}

.p-list li::before {
  content: '';
  width: 4px;
  height: 4px;
  background: var(--clr-primary);
  border-radius: 50%;
}

.btn-p {
  display: block;
  text-align: center;
  padding: 15px;
  border: 1px solid #1a1a1a;
  border-radius: 100px;
  text-decoration: none;
  color: #1a1a1a;
  font-weight: 600;
  transition: all 0.3s;
}

.primary-btn {
  background: #1a1a1a;
  color: white;
}

.btn-p:hover {
  background: #1a1a1a;
  color: white;
}

@media (max-width: 768px) {
  .pricing-minimal-grid { grid-template-columns: 1fr; }
}
</style>
