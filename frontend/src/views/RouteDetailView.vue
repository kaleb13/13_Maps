<template>
  <section>
    <router-link to="/dashboard/routes" class="btn btn-ghost" style="margin-bottom:var(--space-lg)">
      ← Back to Routes
    </router-link>

    <div v-if="store.loading" class="text-muted">Loading…</div>
    <template v-else-if="store.currentRoute">
      <div class="route-detail-header">
        <h2>{{ store.currentRoute.name }}</h2>
        <span :class="`badge badge-${store.currentRoute.status}`">{{ store.currentRoute.status }}</span>
      </div>

      <!-- Waypoints -->
      <div class="card" style="margin-top:var(--space-lg)">
        <h3 style="margin-bottom:var(--space-md)">Waypoints</h3>
        <div class="wp-table">
          <div class="wp-row wp-header text-muted">
            <span>#</span><span>Latitude</span><span>Longitude</span><span>Label</span>
          </div>
          <div v-for="wp in store.currentRoute.waypoints" :key="wp.id" class="wp-row">
            <span>{{ wp.sequence + 1 }}</span>
            <span>{{ wp.latitude }}</span>
            <span>{{ wp.longitude }}</span>
            <span>{{ wp.label || '—' }}</span>
          </div>
        </div>
      </div>

      <!-- Optimize -->
      <div class="card" style="margin-top:var(--space-lg)">
        <h3 style="margin-bottom:var(--space-md)">Run Optimization</h3>
        <div class="flex gap-md" style="align-items:flex-end;flex-wrap:wrap">
          <div class="form-group">
            <label for="opt-profile">Profile</label>
            <select id="opt-profile" v-model="profile" class="input" style="width:160px">
              <option value="driving">Driving</option>
              <option value="cycling">Cycling</option>
              <option value="walking">Walking</option>
            </select>
          </div>
          <div class="form-group">
            <label for="opt-algorithm">Algorithm</label>
            <select id="opt-algorithm" v-model="algorithm" class="input" style="width:160px">
              <option value="osrm_trip">OSRM Trip (TSP)</option>
              <option value="osrm_route">OSRM Route</option>
            </select>
          </div>
          <button id="btn-optimize" class="btn btn-primary" :disabled="optimizing" @click="optimize">
            {{ optimizing ? 'Submitting…' : '⚡ Optimize' }}
          </button>
        </div>
        <p v-if="optimizeMsg" class="text-accent" style="margin-top:var(--space-md);font-size:0.875rem">
          {{ optimizeMsg }}
        </p>
      </div>
    </template>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useRoutesStore } from '@/stores/routes'
import { optimizeApi } from '@/api/routes'

const route      = useRoute()
const store      = useRoutesStore()
const profile    = ref('driving')
const algorithm  = ref('osrm_trip')
const optimizing = ref(false)
const optimizeMsg = ref(null)

onMounted(() => store.fetchRoute(route.params.id))

async function optimize() {
  optimizing.value  = true
  optimizeMsg.value = null
  try {
    const job = await optimizeApi.submit(route.params.id, profile.value, algorithm.value)
    optimizeMsg.value = `✅ Job ${job.id.slice(0, 8)}… submitted. Check the Jobs tab for results.`
  } catch (err) {
    optimizeMsg.value = `❌ ${err.message}`
  } finally {
    optimizing.value = false
  }
}
</script>

<style scoped>
.route-detail-header { display: flex; align-items: center; gap: var(--space-md); }
.wp-table { display: grid; gap: 2px; }
.wp-row {
  display: grid;
  grid-template-columns: 40px 1fr 1fr 1fr;
  gap: var(--space-md);
  padding: 0.5rem 0;
  border-bottom: 1px solid var(--clr-border);
  font-size: 0.875rem;
}
.wp-header { font-weight: 600; font-size: 0.75rem; text-transform: uppercase; }
</style>
