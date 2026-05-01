<template>
  <div class="landing-page" ref="scrollContainer">
    <!-- Minimal Navigation -->
    <nav class="minimal-nav" :class="{ 'is-scrolled': scrollY > 50 }">
      <div class="nav-container">
        <div class="brand">
          <div class="brand-logo">13</div>
          <span class="brand-name">Maps</span>
        </div>
        <div class="nav-right">
          <router-link to="/login" class="nav-link">Sign In</router-link>
          <button class="menu-toggle" @click="isMenuOpen = !isMenuOpen" :class="{ 'is-open': isMenuOpen }">
            <span class="line line-1"></span>
            <span class="line line-2"></span>
          </button>
        </div>
      </div>
    </nav>

    <!-- Large Dropdown Menu Modal -->
    <transition name="fade">
      <div v-if="isMenuOpen" class="menu-backdrop" @click="isMenuOpen = false"></div>
    </transition>

    <transition name="menu-slide">
      <div v-if="isMenuOpen" class="menu-modal-container">
        <div class="menu-grid">
          <div class="menu-links">
            <router-link to="/about" class="menu-item" @click="isMenuOpen = false">
              <span class="m-num">01</span>
              <span class="m-text">About</span>
            </router-link>
            <router-link to="/pricing" class="menu-item" @click="isMenuOpen = false">
              <span class="m-num">02</span>
              <span class="m-text">Pricing</span>
            </router-link>
            <router-link to="/contact" class="menu-item" @click="isMenuOpen = false">
              <span class="m-num">03</span>
              <span class="m-text">Contact</span>
            </router-link>
          </div>
          <div class="menu-aside">
            <div class="aside-content">
              <p class="aside-tag">Ready to Scale?</p>
              <h3>Join the logistics revolution today.</h3>
              <router-link to="/register" class="cta-minimal" @click="isMenuOpen = false">Get Started Free</router-link>
            </div>
          </div>
        </div>
      </div>
    </transition>

    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-bg">
        <div class="orbit orbit-1"></div>
        <div class="orbit orbit-2"></div>
        <div class="orbit orbit-3"></div>
        <div class="floating-map">
          <svg viewBox="0 0 800 800" class="globe-svg">
            <circle cx="400" cy="400" r="300" class="globe-outline" />
            <path d="M400 100 A300 300 0 0 1 400 700" class="globe-meridian" />
            <path d="M400 100 A150 300 0 0 1 400 700" class="globe-meridian" />
            <path d="M100 400 A300 150 0 0 1 700 400" class="globe-parallel" />
            
            <!-- Animated Route Points -->
            <g class="dots">
              <circle cx="400" cy="100" r="4" class="dot" />
              <circle cx="700" cy="400" r="4" class="dot" />
              <circle cx="400" cy="700" r="4" class="dot" />
              <circle cx="100" cy="400" r="4" class="dot" />
            </g>
          </svg>
        </div>
      </div>

      <div class="container hero-inner">
        <div class="hero-content reveal">
          <p class="hero-tag">Global Logistics Engine</p>
          <h1 class="hero-title">
            Intelligence <br />
            <span class="text-thin">in Motion.</span>
          </h1>
          <p class="hero-sub">
            The next generation of route optimization. <br />
            Built for speed, scale, and elegance.
          </p>
          <div class="hero-actions">
            <router-link to="/register" class="btn-elegant">
              <span>Explore the Platform</span>
              <div class="btn-line"></div>
            </router-link>
          </div>
        </div>
      </div>

      <div class="scroll-indicator" :style="{ opacity: scrollY > 100 ? 0 : 1 }">
        <div class="mouse"></div>
        <span>Scroll</span>
      </div>
    </section>

    <!-- Value Prop Section -->
    <section class="value-prop section-padding">
      <div class="container">
        <div class="grid-2">
          <div class="prop-content reveal" data-delay="100">
            <h2 class="section-title">Precision <br />at Scale</h2>
            <p class="section-desc">
              From local deliveries to global distribution networks, 13 Maps provides the underlying intelligence to move faster and further.
            </p>
            <div class="stats-minimal">
              <div class="stat-item">
                <span class="val">2ms</span>
                <span class="lab">Response Time</span>
              </div>
              <div class="stat-item">
                <span class="val">10M+</span>
                <span class="lab">Optimizations</span>
              </div>
            </div>
          </div>
          <div class="prop-visual reveal" data-delay="300">
            <div class="visual-wrapper">
              <div class="visual-line v-1"></div>
              <div class="visual-line v-2"></div>
              <div class="visual-line v-3"></div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Minimal -->
    <section class="features-minimal section-padding">
      <div class="container">
        <div class="features-grid-elegant">
          <div class="feature-item-elegant reveal">
            <span class="f-num">01</span>
            <h3>Neural Routing</h3>
            <p>Advanced algorithms that learn from every journey to predict the most efficient path.</p>
          </div>
          <div class="feature-item-elegant reveal" data-delay="200">
            <span class="f-num">02</span>
            <h3>Dynamic API</h3>
            <p>A developer-first interface designed for seamless integration into any tech stack.</p>
          </div>
          <div class="feature-item-elegant reveal" data-delay="400">
            <span class="f-num">03</span>
            <h3>Global Edge</h3>
            <p>Geospatial data served from edge locations for near-zero latency geocoding.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Final Call -->
    <section class="final-call section-padding">
      <div class="container text-center">
        <div class="reveal">
          <h2 class="hero-title mb-lg">Ready to start?</h2>
          <router-link to="/register" class="btn-elegant large">
            <span>Create Account</span>
            <div class="btn-line"></div>
          </router-link>
        </div>
      </div>
    </section>

    <footer class="minimal-footer">
      <div class="container footer-grid">
        <div class="brand-footer">
          <span class="logo">13 Maps</span>
          <p>© 2026 Intelligence in Motion.</p>
        </div>
        <div class="footer-links">
          <router-link to="/privacy">Privacy</router-link>
          <router-link to="/terms">Terms</router-link>
          <router-link to="/support">Support</router-link>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const scrollY = ref(0)
const isMenuOpen = ref(false)
const scrollContainer = ref(null)

const handleScroll = () => {
  scrollY.value = window.scrollY
}

const initReveal = () => {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const delay = entry.target.dataset.delay || 0
        setTimeout(() => {
          entry.target.classList.add('active')
        }, delay)
      }
    })
  }, { threshold: 0.1 })

  document.querySelectorAll('.reveal').forEach(el => observer.observe(el))
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
  initReveal()
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');

.landing-page {
  font-family: 'Outfit', sans-serif;
  background-color: #fcfcfc;
  color: #1a1a1a;
  overflow-x: hidden;
  --clr-primary-rgb: 83, 70, 152;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 40px;
}

/* Minimal Nav */
.minimal-nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 100px;
  display: flex;
  align-items: center;
  z-index: 2500;
  transition: all 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

.minimal-nav.is-scrolled {
  height: 70px;
  background: rgba(252, 252, 252, 0.8);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(0,0,0,0.05);
}

.nav-container {
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 60px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
}

.brand-logo {
  width: 28px;
  height: 28px;
  background: var(--clr-primary);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 12px;
  border-radius: 4px;
}

.brand-name {
  font-weight: 600;
  font-size: 1.1rem;
  letter-spacing: -0.01em;
}

.nav-right {
  display: flex;
  align-items: center;
  gap: 40px;
}

.nav-link {
  font-size: 0.9rem;
  font-weight: 500;
  color: #666;
  transition: color 0.3s;
}

.nav-link:hover { color: var(--clr-primary); }

.menu-toggle {
  background: none;
  border: none;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  gap: 6px;
  z-index: 3000;
  padding: 10px;
}

.line {
  width: 24px;
  height: 2px;
  background: #1a1a1a;
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

.menu-toggle.is-open .line-1 { transform: translateY(4px) rotate(45deg); background: var(--clr-primary); }
.menu-toggle.is-open .line-2 { transform: translateY(-4px) rotate(-45deg); background: var(--clr-primary); }

/* Menu Modal Content */

.menu-modal-container {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background: rgba(252, 252, 252, 0.98);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(0,0,0,0.05);
  padding: 120px 60px 80px 60px;
  z-index: 2001;
  box-shadow: 0 20px 60px rgba(0,0,0,0.1);
}

.menu-grid {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 100px;
  align-items: center;
}

.menu-links {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.menu-item {
  text-decoration: none;
  display: flex;
  align-items: baseline;
  gap: 20px;
  color: #1a1a1a;
  transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.3s;
}

.menu-item:hover { transform: translateX(10px); color: var(--clr-primary); }

.m-num { font-size: 0.9rem; font-weight: 700; color: var(--clr-primary); opacity: 0.6; }
.m-text { font-size: 3.5rem; font-weight: 700; letter-spacing: -0.04em; }

.menu-aside {
  border-left: 1px solid #eee;
  padding-left: 100px;
}

.aside-tag {
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.2em;
  color: var(--clr-primary);
  margin-bottom: 20px;
}

.menu-aside h3 {
  font-size: 1.8rem;
  font-weight: 600;
  line-height: 1.3;
  margin-bottom: 40px;
  letter-spacing: -0.02em;
}

.menu-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.4);
  backdrop-filter: blur(8px);
  z-index: 1500;
  cursor: pointer;
}

/* Transitions */
.menu-slide-enter-active, .menu-slide-leave-active {
  transition: all 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}

.menu-slide-enter-from, .menu-slide-leave-to {
  transform: translateY(-100%);
  opacity: 0;
}

.fade-enter-active, .fade-leave-active { transition: opacity 0.6s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

.cta-minimal {
  font-size: 0.9rem;
  font-weight: 600;
  color: #1a1a1a;
  padding: 8px 20px;
  border: 1px solid #1a1a1a;
  border-radius: 100px;
  transition: all 0.3s;
}

.cta-minimal:hover {
  background: #1a1a1a;
  color: white;
}

/* Hero */
.hero {
  height: 100vh;
  display: flex;
  align-items: center;
  position: relative;
  overflow: hidden;
}

.hero-bg {
  position: absolute;
  top: 0;
  right: -10%;
  width: 60%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 0;
  pointer-events: none;
}

.orbit {
  position: absolute;
  border: 1px solid rgba(83, 70, 152, 0.1);
  border-radius: 50%;
}

.orbit-1 { width: 400px; height: 400px; animation: rotate 40s linear infinite; }
.orbit-2 { width: 600px; height: 600px; animation: rotate 60s linear infinite reverse; }
.orbit-3 { width: 800px; height: 800px; animation: rotate 90s linear infinite; }

.floating-map {
  width: 500px;
  height: 500px;
  opacity: 0.4;
  animation: float 10s ease-in-out infinite;
}

.globe-outline { fill: none; stroke: var(--clr-primary); stroke-width: 0.5; stroke-dasharray: 4 4; }
.globe-meridian, .globe-parallel { fill: none; stroke: var(--clr-primary); stroke-width: 0.3; opacity: 0.5; }
.dot { fill: var(--clr-primary); filter: drop-shadow(0 0 4px var(--clr-primary)); }

@keyframes rotate { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
@keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-20px); } }

.hero-inner { position: relative; z-index: 1; width: 100%; }

.hero-tag {
  font-size: 0.85rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.3em;
  color: var(--clr-primary);
  margin-bottom: 20px;
  opacity: 0.8;
}

.hero-title {
  font-size: clamp(3.5rem, 8vw, 6rem);
  font-weight: 700;
  line-height: 0.95;
  letter-spacing: -0.04em;
  margin-bottom: 30px;
}

.text-thin { font-weight: 300; font-style: italic; }

.hero-sub {
  font-size: 1.25rem;
  color: #666;
  max-width: 500px;
  line-height: 1.6;
  margin-bottom: 50px;
}

.btn-elegant {
  display: inline-flex;
  flex-direction: column;
  color: #1a1a1a;
  text-decoration: none;
  font-weight: 600;
  font-size: 1.1rem;
  gap: 10px;
}

.btn-line {
  height: 1px;
  background: #1a1a1a;
  width: 40px;
  transition: width 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

.btn-elegant:hover .btn-line { width: 100%; }

.scroll-indicator {
  position: absolute;
  bottom: 40px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  transition: opacity 0.5s;
}

.mouse {
  width: 20px;
  height: 35px;
  border: 1px solid #ccc;
  border-radius: 20px;
  position: relative;
}

.mouse::after {
  content: '';
  position: absolute;
  top: 6px;
  left: 50%;
  width: 2px;
  height: 6px;
  background: #1a1a1a;
  transform: translateX(-50%);
  animation: scrollMouse 2s infinite;
}

@keyframes scrollMouse { 0% { opacity: 0; transform: translate(-50%, 0); } 50% { opacity: 1; } 100% { opacity: 0; transform: translate(-50%, 15px); } }

.scroll-indicator span { font-size: 10px; text-transform: uppercase; letter-spacing: 0.2em; color: #999; }

/* Section Generic */
.section-padding { padding: 180px 0; }

.section-title { font-size: 3.5rem; font-weight: 700; line-height: 1; letter-spacing: -0.03em; margin-bottom: 30px; }
.section-desc { font-size: 1.2rem; color: #666; line-height: 1.6; max-width: 450px; margin-bottom: 40px; }

/* Reveal Animations */
.reveal {
  opacity: 0;
  transform: translateY(30px);
  transition: all 1.2s cubic-bezier(0.16, 1, 0.3, 1);
}

.reveal.active {
  opacity: 1;
  transform: translateY(0);
}

/* Value Prop */
.grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 100px; align-items: center; }

.stats-minimal { display: flex; gap: 60px; margin-top: 60px; }
.stat-item { display: flex; flex-direction: column; }
.val { font-size: 2.5rem; font-weight: 700; }
.lab { font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.1em; color: #999; }

.visual-wrapper {
  position: relative;
  height: 400px;
  border-left: 1px solid #eee;
  padding-left: 60px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 40px;
}

.visual-line {
  height: 1px;
  background: linear-gradient(90deg, var(--clr-primary), transparent);
  width: 0;
  transition: width 2s cubic-bezier(0.16, 1, 0.3, 1);
}

.reveal.active .v-1 { width: 100%; transition-delay: 0.2s; }
.reveal.active .v-2 { width: 70%; transition-delay: 0.4s; }
.reveal.active .v-3 { width: 85%; transition-delay: 0.6s; }

/* Features Elegant */
.features-grid-elegant {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 80px;
}

.feature-item-elegant {
  display: flex;
  flex-direction: column;
}

.f-num {
  font-size: 0.9rem;
  font-weight: 700;
  color: var(--clr-primary);
  margin-bottom: 20px;
  display: block;
}

.feature-item-elegant h3 { font-size: 1.5rem; font-weight: 600; margin-bottom: 15px; letter-spacing: -0.01em; }
.feature-item-elegant p { font-size: 1rem; color: #666; line-height: 1.6; }

/* Final Call */
.mb-lg { margin-bottom: 60px; }
.btn-elegant.large { font-size: 2rem; }
.btn-elegant.large .btn-line { height: 2px; width: 60px; }

/* Footer */
.minimal-footer {
  padding: 80px 0;
  border-top: 1px solid #eee;
}

.footer-grid {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.brand-footer .logo { font-weight: 700; font-size: 1.2rem; display: block; margin-bottom: 8px; }
.brand-footer p { font-size: 0.8rem; color: #999; }

.footer-links { display: flex; gap: 30px; }
.footer-links a { font-size: 0.8rem; color: #666; text-decoration: none; }
.footer-links a:hover { color: var(--clr-primary); }

/* Responsive */
@media (max-width: 1024px) {
  .nav-container { padding: 0 40px; }
  .grid-2 { grid-template-columns: 1fr; gap: 60px; }
  .visual-wrapper { height: 200px; }
  .features-grid-elegant { grid-template-columns: 1fr; gap: 60px; }
}

@media (max-width: 768px) {
  .hero-title { font-size: 3rem; }
  .section-title { font-size: 2.5rem; }
  .hero-bg { display: none; }
  .nav-right { display: none; }
}
</style>
