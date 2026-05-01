<template>
  <div class="view-container">
    <div class="view-header">
      <div class="header-text">
        <h1>Optimization Job List</h1>
        <p>The definitions of route optimization tasks, algorithms, and execution history.</p>
      </div>
      <div class="header-actions">
        <router-link to="/dashboard/routes" class="btn-action primary">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
          Create Job
        </router-link>
      </div>
    </div>

    <div class="table-card">
      <div class="table-tools">
        <div class="search-wrapper">
          <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
          <input type="text" placeholder="Search jobs..." v-model="searchQuery" />
        </div>
        <button class="btn-tool">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 3H2l8 9v6l4 2v-8l8-9z"/></svg>
          Filter
        </button>
      </div>

      <div class="table-container">
        <table class="data-table">
          <thead>
            <tr>
              <th>Job ID</th>
              <th>Algorithm</th>
              <th>Status</th>
              <th>Distance</th>
              <th>Duration</th>
              <th>Created At</th>
              <th class="text-right">Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="loading">
              <td colspan="7" class="loading-state">Loading data...</td>
            </tr>
            <tr v-else-if="filteredJobs.length === 0">
              <td colspan="7" class="empty-state">No jobs found.</td>
            </tr>
            <tr v-for="job in filteredJobs" :key="job.id">
              <td class="font-bold">{{ job.id.slice(0, 8).toUpperCase() }}</td>
              <td>
                <span class="algo-badge">{{ job.algorithm }}</span>
              </td>
              <td>
                <span :class="['status-badge', job.status]">{{ job.status }}</span>
              </td>
              <td>{{ job.total_distance_m ? (job.total_distance_m / 1000).toFixed(2) + ' km' : '-' }}</td>
              <td>{{ job.total_duration_s ? formatDuration(job.total_duration_s) : '-' }}</td>
              <td class="text-muted">{{ formatDate(job.created_at) }}</td>
              <td class="text-right">
                <button class="btn-icon-only">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="1"/><circle cx="12" cy="5" r="1"/><circle cx="12" cy="19" r="1"/></svg>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="table-footer">
        <div class="footer-info">
          Showing 1 to {{ filteredJobs.length }} of {{ jobs.length }} entries
        </div>
        <div class="pagination">
          <div class="per-page">
            Per Page: 
            <select v-model="perPage">
              <option :value="10">10</option>
              <option :value="25">25</option>
              <option :value="50">50</option>
            </select>
          </div>
          <div class="page-controls">
            <button class="btn-page" disabled>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"/></svg>
              Previous
            </button>
            <button class="btn-page active">1</button>
            <button class="btn-page" disabled>
              Next
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { jobsApi } from '@/api/routes'

const jobs = ref([])
const loading = ref(false)
const searchQuery = ref('')
const perPage = ref(10)

onMounted(async () => {
  loading.value = true
  try {
    jobs.value = await jobsApi.list()
  } catch (err) {
    console.error("Failed to load jobs", err)
  } finally {
    loading.value = false
  }
})

const filteredJobs = computed(() => {
  if (!searchQuery.value) return jobs.value
  const q = searchQuery.value.toLowerCase()
  return jobs.value.filter(j => 
    j.id.toLowerCase().includes(q) || 
    j.algorithm.toLowerCase().includes(q) ||
    j.status.toLowerCase().includes(q)
  )
})

function formatDate(iso) {
  return new Date(iso).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

function formatDuration(seconds) {
  const m = Math.floor(seconds / 60)
  const s = Math.round(seconds % 60)
  return m > 0 ? `${m}m ${s}s` : `${s}s`
}
</script>

<style scoped>
.view-container {
  padding-top: 12px;
}

.view-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 24px;
}

.header-text h1 {
  font-size: 20px;
  font-weight: 700;
  color: #0F172A;
  margin-bottom: 4px;
}

.header-text p {
  font-size: 14px;
  color: #64748B;
}

.btn-action {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 700;
  text-decoration: none;
  transition: all 0.2s;
}

.btn-action.primary {
  background-color: #534698;
  color: white;
}

.btn-action.primary:hover {
  background-color: #41367a;
  box-shadow: 0 4px 12px rgba(83, 70, 152, 0.2);
}

.table-card {
  background-color: white;
  border: 1px solid #E2E8F0;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0,0,0,0.02);
}

.table-tools {
  padding: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #F1F5F9;
}

.search-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  width: 300px;
}

.search-icon {
  position: absolute;
  left: 12px;
  color: #94A3B8;
}

.search-wrapper input {
  width: 100%;
  padding: 9px 12px 9px 40px;
  background-color: #FAFAFA;
  border: 1px solid #E2E8F0;
  border-radius: 8px;
  font-size: 14px;
  transition: all 0.2s;
}

.search-wrapper input:focus {
  outline: none;
  border-color: #0047AB;
  background-color: white;
}

.btn-tool {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 9px 16px;
  background-color: white;
  border: 1px solid #E2E8F0;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  color: #475569;
  cursor: pointer;
}

.btn-tool:hover {
  background-color: #FAFAFA;
}

.table-container {
  overflow-x: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

.data-table th {
  padding: 12px 16px;
  font-size: 12px;
  font-weight: 700;
  color: #64748B;
  background-color: #FAFAFA;
  border-bottom: 1px solid #F1F5F9;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.data-table td {
  padding: 16px;
  font-size: 14px;
  color: #1E293B;
  border-bottom: 1px solid #F1F5F9;
}

.data-table tr:hover {
  background-color: #FAFAFA;
}

.font-bold { font-weight: 700; }
.text-muted { color: #64748B; }
.text-right { text-align: right; }

.algo-badge {
  background-color: #F1F5F9;
  color: #475569;
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
}

.status-badge {
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
}

.status-badge.completed { background-color: #DCFCE7; color: #166534; }
.status-badge.pending { background-color: #FEF9C3; color: #854D0E; }
.status-badge.running { background-color: #E0E7FF; color: #3730A3; }
.status-badge.failed { background-color: #FEE2E2; color: #991B1B; }

.btn-icon-only {
  width: 32px;
  height: 32px;
  border: none;
  background: transparent;
  color: #94A3B8;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  cursor: pointer;
}

.btn-icon-only:hover {
  background-color: #F1F5F9;
  color: #0F172A;
}

.table-footer {
  padding: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #FFFFFF;
}

.footer-info {
  font-size: 13px;
  color: #64748B;
}

.pagination {
  display: flex;
  align-items: center;
  gap: 24px;
}

.per-page {
  font-size: 13px;
  color: #64748B;
  display: flex;
  align-items: center;
  gap: 8px;
}

.per-page select {
  padding: 4px 8px;
  border-radius: 6px;
  border: 1px solid #E2E8F0;
  background-color: white;
  outline: none;
}

.page-controls {
  display: flex;
  align-items: center;
  gap: 4px;
}

.btn-page {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border: 1px solid #E2E8F0;
  background-color: white;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 600;
  color: #475569;
  cursor: pointer;
}

.btn-page:hover:not(:disabled) {
  background-color: #FAFAFA;
}

.btn-page.active {
  background-color: #534698;
  border-color: #534698;
  color: white;
}

.btn-page:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.loading-state, .empty-state {
  text-align: center;
  padding: 40px;
  color: #94A3B8;
}
</style>
