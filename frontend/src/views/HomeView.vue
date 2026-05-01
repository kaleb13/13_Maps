<template>
  <main class="hero flex-center">
    <div class="hero-content">
      <p class="hero-tag text-accent">Route Optimization SaaS</p>
      <h1 class="hero-title">Optimize every journey,<br />at scale.</h1>
      <p class="hero-sub text-muted">
        AI-powered OSRM routing engine. Solve TSP, multi-stop delivery, and fleet logistics in seconds.
      </p>
      <div class="hero-cta flex gap-md">
        <router-link id="cta-register" to="/register" class="btn btn-primary">Get started free</router-link>
        <router-link id="cta-login" to="/login" class="btn btn-ghost">Sign in</router-link>
      </div>
    </div>
    <div class="hero-map-preview">
      <div class="map-mock">
        <div class="route-line" />
        <div v-for="(dot, i) in dots" :key="i" class="route-dot" :style="dot" />
      </div>
    </div>
  </main>
</template>

<script setup>
const dots = [
  { top: '15%',  left: '20%'  },
  { top: '40%',  left: '55%'  },
  { top: '65%',  left: '30%'  },
  { top: '75%',  left: '70%'  },
  { top: '25%',  left: '80%'  },
]
</script>

<style scoped>
.hero {
  min-height: 100vh;
  gap: var(--space-2xl);
  padding: var(--space-2xl);
  background: radial-gradient(ellipse at 70% 40%, rgba(83, 70, 152, 0.1) 0%, transparent 60%),
              radial-gradient(ellipse at 20% 80%, rgba(124, 58, 237, 0.07) 0%, transparent 60%),
              var(--clr-bg);
  flex-wrap: wrap;
  justify-content: center;
}
.hero-content { max-width: 540px; }
.hero-tag { font-size: 0.85rem; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: var(--space-md); }
.hero-title { font-size: clamp(2rem, 5vw, 3.5rem); font-weight: 700; line-height: 1.15; margin-bottom: var(--space-lg); }
.hero-sub { font-size: 1.1rem; margin-bottom: var(--space-xl); max-width: 420px; }
.hero-map-preview {
  width: 380px;
  height: 300px;
  border-radius: var(--radius-lg);
  border: 1px solid var(--clr-border);
  overflow: hidden;
  background: var(--clr-card);
  position: relative;
  box-shadow: var(--shadow-glow);
}
.map-mock {
  width: 100%;
  height: 100%;
  background: repeating-linear-gradient(
    0deg,
    transparent,
    transparent 29px,
    rgba(255,255,255,0.03) 30px
  ),
  repeating-linear-gradient(
    90deg,
    transparent,
    transparent 29px,
    rgba(255,255,255,0.03) 30px
  );
  position: relative;
}
.route-dot {
  position: absolute;
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: var(--clr-accent);
  box-shadow: 0 0 8px var(--clr-accent);
  transform: translate(-50%, -50%);
  animation: pulse 2s ease-in-out infinite;
}
.route-dot:nth-child(even) { animation-delay: 0.5s; background: var(--clr-primary); box-shadow: 0 0 8px var(--clr-primary); }
@keyframes pulse {
  0%, 100% { transform: translate(-50%, -50%) scale(1); opacity: 1; }
  50% { transform: translate(-50%, -50%) scale(1.3); opacity: 0.7; }
}
</style>
