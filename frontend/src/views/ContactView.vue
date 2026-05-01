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
        <p class="hero-tag">Reach Out</p>
        <h1 class="hero-title">Connect with <br /><span class="text-thin">our experts.</span></h1>
        
        <div class="contact-grid">
          <div class="contact-info">
            <div class="info-group">
              <span class="label">General Inquiries</span>
              <a href="mailto:hello@13maps.com" class="link">hello@13maps.com</a>
            </div>
            <div class="info-group">
              <span class="label">Technical Support</span>
              <a href="mailto:dev@13maps.com" class="link">dev@13maps.com</a>
            </div>
            <div class="info-group">
              <span class="label">Headquarters</span>
              <p>Silicon Valley, CA <br />United States</p>
            </div>
          </div>

          <form @submit.prevent class="minimal-form">
            <div class="form-group">
              <input type="text" placeholder="Your Name" class="m-input" />
            </div>
            <div class="form-group">
              <input type="email" placeholder="Your Email" class="m-input" />
            </div>
            <div class="form-group">
              <textarea placeholder="Tell us about your project" class="m-input area"></textarea>
            </div>
            <button class="btn-elegant-form">
              <span>Send Message</span>
              <div class="btn-line"></div>
            </button>
          </form>
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

.contact-grid {
  display: grid;
  grid-template-columns: 2fr 3fr;
  gap: 100px;
}

.info-group {
  margin-bottom: 40px;
}

.label {
  display: block;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: #999;
  margin-bottom: 10px;
}

.link {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1a1a1a;
  text-decoration: none;
  transition: color 0.3s;
}

.link:hover { color: var(--clr-primary); }

.contact-info p {
  font-size: 1.1rem;
  line-height: 1.6;
  color: #666;
}

.minimal-form {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.m-input {
  width: 100%;
  padding: 15px 0;
  background: transparent;
  border: none;
  border-bottom: 1px solid #eee;
  font-family: inherit;
  font-size: 1rem;
  color: #1a1a1a;
  transition: border-color 0.3s;
}

.m-input:focus {
  outline: none;
  border-color: var(--clr-primary);
}

.m-input.area {
  min-height: 120px;
  resize: none;
}

.btn-elegant-form {
  align-self: flex-start;
  display: flex;
  flex-direction: column;
  background: none;
  border: none;
  font-family: inherit;
  font-weight: 700;
  font-size: 1.1rem;
  cursor: pointer;
  gap: 8px;
}

.btn-line {
  height: 2px;
  background: #1a1a1a;
  width: 40px;
  transition: width 0.6s;
}

.btn-elegant-form:hover .btn-line { width: 100%; }

@media (max-width: 768px) {
  .contact-grid { grid-template-columns: 1fr; gap: 60px; }
}
</style>
