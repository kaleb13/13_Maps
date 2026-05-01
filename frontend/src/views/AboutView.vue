<template>
  <div class="minimalist-page">
    <nav class="sub-nav">
      <router-link to="/" class="back-link">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
        <span>Home</span>
      </router-link>
    </nav>

    <main class="container content-area">
      <div class="world-map-bg">
        <img src="@/assets/Flat world map with transparent background.png" alt="World Map" />
      </div>
      
      <div class="reveal active">
        <p class="hero-tag">The Vision</p>
        <h1 class="hero-title">Pioneering <br /><span class="text-thin">Logistics Intelligence.</span></h1>
        <div class="about-grid">
          <div class="text-content">
            <p class="large-p">
              13 Maps was founded on a simple premise: complexity should be invisible. 
              We believe that route optimization is not just about coordinates, but about the flow of time and resources.
            </p>
            <p>
              Our team of engineers and logistics experts work at the intersection of graph theory and real-time data to build the most elegant routing engine on the market.
            </p>
          </div>
          <div class="visual-accent">
            <div class="animated-circle"></div>
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
  transition: opacity 0.3s;
}

.back-link:hover { opacity: 0.6; }

.container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 40px;
  position: relative;
}

.world-map-bg {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 140%;
  opacity: 0.08;
  pointer-events: none;
  z-index: 0;
  filter: grayscale(100%);
  animation: mapReveal 2s ease-out forwards;
}

.world-map-bg img {
  width: 100%;
  height: auto;
}

@keyframes mapReveal {
  from { opacity: 0; transform: translate(-50%, -45%); }
  to { opacity: 0.08; transform: translate(-50%, -50%); }
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

.about-grid {
  display: grid;
  grid-template-columns: 3fr 2fr;
  gap: 80px;
  align-items: center;
}

.large-p {
  font-size: 1.5rem;
  line-height: 1.4;
  margin-bottom: 30px;
  color: #333;
}

.text-content p {
  color: #666;
  line-height: 1.8;
  margin-bottom: 20px;
}

.visual-accent {
  position: relative;
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.animated-circle {
  width: 200px;
  height: 200px;
  border: 1px solid rgba(83, 70, 152, 0.2);
  border-radius: 50%;
  position: relative;
  animation: pulse 4s ease-in-out infinite;
}

.animated-circle::after {
  content: '';
  position: absolute;
  top: -2px;
  left: 50%;
  width: 5px;
  height: 5px;
  background: var(--clr-primary);
  border-radius: 50%;
  transform: translateX(-50%);
}

@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 0.5; }
  50% { transform: scale(1.2); opacity: 1; }
}

.reveal {
  opacity: 0;
  transform: translateY(30px);
  transition: all 1.2s cubic-bezier(0.16, 1, 0.3, 1);
}

.reveal.active {
  opacity: 1;
  transform: translateY(0);
}

@media (max-width: 768px) {
  .about-grid { grid-template-columns: 1fr; }
  .sub-nav { top: 20px; left: 20px; }
}
</style>
