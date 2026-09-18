<template>
  <div class="dashboard">
    <!-- Stats Grid -->
    <div class="stats-grid">
      <div class="stat-card" v-for="stat in stats" :key="stat.label">
        <p class="stat-card__value">{{ stat.value }}</p>
        <p class="stat-card__label">{{ stat.label }}</p>
      </div>
    </div>

    <!-- Recent Products -->
    <div class="dashboard-section">
      <div class="dashboard-section__header">
        <h2 class="dashboard-section__title">Recent Products</h2>
        <RouterLink to="/admin/products" class="btn btn-outline btn-sm">View All</RouterLink>
      </div>

      <div v-if="loading" class="admin-loading">Loading…</div>

      <div v-else-if="recentProducts.length > 0" class="recent-products">
        <div v-for="product in recentProducts" :key="product.id" class="recent-product">
          <div class="recent-product__image">
            <img
              v-if="product.primary_image"
              :src="product.primary_image.image_url"
              :alt="product.name"
              class="img-cover"
              loading="lazy"
              width="60"
              height="60"
            />
            <div v-else class="recent-product__placeholder" aria-hidden="true">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" opacity="0.3" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
            </div>
          </div>
          <div class="recent-product__info">
            <p class="recent-product__name">{{ product.name }}</p>
            <p class="recent-product__meta">{{ product.collection?.name || '—' }} · {{ product.product_type || '—' }}</p>
          </div>
          <div class="recent-product__status">
            <span class="status-badge" :class="product.is_active ? 'status-badge--active' : 'status-badge--inactive'">
              {{ product.is_active ? 'Published' : 'Draft' }}
            </span>
          </div>
          <div class="recent-product__actions">
            <RouterLink :to="`/admin/products/${product.id}/edit`" class="btn btn-ghost btn-sm">Edit</RouterLink>
          </div>
        </div>
      </div>

      <div v-else class="admin-empty">
        <p>No products yet.</p>
        <RouterLink to="/admin/products/new" class="btn btn-primary btn-sm" style="margin-top: var(--space-4);">Add First Product</RouterLink>
      </div>
    </div>

    <!-- Quick actions -->
    <div class="dashboard-section">
      <h2 class="dashboard-section__title">Quick Actions</h2>
      <div class="quick-actions">
        <RouterLink to="/admin/products/new" class="quick-action" id="quick-add-product">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>
          <span>Add Product</span>
        </RouterLink>
        <RouterLink to="/admin/categories" class="quick-action">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M22 19a2 2 0 01-2 2H4a2 2 0 01-2-2V5a2 2 0 012-2h5l2 3h9a2 2 0 012 2z"/></svg>
          <span>Manage Categories</span>
        </RouterLink>
        <a href="/" target="_blank" class="quick-action">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
          <span>View Website</span>
        </a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '@/services/api'

const dashboardData = ref(null)
const loading = ref(true)

const stats = computed(() => {
  if (!dashboardData.value) return []
  const s = dashboardData.value.stats
  return [
    { label: 'Total Products', value: s.total_products },
    { label: 'Published', value: s.active_products },
    { label: 'Featured', value: s.featured_products },
    { label: 'Drafts', value: s.inactive_products },
    { label: 'Categories', value: s.total_categories },
  ]
})

const recentProducts = computed(() => dashboardData.value?.recent_products || [])

onMounted(async () => {
  try {
    const res = await api.get('/admin/dashboard')
    dashboardData.value = res.data
  } catch (err) {
    console.error('Failed to load dashboard:', err)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.stats-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: var(--space-4);
  margin-bottom: var(--space-8);
}

.stat-card {
  background: white;
  border-radius: var(--radius-lg);
  padding: var(--space-6);
  border: 1px solid var(--border-light);
}

.stat-card__value {
  font-size: var(--text-4xl);
  font-family: var(--font-display);
  font-weight: 400;
  color: var(--text-primary);
  line-height: 1;
  margin-bottom: var(--space-2);
}

.stat-card__label {
  font-size: var(--text-xs);
  font-weight: 500;
  letter-spacing: var(--tracking-wide);
  text-transform: uppercase;
  color: var(--text-muted);
}

.dashboard-section {
  background: white;
  border-radius: var(--radius-lg);
  padding: var(--space-6);
  margin-bottom: var(--space-6);
  border: 1px solid var(--border-light);
}

.dashboard-section__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-6);
}

.dashboard-section__title {
  font-family: var(--font-sans);
  font-size: var(--text-md);
  font-weight: 600;
}

/* Recent products */
.recent-products {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.recent-product {
  display: grid;
  grid-template-columns: 60px 1fr auto auto;
  gap: var(--space-4);
  align-items: center;
  padding: var(--space-4) 0;
  border-bottom: 1px solid var(--border-light);
}

.recent-product:last-child {
  border-bottom: none;
}

.recent-product__image {
  width: 60px;
  height: 60px;
  border-radius: var(--radius-md);
  overflow: hidden;
  background: var(--color-ivory-dark);
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.recent-product__name {
  font-size: var(--text-sm);
  font-weight: 500;
  color: var(--text-primary);
  margin-bottom: 2px;
}

.recent-product__meta {
  font-size: var(--text-xs);
  color: var(--text-muted);
}

.status-badge {
  font-size: var(--text-xs);
  font-weight: 500;
  letter-spacing: var(--tracking-wide);
  text-transform: uppercase;
  padding: 0.2em 0.7em;
  border-radius: var(--radius-full);
}

.status-badge--active {
  background: rgba(45, 106, 79, 0.1);
  color: var(--color-success);
}

.status-badge--inactive {
  background: rgba(120, 113, 108, 0.1);
  color: var(--color-stone);
}

/* Quick actions */
.quick-actions {
  display: flex;
  gap: var(--space-4);
  flex-wrap: wrap;
}

.quick-action {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-5) var(--space-6);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  color: var(--text-secondary);
  font-size: var(--text-sm);
  font-weight: 500;
  transition: all var(--transition-base);
  min-width: 120px;
}

.quick-action:hover {
  border-color: var(--color-brass);
  color: var(--color-brass);
  background: rgba(176, 141, 87, 0.05);
}

.admin-loading {
  color: var(--text-muted);
  font-size: var(--text-sm);
  padding: var(--space-6) 0;
}

.admin-empty {
  color: var(--text-muted);
  font-size: var(--text-sm);
  padding: var(--space-6) 0;
  text-align: center;
}

@media (max-width: 900px) {
  .stats-grid { grid-template-columns: repeat(3, 1fr); }
}
@media (max-width: 600px) {
  .stats-grid { grid-template-columns: 1fr 1fr; }
  .recent-product { grid-template-columns: 48px 1fr auto; }
  .recent-product__actions { display: none; }
}
</style>
