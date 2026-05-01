<template>
  <div class="view-container">
    <div class="view-header">
      <div class="header-text">
        <h1>Account Settings</h1>
        <p>Manage your organization, profile, and system preferences.</p>
      </div>
    </div>

    <div class="settings-grid">
      <!-- Sidebar within Settings -->
      <div class="settings-nav">
        <button 
          v-for="tab in tabs" 
          :key="tab.id"
          :class="['nav-item', { active: activeTab === tab.id }]"
          @click="activeTab = tab.id"
        >
          <component :is="tab.icon" class="icon" />
          <span>{{ tab.name }}</span>
        </button>
      </div>

      <!-- Main Content -->
      <div class="settings-content">
        <div class="card">
          <div class="card-header">
            <h3>{{ currentTabName }}</h3>
            <p>Update your {{ currentTabName.toLowerCase() }} information here.</p>
          </div>
          
          <div class="card-body">
            <div v-if="activeTab === 'profile'" class="form-grid">
              <div class="form-group">
                <label>Full Name</label>
                <input type="text" v-model="profile.name" placeholder="Eyouel T." />
              </div>
              <div class="form-group">
                <label>Email Address</label>
                <input type="email" v-model="profile.email" disabled />
                <span class="hint">Contact support to change your registered email.</span>
              </div>
              <div class="form-group full-width">
                <label>Bio / Description</label>
                <textarea v-model="profile.bio" rows="4" placeholder="Brief description..."></textarea>
              </div>
            </div>

            <div v-if="activeTab === 'org'" class="form-grid">
              <div class="form-group">
                <label>Organization Name</label>
                <input type="text" v-model="org.name" />
              </div>
              <div class="form-group">
                <label>Industry</label>
                <select v-model="org.industry">
                  <option value="logistics">Logistics & Supply Chain</option>
                  <option value="retail">Retail Delivery</option>
                  <option value="service">Field Service</option>
                </select>
              </div>
            </div>

            <div v-if="activeTab === 'notifications'" class="settings-list">
              <div class="setting-item">
                <div class="setting-info">
                  <span class="setting-title">Email Notifications</span>
                  <span class="setting-desc">Receive weekly reports and job completion alerts.</span>
                </div>
                <label class="switch">
                  <input type="checkbox" v-model="notifications.email" />
                  <span class="slider round"></span>
                </label>
              </div>
              <div class="setting-item">
                <div class="setting-info">
                  <span class="setting-title">Push Notifications</span>
                  <span class="setting-desc">Real-time alerts for system status and updates.</span>
                </div>
                <label class="switch">
                  <input type="checkbox" v-model="notifications.push" />
                  <span class="slider round"></span>
                </label>
              </div>
            </div>
          </div>

          <div class="card-footer">
            <button class="btn-primary" @click="saveSettings">Save Changes</button>
            <button class="btn-ghost">Cancel</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, markRaw } from 'vue'

// Basic Icons (SVG Components)
const UserIcon = { template: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>' }
const OrgIcon = { template: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>' }
const NotifIcon = { template: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>' }
const SecurityIcon = { template: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>' }

const activeTab = ref('profile')
const tabs = [
  { id: 'profile', name: 'My Profile', icon: markRaw(UserIcon) },
  { id: 'org', name: 'Organization', icon: markRaw(OrgIcon) },
  { id: 'notifications', name: 'Notifications', icon: markRaw(NotifIcon) },
  { id: 'security', name: 'Security', icon: markRaw(SecurityIcon) },
]

const currentTabName = computed(() => tabs.find(t => t.id === activeTab.value)?.name || '')

const profile = ref({
  name: 'Eyouel T.',
  email: 'admin@13maps.com',
  bio: 'Lead Logistics Administrator at 13 Maps Hub.'
})

const org = ref({
  name: '13 Maps Hub',
  industry: 'logistics'
})

const notifications = ref({
  email: true,
  push: false
})

function saveSettings() {
  alert('Settings saved successfully!')
}
</script>

<script>
// For the markRaw templates to work in this simplified example
export default {
  components: {
    UserIcon: { template: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>' },
    OrgIcon: { template: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>' },
    NotifIcon: { template: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>' },
    SecurityIcon: { template: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>' }
  }
}
</script>

<style scoped>
.view-container {
  padding-top: 12px;
}

.view-header {
  margin-bottom: 24px;
}

.view-header h1 {
  font-size: 20px;
  font-weight: 700;
  color: #0F172A;
  margin-bottom: 4px;
}

.view-header p {
  font-size: 14px;
  color: #64748B;
}

.settings-grid {
  display: grid;
  grid-template-columns: 240px 1fr;
  gap: 24px;
}

.settings-nav {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 16px;
  background: none;
  border: none;
  border-radius: 8px;
  color: #64748B;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  text-align: left;
  transition: all 0.2s;
}

.nav-item:hover {
  background-color: #F1F5F9;
  color: #0F172A;
}

.nav-item.active {
  background-color: #534698;
  color: white;
}

.card {
  background: white;
  border: 1px solid #E2E8F0;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0,0,0,0.02);
}

.card-header {
  padding: 24px;
  border-bottom: 1px solid #F1F5F9;
}

.card-header h3 {
  font-size: 16px;
  font-weight: 700;
  color: #0F172A;
  margin-bottom: 4px;
}

.card-header p {
  font-size: 13px;
  color: #64748B;
}

.card-body {
  padding: 24px;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group.full-width {
  grid-column: span 2;
}

.form-group label {
  font-size: 13px;
  font-weight: 600;
  color: #334155;
}

.form-group input, 
.form-group select, 
.form-group textarea {
  padding: 10px 12px;
  border: 1px solid #E2E8F0;
  border-radius: 8px;
  font-size: 14px;
  background-color: #FAFAFA;
  transition: all 0.2s;
}

.form-group input:focus, 
.form-group select:focus, 
.form-group textarea:focus {
  outline: none;
  border-color: #534698;
  background-color: white;
}

.hint {
  font-size: 11px;
  color: #94A3B8;
}

.settings-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.setting-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  background-color: #FAFAFA;
  border-radius: 12px;
  border: 1px solid #F1F5F9;
}

.setting-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.setting-title {
  font-size: 14px;
  font-weight: 600;
  color: #1E293B;
}

.setting-desc {
  font-size: 12px;
  color: #64748B;
}

.card-footer {
  padding: 16px 24px;
  background-color: #FAFAFA;
  border-top: 1px solid #F1F5F9;
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

.btn-primary {
  padding: 10px 20px;
  background-color: #534698;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary:hover {
  background-color: #41367a;
}

.btn-ghost {
  padding: 10px 20px;
  background: none;
  border: 1px solid #E2E8F0;
  border-radius: 8px;
  color: #475569;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
}

/* Switch Styles */
.switch {
  position: relative;
  display: inline-block;
  width: 44px;
  height: 24px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #CBD5E1;
  transition: .4s;
}

.slider:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: .4s;
}

input:checked + .slider {
  background-color: #534698;
}

input:checked + .slider:before {
  transform: translateX(20px);
}

.slider.round {
  border-radius: 34px;
}

.slider.round:before {
  border-radius: 50%;
}
</style>
