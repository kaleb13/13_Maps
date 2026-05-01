<template>
  <div class="map-view-container">
    <div class="sidebar-panel">
      <div class="panel-header">
        <h2>Route Optimizer</h2>
        <p>Click on the map to add delivery points.</p>
      </div>

      <!-- Movement Mode Selector -->
      <div class="mode-selector">
        <p class="mode-label">MOVEMENT MODE</p>
        <div class="mode-pills">
          <button
            v-for="p in profiles"
            :key="p.key"
            class="mode-pill"
            :class="{ active: selectedProfile === p.key }"
            @click="selectProfile(p.key)"
            :title="p.description"
          >
            <span class="mode-icon">{{ p.icon }}</span>
            <span class="mode-text">{{ p.label }}</span>
          </button>
        </div>
      </div>

      <!-- Input Mode -->
      <div v-if="!optimizedData" class="locations-list">
        <div class="list-header">
          <span>STOPS ({{ locations.length }})</span>
        </div>
        <ul v-if="locations.length > 0" class="stop-list">
          <li v-for="(loc, i) in locations" :key="i" class="stop-item">
            <span class="stop-number">{{ i + 1 }}</span>
            <div class="stop-info">
              <span class="stop-addr">{{ loc.address }}</span>
              <span class="stop-coords">{{ loc.latitude.toFixed(4) }}, {{ loc.longitude.toFixed(4) }}</span>
            </div>
            <button @click="removeLocation(i)" class="btn-remove" title="Remove stop">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
            </button>
          </li>
        </ul>
        <div v-else class="empty-state">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#E2E8F0" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
          <p>No stops added yet.</p>
        </div>

        <div class="actions">
          <button @click="loadDemo" class="btn-tool">Load Demo</button>
          <button @click="clearAll" class="btn-tool danger" :disabled="locations.length === 0">Clear</button>
          <button 
            @click="optimizeRoute" 
            class="btn-primary-full" 
            :disabled="locations.length < 2 || loading"
          >
            <span v-if="loading" class="btn-loading">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="spin"><path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/></svg>
              Optimizing...
            </span>
            <span v-else>
              {{ activeProfile.icon }} Optimize Route
            </span>
          </button>
        </div>
      </div>

      <!-- Result Mode -->
      <div v-else class="results-panel">
        <!-- Active Mode Badge -->
        <div class="active-mode-badge">
          <span class="mode-badge-icon">{{ optimizedData.profile_icon }}</span>
          <span class="mode-badge-text">{{ optimizedData.profile_label }} Route</span>
        </div>

        <div class="summary-card">
          <div class="summary-item">
            <span class="summary-label">Total Distance</span>
            <span class="summary-value">{{ (optimizedData.distance / 1000).toFixed(2) }} km</span>
          </div>
          <div class="summary-item">
            <span class="summary-label">Estimated Time</span>
            <span class="summary-value">{{ formatDuration(optimizedData.duration) }}</span>
          </div>
        </div>

        <div class="list-header" style="margin-top: 1rem;">
          <span>OPTIMIZED SEQUENCE</span>
        </div>
        <ul class="stop-list">
          <li v-for="(stop, i) in optimizedData.stops" :key="stop.sequence" class="stop-item">
            <span class="stop-number active">{{ i + 1 }}</span>
            <div class="stop-info">
              <span class="stop-addr">{{ stop.address }}</span>
              <span v-if="stop.eta" class="eta-badge">
                ETA: {{ formatETA(stop.eta) }}
              </span>
            </div>
          </li>
        </ul>

        <div class="actions" style="margin-top: 1rem;">
          <button @click="resetToEdit" class="btn-tool full-width">↩ Reset & Edit</button>
        </div>
      </div>
    </div>

    <div class="map-wrapper">
      <!-- Map Mode Indicator (visible on map) -->
      <div v-if="optimizedData" class="map-mode-indicator">
        <span>{{ optimizedData.profile_icon }}</span>
        <span>{{ optimizedData.profile_label }}</span>
      </div>
      <div id="map" class="map-element"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, shallowRef } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import http from '@/api/http'

// Fix Leaflet's default icon paths in Vite
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});

// ─── State ────────────────────────────────────────────────────────────────────
const map = shallowRef(null)
const locations = ref([])
const markers = shallowRef([])
const routePolyline = shallowRef(null)
const optimizedData = ref(null)
const loading = ref(false)

// ─── Movement Profiles ────────────────────────────────────────────────────────
// Hardcoded defaults that mirror the backend registry.
// On mount we'll try to fetch from /optimize/profiles for the source of truth.
const DEFAULT_PROFILES = [
  { key: 'driving', label: 'Driving', icon: '🚗', description: 'Optimized for motor vehicles' },
  { key: 'cycling', label: 'Cycling', icon: '🚴', description: 'Optimized for bicycles' },
  { key: 'walking', label: 'Walking', icon: '🚶', description: 'Optimized for pedestrians' },
]

const profiles = ref(DEFAULT_PROFILES)
const selectedProfile = ref('driving')

const activeProfile = computed(() =>
  profiles.value.find(p => p.key === selectedProfile.value) || DEFAULT_PROFILES[0]
)

// Polyline colors per profile for visual distinction on map
const PROFILE_COLORS = {
  driving: '#534698',
  cycling: '#16A34A',
  walking: '#EA580C',
}

// ─── Map Constants ─────────────────────────────────────────────────────────────
const INITIAL_CENTER = [8.9806, 38.7578]
const INITIAL_ZOOM = 12

const DEMO_LOCATIONS = [
  { latitude: 8.9778, longitude: 38.7992, address: "Bole Airport" },
  { latitude: 9.0100, longitude: 38.7350, address: "Mercato" },
  { latitude: 9.0320, longitude: 38.7480, address: "Piazza" },
  { latitude: 8.9950, longitude: 38.7560, address: "Sarbet" }
]

// ─── Lifecycle ─────────────────────────────────────────────────────────────────
onMounted(async () => {
  initMap()
  await loadProfiles()
})

onUnmounted(() => {
  if (map.value) map.value.remove()
})

// ─── Profile Selector ──────────────────────────────────────────────────────────
async function loadProfiles() {
  try {
    const res = await http.get('/optimize/profiles')
    if (res?.profiles?.length) {
      profiles.value = res.profiles
    }
  } catch {
    // Falls back to DEFAULT_PROFILES already set
  }
}

function selectProfile(key) {
  if (selectedProfile.value === key) return
  selectedProfile.value = key

  // If results are showing, recalculate with the new mode
  if (optimizedData.value) {
    recalculate()
  }
}

async function recalculate() {
  // Keep current locations (from optimized stops) and re-run
  if (optimizedData.value?.stops?.length >= 2) {
    const currentLocs = optimizedData.value.stops.map(s => ({
      latitude: s.latitude,
      longitude: s.longitude,
      address: s.address,
    }))
    optimizedData.value = null
    if (routePolyline.value) {
      routePolyline.value.remove()
      routePolyline.value = null
    }
    locations.value = currentLocs
    updateMapMarkers()
    await optimizeRoute()
  }
}

// ─── Map Functions ─────────────────────────────────────────────────────────────
function initMap() {
  map.value = L.map('map').setView(INITIAL_CENTER, INITIAL_ZOOM)

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map.value)

  map.value.on('click', (e) => {
    if (optimizedData.value) return
    addLocation(e.latlng.lat, e.latlng.lng)
  })
}

async function addLocation(lat, lng, address = null) {
  const index = locations.value.length;
  const defaultName = `Stop ${index + 1}`;
  
  if (address) {
    locations.value.push({ latitude: lat, longitude: lng, address });
    updateMapMarkers();
    return;
  }
  
  locations.value.push({ latitude: lat, longitude: lng, address: `${defaultName} (Loading...)` });
  updateMapMarkers();
  
  try {
    const res = await http.get(`/geocode/reverse?lat=${lat}&lon=${lng}`);
    if (res?.display_name) {
      const parts = res.display_name.split(',');
      const placeName = parts.slice(0, Math.min(3, parts.length)).join(',').trim();
      locations.value[index].address = `${defaultName} (${placeName})`;
    } else {
      locations.value[index].address = defaultName;
    }
  } catch {
    locations.value[index].address = defaultName;
  }
  
  updateMapMarkers();
}

function removeLocation(index) {
  locations.value.splice(index, 1)
  updateMapMarkers()
}

function updateMapMarkers() {
  markers.value.forEach(m => m.remove())
  markers.value = []

  const pointsToDraw = optimizedData.value ? optimizedData.value.stops : locations.value

  pointsToDraw.forEach((loc, i) => {
    const marker = L.marker([loc.latitude, loc.longitude])
      .bindPopup(`<b>${optimizedData.value ? 'Optimized Stop' : 'Stop'} ${i + 1}</b><br/>${loc.address}`)
      .addTo(map.value)
    
    if (!optimizedData.value && i === pointsToDraw.length - 1) {
      marker.openPopup()
    }
    
    markers.value.push(marker)
  })
}

function loadDemo() {
  clearAll()
  DEMO_LOCATIONS.forEach(loc => addLocation(loc.latitude, loc.longitude, loc.address))
  
  const group = new L.featureGroup(markers.value)
  map.value.fitBounds(group.getBounds(), { padding: [50, 50] })
}

function clearAll() {
  locations.value = []
  optimizedData.value = null
  updateMapMarkers()
  if (routePolyline.value) {
    routePolyline.value.remove()
    routePolyline.value = null
  }
}

function resetToEdit() {
  optimizedData.value = null
  if (routePolyline.value) {
    routePolyline.value.remove()
    routePolyline.value = null
  }
  updateMapMarkers()
}

// ─── Optimization ──────────────────────────────────────────────────────────────
async function optimizeRoute() {
  if (locations.value.length < 2) return
  
  loading.value = true
  try {
    const response = await http.post('/optimize/', {
      locations: locations.value,
      profile: selectedProfile.value,
    })
    
    optimizedData.value = response
    drawRoute(response.stops, response.geometry, response.profile)
  } catch (err) {
    console.error("Optimization failed:", err)
    alert("Failed to optimize route. Ensure OSRM is running and you are logged in.")
  } finally {
    loading.value = false
  }
}

function drawRoute(stops, geometry = null, profile = 'driving') {
  if (routePolyline.value) routePolyline.value.remove()

  updateMapMarkers()

  const latlngs = geometry?.length > 0
    ? geometry
    : stops.map(s => [s.latitude, s.longitude])
  
  const color = PROFILE_COLORS[profile] || PROFILE_COLORS.driving

  routePolyline.value = L.polyline(latlngs, {
    color,
    weight: 5,
    opacity: 0.85,
    dashArray: geometry?.length > 0 ? null : '10, 10'
  }).addTo(map.value)

  map.value.fitBounds(routePolyline.value.getBounds(), { padding: [50, 50] })
}

// ─── Formatters ────────────────────────────────────────────────────────────────
function formatETA(isoString) {
  if (!isoString) return '';
  return new Date(isoString).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function formatDuration(seconds) {
  if (!seconds) return '—';
  const h = Math.floor(seconds / 3600);
  const m = Math.round((seconds % 3600) / 60);
  if (h > 0) return `${h}h ${m}m`;
  return `${m} min`;
}
</script>

<style scoped>
.map-view-container {
  display: flex;
  height: calc(100vh - 142px);
  background: white;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid #E2E8F0;
  box-shadow: 0 1px 3px rgba(0,0,0,0.02);
}

.sidebar-panel {
  width: 300px;
  background: white;
  border-right: 1px solid #E2E8F0;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  z-index: 10;
}

.panel-header {
  padding: 20px;
  border-bottom: 1px solid #F1F5F9;
}

.panel-header h2 {
  font-size: 16px;
  font-weight: 700;
  color: #0F172A;
  margin-bottom: 4px;
}

.panel-header p {
  font-size: 12px;
  color: #64748B;
}

/* ── Movement Mode Selector ─────────────────────────────────────────────────── */
.mode-selector {
  padding: 14px 16px;
  border-bottom: 1px solid #F1F5F9;
  background: #FAFAFA;
}

.mode-label {
  font-size: 10px;
  font-weight: 700;
  color: #94A3B8;
  letter-spacing: 0.08em;
  margin-bottom: 10px;
}

.mode-pills {
  display: flex;
  gap: 6px;
}

.mode-pill {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 10px 6px;
  background: white;
  border: 1.5px solid #E2E8F0;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  font-size: 11px;
  font-weight: 600;
  color: #64748B;
}

.mode-pill:hover {
  border-color: #CBD5E1;
  background: #F8FAFC;
}

.mode-pill.active {
  border-color: #534698;
  background: rgba(83, 70, 152, 0.05);
  color: #534698;
  box-shadow: 0 2px 8px rgba(83, 70, 152, 0.1);
}

.mode-pill.active .mode-icon {
  transform: scale(1.2);
}

.mode-icon {
  font-size: 18px;
  transition: transform 0.2s;
}

.mode-text {
  font-size: 11px;
  font-weight: 700;
}

/* ── List ─────────────────────────────────────────────────────────────────── */
.list-header {
  padding: 12px 20px;
  background-color: #FAFAFA;
  font-size: 11px;
  font-weight: 700;
  color: #94A3B8;
  letter-spacing: 0.05em;
}

.map-wrapper {
  flex: 1;
  position: relative;
}

.map-element {
  position: absolute;
  inset: 0;
  z-index: 1;
}

.stop-list {
  list-style: none;
  padding: 12px 16px;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.stop-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px;
  background: #FAFAFA;
  border: 1px solid #E2E8F0;
  border-radius: 8px;
  transition: all 0.2s;
}

.stop-item:hover {
  border-color: #CBD5E1;
  background: white;
}

.stop-number {
  width: 24px;
  height: 24px;
  border-radius: 6px;
  background: #E2E8F0;
  color: #64748B;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 11px;
  flex-shrink: 0;
}

.stop-number.active {
  background: #534698;
  color: white;
}

.stop-info {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-width: 0;
}

.stop-addr {
  font-size: 13px;
  font-weight: 600;
  color: #1E293B;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.stop-coords {
  font-size: 11px;
  color: #94A3B8;
}

.eta-badge {
  font-size: 11px;
  font-weight: 700;
  color: #534698;
  margin-top: 2px;
}

.btn-remove {
  background: none;
  border: none;
  color: #94A3B8;
  cursor: pointer;
  padding: 4px;
  display: flex;
  align-items: center;
  border-radius: 4px;
}

.btn-remove:hover {
  background-color: #FEE2E2;
  color: #EF4444;
}

/* ── Actions ────────────────────────────────────────────────────────────────── */
.actions {
  padding: 16px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  border-top: 1px solid #F1F5F9;
  margin-top: auto;
}

.btn-tool {
  flex: 1;
  padding: 9px;
  background: white;
  border: 1px solid #E2E8F0;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  color: #475569;
  cursor: pointer;
}

.btn-tool:hover:not(:disabled) { background: #FAFAFA; }
.btn-tool.danger:hover { border-color: #FCA5A5; color: #EF4444; }

.btn-primary-full {
  width: 100%;
  padding: 12px;
  background-color: #534698;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.btn-primary-full:hover:not(:disabled) { background-color: #41367a; }
.btn-primary-full:disabled { opacity: 0.5; cursor: not-allowed; }

.btn-loading {
  display: flex;
  align-items: center;
  gap: 8px;
}

.spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* ── Empty State ────────────────────────────────────────────────────────────── */
.empty-state {
  padding: 40px 20px;
  text-align: center;
  color: #94A3B8;
}

.empty-state p {
  font-size: 13px;
  margin-top: 8px;
}

.full-width { width: 100%; }

/* ── Results Panel ──────────────────────────────────────────────────────────── */
.active-mode-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 16px 16px 0 16px;
  padding: 10px 14px;
  background: rgba(83, 70, 152, 0.06);
  border: 1.5px solid rgba(83, 70, 152, 0.2);
  border-radius: 10px;
  font-size: 14px;
  font-weight: 700;
  color: #534698;
}

.mode-badge-icon { font-size: 18px; }

.summary-card {
  margin: 12px 16px;
  background: #FAFAFA;
  border: 1px solid #E2E8F0;
  border-radius: 12px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.summary-label {
  font-size: 12px;
  font-weight: 600;
  color: #64748B;
}

.summary-value {
  font-weight: 700;
  font-size: 16px;
  color: #0F172A;
}

/* ── Map Overlay Indicator ──────────────────────────────────────────────────── */
.map-mode-indicator {
  position: absolute;
  top: 16px;
  right: 16px;
  z-index: 500;
  display: flex;
  align-items: center;
  gap: 6px;
  background: white;
  border: 1px solid #E2E8F0;
  border-radius: 100px;
  padding: 6px 14px;
  font-size: 13px;
  font-weight: 700;
  color: #1E293B;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
</style>
