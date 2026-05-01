<template>
  <div class="app-layout">
    <!-- Side Bar -->
    <aside class="side-bar" :class="{ collapsed: isSidebarCollapsed }">
      <div class="side-bar-main">
        <!-- Org Switcher -->
        <div class="org-switcher" data-tooltip="Switch Organization">
          <div class="org-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>
          </div>
          <div class="org-info">
            <span class="org-name">13 Maps Hub</span>
            <span class="org-subtext">Logistics Admin</span>
          </div>
          <svg class="chevron" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M7 15l5 5 5-5M7 9l5-5 5 5"/></svg>
        </div>

        <!-- Overview Section -->
        <div class="menu-section">
          <p class="section-label">OVERVIEW</p>
          <nav class="nav-group">
            <router-link to="/dashboard" class="nav-link" exact data-tooltip="Dashboard">
              <svg class="nav-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>
              <span>Dashboard</span>
            </router-link>
          </nav>
        </div>

        <!-- Logistics Section -->
        <div class="menu-section">
          <p class="section-label">LOGISTICS OPS</p>
          <nav class="nav-group">
            <router-link to="/dashboard/routes" class="nav-link" data-tooltip="Route Management">
              <svg class="nav-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
              <span>Route Management</span>
            </router-link>
            <router-link to="/dashboard/jobs" class="nav-link" data-tooltip="Optimization Jobs">
              <svg class="nav-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>
              <span>Optimization Jobs</span>
            </router-link>
          </nav>
        </div>

        <!-- System Section -->
        <div class="menu-section">
          <p class="section-label">SYSTEM CONFIG</p>
          <nav class="nav-group">
            <router-link to="/dashboard/settings" class="nav-link" data-tooltip="Settings">
              <svg class="nav-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
              <span>Settings</span>
            </router-link>
            <router-link to="/dashboard/help" class="nav-link" data-tooltip="Help & Support">
              <svg class="nav-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
              <span>Help & Support</span>
            </router-link>
          </nav>
        </div>
        <div class="side-bar-spacer"></div>
      </div>

      <!-- No Footer Menu - Logout moved to User Menu in Top Bar -->
      
      <!-- Resizer Handle -->
      <div class="sidebar-resizer" @click="toggleSidebar"></div>
    </aside>

    <!-- Main Section -->
    <div class="main-container">
      <!-- Top Bar -->
      <header class="top-bar">
        <button class="icon-btn sidebar-toggle" @click="toggleSidebar" :title="isSidebarCollapsed ? 'Expand Sidebar' : 'Collapse Sidebar'">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect width="18" height="18" x="3" y="3" rx="2" />
            <path d="M9 3v18" />
          </svg>
        </button>
        <div class="search-box">
          <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
          <input ref="searchInput" type="text" placeholder="Search Everything..." />
          <span class="search-hint">/</span>
        </div>

        <div class="top-bar-right">
          <div class="action-icons">
            <button class="icon-btn" title="Full Screen">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"/></svg>
            </button>
            <button class="icon-btn" title="Theme">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
            </button>
            <button class="icon-btn" title="Language">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>
            </button>
            <div class="notification-btn">
              <button class="icon-btn"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg></button>
              <span class="notif-badge">2</span>
            </div>
          </div>
          <div class="divider-v"></div>
          <div class="user-menu-wrapper">
            <!-- Transparent overlay to close menu -->
            <div v-if="isUserMenuOpen" class="menu-overlay" @click="isUserMenuOpen = false"></div>

            <button class="user-trigger" @click="toggleUserMenu">
              <div class="user-avatar-sm">ET</div>
              <span class="user-name-sm">Eyouel T.</span>
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg>
            </button>

            <transition name="fade">
              <div v-if="isUserMenuOpen" class="user-dropdown">
                <div class="dropdown-header">
                  <p class="dropdown-user-name">Eyouel T.</p>
                  <p class="dropdown-user-email">admin@13maps.com</p>
                </div>
                <div class="dropdown-divider"></div>
                <router-link to="/dashboard/profile" class="dropdown-item" @click="isUserMenuOpen = false">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                  <span>My Profile</span>
                </router-link>
                <router-link to="/dashboard/settings" class="dropdown-item" @click="isUserMenuOpen = false">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
                  <span>Settings</span>
                </router-link>
                <div class="dropdown-divider"></div>
                <button @click="handleLogout" class="dropdown-item logout">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
                  <span>Logout</span>
                </button>
              </div>
            </transition>
          </div>
        </div>
      </header>

      <!-- Breadcrumbs & Content Area -->
      <main class="page-content">
        <nav class="breadcrumbs">
          <div v-for="(crumb, index) in breadcrumbs" :key="index" class="crumb-item">
            <router-link v-if="index < breadcrumbs.length - 1" :to="crumb.path" class="crumb-link">
              <svg v-if="index === 0" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>
              <span v-else>{{ crumb.name }}</span>
            </router-link>
            <span v-else class="current-crumb">
              <svg v-if="index === 0" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>
              <span v-else>{{ crumb.name }}</span>
            </span>
            <svg v-if="index < breadcrumbs.length - 1" class="crumb-separator" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg>
          </div>
        </nav>

        <div class="router-view-container">
          <router-view />
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const isSidebarCollapsed = ref(false)
const isUserMenuOpen = ref(false)
const searchInput = ref(null)

const breadcrumbs = computed(() => {
  const crumbs = [{ name: 'Dashboard', path: '/dashboard' }]
  
  // Mapping of route names to user-friendly sidebar titles
  const routeMap = {
    'Routes': 'Route Management',
    'RouteDetail': 'Route Management',
    'Jobs': 'Optimization Jobs',
    'Settings': 'Settings',
    'Help': 'Help and Support'
  }

  const currentName = route.name
  if (currentName && currentName !== 'Dashboard' && currentName !== 'DashboardOverview') {
    crumbs.push({ 
      name: routeMap[currentName] || currentName, 
      path: currentName.includes('Detail') ? route.matched[route.matched.length - 2]?.path || '/dashboard' : route.path 
    })
    
    // Handle Detail Pages
    if (currentName === 'RouteDetail' && route.params.id) {
      crumbs.push({ name: `Route #${route.params.id}`, path: route.path })
    }
  }
  
  return crumbs
})

function toggleSidebar() {
  isSidebarCollapsed.value = !isSidebarCollapsed.value
  if (isUserMenuOpen.value) isUserMenuOpen.value = false
}

function toggleUserMenu() {
  isUserMenuOpen.value = !isUserMenuOpen.value
}

function handleLogout() {
  auth.logout()
  router.push('/login')
}

// Global shortcut for search
const handleGlobalKeydown = (e) => {
  if (e.key === '/' && document.activeElement.tagName !== 'INPUT' && document.activeElement.tagName !== 'TEXTAREA') {
    e.preventDefault()
    searchInput.value?.focus()
  }
  if (e.key === 'Escape' && isUserMenuOpen.value) {
    isUserMenuOpen.value = false
  }
}

onMounted(() => {
  window.addEventListener('keydown', handleGlobalKeydown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleGlobalKeydown)
})
</script>

<style scoped>
.app-layout {
  display: flex;
  height: 100vh;
  width: 100vw;
  background-color: #FAFAFA;
  overflow: hidden;
}

/* --- Sidebar --- */
.side-bar {
  width: 260px;
  background-color: #FFFFFF;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: visible; /* Allow resizer to be visible/clickable */
  border-right: 1px solid #E2E8F0;
  position: relative; /* For resizer positioning */
}

.sidebar-resizer {
  position: absolute;
  top: 0;
  right: -4px;
  width: 8px;
  height: 100%;
  cursor: col-resize;
  z-index: 50;
  transition: all 0.2s;
}

.sidebar-resizer:hover {
  background-color: rgba(83, 70, 152, 0.2);
}

.sidebar-resizer:hover {
  background-color: rgba(83, 70, 152, 0.2);
}

.side-bar-main {
  background-color: #FFFFFF;
  border-bottom-left-radius: 16px;
  border-bottom-right-radius: 16px;
  padding-bottom: 24px;
  display: flex;
  flex-direction: column;
  flex: 1; /* Stretch to fill space until footer */
  transition: all 0.3s;
}

.side-bar.collapsed {
  width: 72px;
}

/* --- Collapsed State Overrides --- */
.side-bar.collapsed .org-name,
.side-bar.collapsed .org-subtext,
.side-bar.collapsed .chevron,
.side-bar.collapsed .section-label,
.side-bar.collapsed .nav-link span,
.side-bar.collapsed .org-info,
.side-bar.collapsed .logout-btn-full span {
  display: none;
}

.side-bar.collapsed .org-switcher {
  padding: 0;
  justify-content: center;
  height: 56px;
  width: 56px;
  margin: 8px auto 0 auto;
  position: relative;
}

/* Tooltips for Org Switcher in collapsed state */
.side-bar.collapsed .org-switcher::after {
  content: attr(data-tooltip);
  position: absolute;
  left: calc(100% + 12px);
  background: #1E293B;
  color: white;
  padding: 6px 10px;
  border-radius: 6px;
  font-size: 12px;
  white-space: nowrap;
  opacity: 0;
  visibility: hidden;
  transition: all 0.2s;
  pointer-events: none;
  z-index: 100;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.side-bar.collapsed .org-switcher:hover::after {
  opacity: 1;
  visibility: visible;
  transform: translateX(5px);
}

.side-bar.collapsed .nav-group {
  padding: 0 12px;
}

.side-bar.collapsed .nav-link {
  justify-content: center;
  padding: 0;
  height: 48px;
  width: 48px;
  margin: 0 auto 2px auto;
}

.side-bar.collapsed .nav-icon {
  margin: 0;
}

.org-switcher {
  margin: 8px 12px 0 12px;
  padding: 8px 12px;
  height: 56px; /* 8px margin-top + 56px height = 64px (matches top bar bottom) */
  background-color: #FAFAFA;
  border: 1px solid #E2E8F0;
  border-radius: 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  box-sizing: border-box;
  transition: all 0.3s;
}

.org-icon {
  width: 32px;
  height: 32px;
  background-color: rgba(83, 70, 152, 0.1);
  color: #534698;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  flex-shrink: 0;
}

.org-info {
  display: flex;
  flex-direction: column;
  gap: 2px; /* Increased gap as requested */
  line-height: 1.2;
  flex: 1;
  min-width: 0;
}

.org-name {
  font-size: 13px;
  font-weight: 600;
  color: #0F172A;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.org-subtext {
  font-size: 11px;
  color: #737373;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.chevron {
  color: #737373;
  margin-left: auto; /* Push to the right edge */
}

.menu-section {
  margin-top: 16px;
}

.section-label {
  padding: 0 24px;
  font-size: 10px; /* Smaller for better visual hierarchy */
  font-weight: 400; /* Regular */
  color: #94A3B8; /* Muted gray */
  letter-spacing: 0.08em;
  text-transform: uppercase;
  margin-bottom: 8px;
}

.nav-group {
  display: flex;
  flex-direction: column;
  padding: 0 12px;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0 14px;
  height: 40px; /* Reduced from 48px for a more compact look */
  color: #94A3B8; /* More grayish for inactive items */
  font-size: 14px;
  font-weight: 500; /* Medium */
  text-decoration: none;
  border-radius: 16px;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  margin-bottom: 2px;
  box-sizing: border-box;
  position: relative;
}

/* Tooltips for collapsed state */
.side-bar.collapsed .nav-link::after {
  content: attr(data-tooltip);
  position: absolute;
  left: calc(100% + 12px);
  background: #1E293B;
  color: white;
  padding: 6px 10px;
  border-radius: 6px;
  font-size: 12px;
  white-space: nowrap;
  opacity: 0;
  visibility: hidden;
  transition: all 0.2s;
  pointer-events: none;
  z-index: 100;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.side-bar.collapsed .nav-link:hover::after {
  opacity: 1;
  visibility: visible;
  transform: translateX(5px);
}

.nav-link:hover {
  background-color: #F8FAFC;
  color: #0F172A;
}

.nav-link.router-link-exact-active {
  background-color: rgba(83, 70, 152, 0.1);
  color: #534698;
  font-weight: 600;
  box-shadow: none;
}

.nav-icon {
  color: #94A3B8;
  transition: color 0.2s;
}

.nav-link:hover .nav-icon {
  color: #0F172A;
}

.nav-link.router-link-exact-active .nav-icon {
  color: #534698;
}

/* --- Main Container --- */
.main-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* --- Top Bar --- */
.top-bar {
  height: 64px;
  background-color: #FFFFFF;
  border-bottom: 1px solid #E2E8F0;
  display: flex;
  align-items: center;
  padding: 0 24px;
  gap: 16px; /* Equal gap between Toggle, Search, and Right Actions */
  flex-shrink: 0;
}

.top-bar-right {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}

.icon-btn {
  width: 36px;
  height: 36px;
  border: none;
  background: transparent;
  color: #64748B;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
  flex-shrink: 0;
}

.icon-btn:hover {
  background-color: #F1F5F9;
  color: #0F172A;
}

.search-box {
  display: flex;
  align-items: center;
  background-color: #FAFAFA;
  border: 1px solid #E2E8F0;
  border-radius: 16px;
  padding: 0 16px;
  flex: 1;
  max-width: 600px; /* Increased from 380px */
  margin: 0 auto; /* Keeps it centered in the available space */
  height: 38px;
  gap: 10px;
  transition: all 0.3s;
}

.search-icon {
  color: #94A3B8;
}

.search-box input {
  border: none;
  background: transparent;
  font-size: 13px;
  width: 100%;
  color: #0F172A;
}

.search-box input:focus {
  outline: none;
}

.search-hint {
  font-size: 12px;
  color: #94A3B8;
  border: 1px solid #E2E8F0;
  padding: 3px 7px;
  border-radius: 4px;
  background-color: #FFFFFF;
  line-height: 1;
  font-weight: 500;
  box-shadow: 0 1px 1px rgba(0,0,0,0.02);
}

.action-icons {
  display: flex;
  align-items: center;
  gap: 4px;
}

.notification-btn {
  position: relative;
}

.notif-badge {
  position: absolute;
  top: 2px;
  right: 2px;
  background-color: #EF4444;
  color: white;
  font-size: 11px;
  font-weight: 700;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid #FFFFFF;
}

.divider-v {
  width: 1.5px;
  height: 24px;
  background-color: #64748B; /* Exact icon color */
  margin: 0 4px;
  border-radius: 1px;
}

/* --- User Menu --- */
.user-menu-wrapper {
  position: relative;
  margin-left: 8px;
}

.user-trigger {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 6px 10px 6px 14px; /* Balanced L > R to offset chevron */
  border: none;
  background: transparent;
  cursor: pointer;
  border-radius: 10px;
  transition: all 0.2s ease;
  color: #64748B;
}

.user-trigger:hover {
  background-color: #F8FAFC;
}

.user-avatar-container {
  position: relative;
  display: block;
}

.user-avatar-sm {
  width: 32px;
  height: 32px;
  background-color: #534698;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
  border: 2px solid #FFFFFF; /* Matches top bar background */
  box-shadow: 0 0 0 1px #E2E8F0;
}

.status-indicator {
  position: absolute;
  bottom: 2px;
  right: 2px;
  width: 10px;
  height: 10px;
  background-color: #10B981;
  border: 2px solid #FFFFFF; /* Matches top bar background */
  border-radius: 50%;
  box-shadow: 0 1px 2px rgba(0,0,0,0.1);
}

.user-name-sm {
  font-size: 14px;
  font-weight: 400; /* Regular text */
  color: #0F172A;
  white-space: nowrap;
}

.user-dropdown {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  width: 220px;
  background-color: #FFFFFF;
  border: 1px solid #E2E8F0;
  border-radius: 12px;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  padding: 8px;
  z-index: 1000;
}

.menu-overlay {
  position: fixed;
  inset: 0;
  background: transparent;
  z-index: 100;
  cursor: default;
}

.dropdown-header {
  padding: 12px 12px 8px 12px;
}

.dropdown-user-name {
  font-size: 13px;
  font-weight: 500; /* Medium weight as requested */
  color: #0F172A;
  margin-bottom: 2px;
}

.dropdown-user-email {
  font-size: 11px;
  color: #64748B;
}

.dropdown-divider {
  height: 1px;
  background-color: #F1F5F9;
  margin: 8px 0;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  font-size: 13px;
  color: #475569;
  text-decoration: none;
  border-radius: 6px;
  transition: all 0.2s;
  border: none;
  background: none;
  width: 100%;
  cursor: pointer;
  text-align: left;
}

.dropdown-item:hover {
  background-color: #F8FAFC;
  color: #0F172A;
}

.dropdown-item svg {
  color: #94A3B8;
}

.dropdown-item.logout {
  color: #E11D48;
}

.dropdown-item.logout svg {
  color: #FB7185;
}

.dropdown-item.logout:hover {
  background-color: #FFF1F2;
}

/* Transitions */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.2s, transform 0.2s;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.status-dot {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 10px;
  height: 10px;
  background-color: #10B981;
  border: 2px solid #FFFFFF;
  border-radius: 50%;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 6px;
}

.user-name {
  font-size: 13px;
  font-weight: 600;
  color: #0F172A;
}

/* --- Page Content --- */
.page-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.breadcrumbs {
  display: flex;
  align-items: center;
  padding: 12px 24px;
  gap: 4px;
}

.crumb-item {
  display: flex;
  align-items: center;
  gap: 4px;
}

.crumb-link {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #737373;
  text-decoration: none;
  font-size: 13px;
  transition: color 0.2s;
}

.crumb-link:hover {
  color: #0F172A;
}

.crumb-separator {
  color: #CBD5E1;
  margin: 0 4px;
}

.current-crumb {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #0F172A;
  font-weight: 500;
  font-size: 13px;
}

.router-view-container {
  flex: 1;
  overflow-y: auto;
  padding: 0 24px 12px 24px;
}
</style>
