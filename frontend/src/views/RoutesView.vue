<template>
  <div class="map-view-container">
    <div class="sidebar-panel">
      <div class="panel-header">
        <h2>Route Optimizer</h2>
        <p>Click on the map to add delivery points.</p>
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
            {{ loading ? 'Optimizing...' : 'Optimize Route' }}
          </button>
        </div>
      </div>

      <!-- Result Mode -->
      <div v-else class="results-panel">
        <div class="summary-card">
          <div class="summary-item">
            <span class="summary-label">Total Distance</span>
            <span class="summary-value">{{ (optimizedData.distance / 1000).toFixed(2) }} km</span>
          </div>
          <div class="summary-item">
            <span class="summary-label">Estimated Time</span>
            <span class="summary-value">{{ Math.round(optimizedData.duration / 60) }} min</span>
          </div>
        </div>

        <div class="list-header" style="margin-top: 1.5rem;">
          <span>OPTIMIZED SEQUENCE</span>
        </div>
        <ul class="stop-list">
          <li v-for="(stop, i) in optimizedData.stops" :key="stop.sequence" class="stop-item">
            <span class="stop-number active">{{ i + 1 }}</span>
            <div class="stop-info">
              <span class="stop-addr">{{ stop.address }}</span>
            </div>
          </li>
        </ul>

        <div class="actions" style="margin-top: 1rem;">
          <button @click="resetToEdit" class="btn-tool full-width">Reset & Edit</button>
        </div>
      </div>
    </div>

    <div class="map-wrapper">
      <div id="map" class="map-element"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, shallowRef } from 'vue'
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

// State
const map = shallowRef(null)
const locations = ref([])
const markers = shallowRef([])
const routePolyline = shallowRef(null)

const optimizedData = ref(null)
const loading = ref(false)

// Addis Ababa coordinates
const INITIAL_CENTER = [8.9806, 38.7578]
const INITIAL_ZOOM = 12

// Demo locations around Addis Ababa
const DEMO_LOCATIONS = [
  { latitude: 8.9778, longitude: 38.7992, address: "Bole Airport" },
  { latitude: 9.0100, longitude: 38.7350, address: "Mercato" },
  { latitude: 9.0320, longitude: 38.7480, address: "Piazza" },
  { latitude: 8.9950, longitude: 38.7560, address: "Sarbet" }
]

onMounted(() => {
  initMap()
})

onUnmounted(() => {
  if (map.value) {
    map.value.remove()
  }
})

function initMap() {
  map.value = L.map('map').setView(INITIAL_CENTER, INITIAL_ZOOM)

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map.value)

  map.value.on('click', (e) => {
    if (optimizedData.value) return // Don't allow adding while showing results
    
    const lat = e.latlng.lat
    const lng = e.latlng.lng
    addLocation(lat, lng)
  })
}

function addLocation(lat, lng, address = null) {
  locations.value.push({ 
    latitude: lat, 
    longitude: lng,
    address: address || `Stop ${locations.value.length + 1}`
  })
  updateMapMarkers()
}

function removeLocation(index) {
  locations.value.splice(index, 1)
  updateMapMarkers()
}

function updateMapMarkers() {
  // Clear existing markers
  markers.value.forEach(m => m.remove())
  markers.value = []

  // Add new markers
  const pointsToDraw = optimizedData.value ? optimizedData.value.stops : locations.value

  pointsToDraw.forEach((loc, i) => {
    const marker = L.marker([loc.latitude, loc.longitude])
      .bindPopup(`<b>${optimizedData.value ? 'Optimized Stop' : 'Stop'} ${i + 1}</b><br/>${loc.address}`)
      .addTo(map.value)
    
    // Open popup for newly added markers if not optimized
    if (!optimizedData.value && i === pointsToDraw.length - 1) {
      marker.openPopup()
    }
    
    markers.value.push(marker)
  })
}

function loadDemo() {
  clearAll()
  DEMO_LOCATIONS.forEach(loc => addLocation(loc.latitude, loc.longitude, loc.address))
  
  // Auto fit map
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

async function optimizeRoute() {
  if (locations.value.length < 2) return
  
  loading.value = true
  try {
    // Send to the optimization endpoint
    const response = await http.post('/optimize/', {
      locations: locations.value
    })
    
    optimizedData.value = response
    
    // Draw the optimized route using real OSRM geometry
    drawRoute(response.stops, response.geometry)
  } catch (err) {
    console.error("Optimization failed:", err)
    alert("Failed to optimize route. Ensure OSRM is running and you are logged in.")
  } finally {
    loading.value = false
  }
}

function drawRoute(stops, geometry = null) {
  if (routePolyline.value) {
    routePolyline.value.remove()
  }

  updateMapMarkers()

  // Use OSRM geometry if available, otherwise fallback to straight lines
  const latlngs = geometry && geometry.length > 0 
    ? geometry 
    : stops.map(s => [s.latitude, s.longitude])
  
  routePolyline.value = L.polyline(latlngs, {
    color: 'var(--clr-primary, #534698)',
    weight: 5,
    opacity: 0.8,
    dashArray: geometry && geometry.length > 0 ? null : '10, 10' // dashed only for mock
  }).addTo(map.value)

  map.value.fitBounds(routePolyline.value.getBounds(), { padding: [50, 50] })
}
</script>

<style scoped>
.map-view-container {
  display: flex;
  height: calc(100vh - 142px); /* Tighter height to eliminate scrolling */
  background: white;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid #E2E8F0;
  box-shadow: 0 1px 3px rgba(0,0,0,0.02);
}

.sidebar-panel {
  width: 280px;
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
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
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

.btn-remove {
  background: none;
  border: none;
  color: #94A3B8;
  cursor: pointer;
  padding: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
}

.btn-remove:hover {
  background-color: #FEE2E2;
  color: #EF4444;
}

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
  text-align: center;
}

.btn-tool:hover:not(:disabled) {
  background: #FAFAFA;
}

.btn-tool.danger:hover {
  border-color: #FCA5A5;
  color: #EF4444;
}

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
}

.btn-primary-full:hover:not(:disabled) {
  background-color: #41367a;
}

.btn-primary-full:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

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

/* Results Panel */
.summary-card {
  margin: 16px;
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
</style>

