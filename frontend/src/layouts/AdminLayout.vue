<template>
  <div class="admin-shell">
    <!-- Sidebar -->
    <aside class="admin-sidebar" :class="{ 'admin-sidebar--collapsed': sidebarCollapsed }">
      <div class="admin-sidebar__header">
        <RouterLink to="/admin" class="admin-logo">
          <span class="admin-logo__text">GLF Admin</span>
        </RouterLink>
        <button class="admin-sidebar__toggle" @click="sidebarCollapsed = !sidebarCollapsed" :aria-label="sidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">
            <line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/>
          </svg>
        </button>
      </div>

      <nav class="admin-nav" aria-label="Admin navigation">
        <RouterLink to="/admin" exact-active-class="admin-nav__link--active" class="admin-nav__link">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>
          <span>Dashboard</span>
        </RouterLink>
        <RouterLink to="/admin/products" active-class="admin-nav__link--active" class="admin-nav__link">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M21 16V8a2 2 0 00-1-1.73l-7-4a2 2 0 00-2 0l-7 4A2 2 0 003 8v8a2 2 0 001 1.73l7 4a2 2 0 002 0l7-4A2 2 0 0021 16z"/></svg>
          <span>Products</span>
        </RouterLink>
        <RouterLink to="/admin/categories" active-class="admin-nav__link--active" class="admin-nav__link">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M22 19a2 2 0 01-2 2H4a2 2 0 01-2-2V5a2 2 0 012-2h5l2 3h9a2 2 0 012 2z"/></svg>
          <span>Categories</span>
        </RouterLink>
        <RouterLink to="/admin/settings" active-class="admin-nav__link--active" class="admin-nav__link">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 010 2.83 2 2 0 01-2.83 0l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-4 0v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83-2.83l.06-.06A1.65 1.65 0 004.68 15a1.65 1.65 0 00-1.51-1H3a2 2 0 010-4h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 012.83-2.83l.06.06A1.65 1.65 0 009 4.68a1.65 1.65 0 001-1.51V3a2 2 0 014 0v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 2.83l-.06.06A1.65 1.65 0 0019.4 9a1.65 1.65 0 001.51 1H21a2 2 0 010 4h-.09a1.65 1.65 0 00-1.51 1z"/></svg>
          <span>Settings</span>
        </RouterLink>
        <hr class="admin-nav__divider" />
        <a href="/" target="_blank" class="admin-nav__link admin-nav__link--external">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
          <span>View Site</span>
        </a>
      </nav>

      <div class="admin-sidebar__footer">
        <div class="admin-user">
          <div class="admin-user__avatar" aria-hidden="true">{{ userInitial }}</div>
          <div class="admin-user__info">
            <p class="admin-user__name">{{ authStore.user?.name || 'Admin' }}</p>
            <p class="admin-user__email">{{ authStore.user?.email }}</p>
          </div>
        </div>
        <button class="admin-logout" @click="handleLogout" aria-label="Log out">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">
            <path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/>
          </svg>
        </button>
      </div>
    </aside>

    <!-- Main Content -->
    <div class="admin-main">
      <header class="admin-topbar">
        <button class="admin-topbar__menu" @click="sidebarCollapsed = !sidebarCollapsed" aria-label="Toggle sidebar">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">
            <line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/>
          </svg>
        </button>
        <h1 class="admin-topbar__title">{{ pageTitle }}</h1>
        <div class="admin-topbar__actions">
          <RouterLink v-if="route.name === 'admin-products'" to="/admin/products/new" class="btn btn-primary btn-sm" id="add-product-btn">
            + New Product
          </RouterLink>
        </div>
      </header>

      <main class="admin-content">
        <RouterView />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const sidebarCollapsed = ref(false)

const userInitial = computed(() =>
  (authStore.user?.name || 'A').charAt(0).toUpperCase()
)

const pageTitle = computed(() => {
  const titles = {
    'admin-dashboard': 'Dashboard',
    'admin-products': 'Products',
    'admin-product-new': 'New Product',
    'admin-product-edit': 'Edit Product',
    'admin-categories': 'Categories',
    'admin-settings': 'Settings',
  }
  return titles[route.name] || 'Admin'
})

async function handleLogout() {
  await authStore.logout()
  router.push({ name: 'admin-login' })
}
</script>

<style scoped>
.admin-shell {
  display: flex;
  min-height: 100vh;
  background: #F2F0ED;
}

/* ─── Sidebar ─────────────────────── */
.admin-sidebar {
  width: 240px;
  flex-shrink: 0;
  background: var(--color-charcoal);
  display: flex;
  flex-direction: column;
  position: sticky;
  top: 0;
  height: 100vh;
  overflow-y: auto;
  transition: width var(--transition-base);
}

.admin-sidebar--collapsed {
  width: 60px;
}

.admin-sidebar__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-5) var(--space-4);
  border-bottom: 1px solid rgba(255,255,255,0.08);
}

.admin-logo {
  display: block;
  overflow: hidden;
  white-space: nowrap;
}

.admin-logo__text {
  font-family: var(--font-display);
  font-size: var(--text-md);
  font-weight: 500;
  color: var(--color-ivory);
}

.admin-sidebar__toggle {
  color: rgba(255,255,255,0.4);
  transition: color var(--transition-fast);
  flex-shrink: 0;
}

.admin-sidebar__toggle:hover {
  color: rgba(255,255,255,0.8);
}

.admin-nav {
  flex: 1;
  padding: var(--space-5) var(--space-3);
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.admin-nav__link {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-3);
  font-size: var(--text-sm);
  color: rgba(255,255,255,0.6);
  border-radius: var(--radius-md);
  transition: all var(--transition-fast);
  white-space: nowrap;
  overflow: hidden;
}

.admin-nav__link:hover {
  background: rgba(255,255,255,0.08);
  color: rgba(255,255,255,0.9);
}

.admin-nav__link--active {
  background: rgba(176, 141, 87, 0.2);
  color: var(--color-brass-light) !important;
}

.admin-nav__divider {
  border: none;
  border-top: 1px solid rgba(255,255,255,0.08);
  margin-block: var(--space-3);
}

.admin-nav__link--external {
  font-size: var(--text-xs);
  color: rgba(255,255,255,0.4);
}

/* Sidebar Footer */
.admin-sidebar__footer {
  padding: var(--space-4);
  border-top: 1px solid rgba(255,255,255,0.08);
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.admin-user {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  flex: 1;
  overflow: hidden;
  min-width: 0;
}

.admin-user__avatar {
  width: 32px;
  height: 32px;
  background: var(--color-brass);
  color: white;
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: var(--text-sm);
  font-weight: 600;
  flex-shrink: 0;
}

.admin-user__info {
  overflow: hidden;
  min-width: 0;
}

.admin-user__name {
  font-size: var(--text-sm);
  color: rgba(255,255,255,0.8);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.admin-user__email {
  font-size: var(--text-xs);
  color: rgba(255,255,255,0.4);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.admin-logout {
  color: rgba(255,255,255,0.4);
  transition: color var(--transition-fast);
  flex-shrink: 0;
}

.admin-logout:hover {
  color: rgba(255,255,255,0.8);
}

/* ─── Main ────────────────────────── */
.admin-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.admin-topbar {
  background: white;
  border-bottom: 1px solid var(--border-light);
  padding: var(--space-4) var(--space-6);
  display: flex;
  align-items: center;
  gap: var(--space-4);
  position: sticky;
  top: 0;
  z-index: 10;
}

.admin-topbar__menu {
  color: var(--text-muted);
  display: none;
}

.admin-topbar__title {
  font-family: var(--font-sans);
  font-size: var(--text-lg);
  font-weight: 600;
  color: var(--text-primary);
  flex: 1;
}

.admin-content {
  padding: var(--space-8);
  flex: 1;
}

/* Collapsed sidebar */
.admin-sidebar--collapsed .admin-logo__text,
.admin-sidebar--collapsed .admin-user__info,
.admin-sidebar--collapsed .admin-nav__link span {
  display: none;
}

@media (max-width: 768px) {
  .admin-sidebar {
    position: fixed;
    z-index: var(--z-nav);
    transform: translateX(-100%);
  }
  .admin-sidebar:not(.admin-sidebar--collapsed) {
    transform: translateX(0);
  }
  .admin-topbar__menu {
    display: block;
  }
}
</style>
