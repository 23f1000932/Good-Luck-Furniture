<template>
  <div class="products-list-view">
    <!-- Toolbar -->
    <div class="admin-toolbar">
      <div class="admin-toolbar__left">
        <input
          v-model="search"
          type="search"
          class="form-input admin-toolbar__search"
          placeholder="Search products…"
          @input="debouncedSearch"
          id="products-search"
        />
        <select v-model="statusFilter" @change="loadProducts" class="form-select admin-toolbar__filter">
          <option value="">All Status</option>
          <option value="active">Published</option>
          <option value="inactive">Drafts</option>
        </select>
      </div>
      <RouterLink to="/admin/products/new" class="btn btn-primary" id="new-product-link">
        + Add Product
      </RouterLink>
    </div>

    <!-- Table -->
    <div class="admin-table-wrap">
      <div v-if="loading" class="admin-loading-state">
        <div v-for="n in 5" :key="n" class="skeleton-row"></div>
      </div>

      <table v-else-if="products.length > 0" class="admin-table" aria-label="Products list">
        <thead>
          <tr>
            <th scope="col">Product</th>
            <th scope="col">Collection</th>
            <th scope="col">Type</th>
            <th scope="col">Status</th>
            <th scope="col">Featured</th>
            <th scope="col">Updated</th>
            <th scope="col">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="product in products" :key="product.id" class="admin-table__row">
            <td class="admin-table__product-cell">
              <div class="admin-table__thumb">
                <img
                  v-if="product.primary_image"
                  :src="product.primary_image.image_url"
                  :alt="product.name"
                  class="admin-table__thumb-img"
                  loading="lazy"
                  width="48"
                  height="48"
                />
                <div v-else class="admin-table__thumb-placeholder" aria-hidden="true"></div>
              </div>
              <span class="admin-table__name">{{ product.name }}</span>
            </td>
            <td class="admin-table__cell">{{ product.collection?.name || '—' }}</td>
            <td class="admin-table__cell">{{ product.product_type || '—' }}</td>
            <td class="admin-table__cell">
              <span class="status-badge" :class="product.is_active ? 'status-badge--active' : 'status-badge--inactive'">
                {{ product.is_active ? 'Published' : 'Draft' }}
              </span>
            </td>
            <td class="admin-table__cell">
              <span v-if="product.is_featured" class="featured-badge">★ Featured</span>
              <span v-else class="text-muted-sm">—</span>
            </td>
            <td class="admin-table__cell admin-table__date">{{ formatDate(product.updated_at) }}</td>
            <td class="admin-table__actions">
              <RouterLink :to="`/products/${product.slug}`" target="_blank" class="admin-action-btn" title="View on site" :aria-label="`View ${product.name} on site`">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
              </RouterLink>
              <RouterLink :to="`/admin/products/${product.id}/edit`" class="admin-action-btn" :aria-label="`Edit ${product.name}`">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
              </RouterLink>
              <button
                class="admin-action-btn admin-action-btn--danger"
                @click="confirmDelete(product)"
                :aria-label="`Delete ${product.name}`"
                :id="`delete-${product.id}`"
              >
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a1 1 0 011-1h4a1 1 0 011 1v2"/></svg>
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-else class="admin-empty-state">
        <p>No products found.</p>
        <RouterLink to="/admin/products/new" class="btn btn-primary btn-sm" style="margin-top: var(--space-4);">Add First Product</RouterLink>
      </div>
    </div>

    <!-- Pagination -->
    <div v-if="totalPages > 1" class="admin-pagination">
      <button :disabled="page === 1" @click="goPage(page - 1)" class="btn btn-outline btn-sm">← Prev</button>
      <span class="admin-pagination__info">{{ page }} / {{ totalPages }}</span>
      <button :disabled="page === totalPages" @click="goPage(page + 1)" class="btn btn-outline btn-sm">Next →</button>
    </div>

    <!-- Delete Confirm Modal -->
    <Teleport to="body">
      <div v-if="deleteTarget" class="modal-backdrop" @click.self="deleteTarget = null" role="dialog" aria-modal="true" :aria-label="`Delete ${deleteTarget?.name}`">
        <div class="modal">
          <h3 class="modal__title">Delete Product?</h3>
          <p class="modal__body">
            Are you sure you want to delete <strong>{{ deleteTarget?.name }}</strong>?
            This will permanently remove the product and all its images.
          </p>
          <div class="modal__actions">
            <button class="btn btn-outline" @click="deleteTarget = null">Cancel</button>
            <button class="btn btn-danger" @click="executeDelete" :disabled="deleting" id="confirm-delete-btn">
              {{ deleting ? 'Deleting…' : 'Delete' }}
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { productsApi } from '@/services/products'

const products = ref([])
const loading = ref(true)
const page = ref(1)
const total = ref(0)
const perPage = 20
const search = ref('')
const statusFilter = ref('')
const deleteTarget = ref(null)
const deleting = ref(false)

const totalPages = computed(() => Math.max(1, Math.ceil(total.value / perPage)))

let searchTimer = null
function debouncedSearch() {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(loadProducts, 350)
}

async function loadProducts() {
  loading.value = true
  try {
    const params = { page: page.value, per_page: perPage }
    if (search.value) params.search = search.value
    if (statusFilter.value) params.status = statusFilter.value
    const res = await productsApi.adminGetAll(params)
    products.value = res.data || []
    total.value = res.meta?.total || 0
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

function goPage(p) {
  page.value = p
  loadProducts()
}

function confirmDelete(product) {
  deleteTarget.value = product
}

async function executeDelete() {
  if (!deleteTarget.value) return
  deleting.value = true
  try {
    await productsApi.adminDelete(deleteTarget.value.id)
    deleteTarget.value = null
    await loadProducts()
  } catch (err) {
    console.error('Delete failed:', err)
    alert('Failed to delete product')
  } finally {
    deleting.value = false
  }
}

function formatDate(dateStr) {
  if (!dateStr) return '—'
  return new Date(dateStr).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })
}

onMounted(loadProducts)
</script>

<style scoped>
.admin-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-4);
  margin-bottom: var(--space-5);
}

.admin-toolbar__left {
  display: flex;
  gap: var(--space-3);
  flex: 1;
}

.admin-toolbar__search {
  max-width: 280px;
}

.admin-toolbar__filter {
  max-width: 160px;
}

.admin-table-wrap {
  background: white;
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-light);
  overflow: hidden;
}

.admin-table {
  width: 100%;
  border-collapse: collapse;
  font-size: var(--text-sm);
}

.admin-table thead {
  background: var(--color-ivory-mid);
  border-bottom: 1px solid var(--border-light);
}

.admin-table th {
  padding: var(--space-3) var(--space-4);
  text-align: left;
  font-size: var(--text-xs);
  font-weight: 600;
  letter-spacing: var(--tracking-wide);
  text-transform: uppercase;
  color: var(--text-muted);
  white-space: nowrap;
}

.admin-table__row {
  border-bottom: 1px solid var(--border-light);
  transition: background var(--transition-fast);
}

.admin-table__row:last-child {
  border-bottom: none;
}

.admin-table__row:hover {
  background: var(--color-ivory-mid);
}

.admin-table__product-cell {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
}

.admin-table__cell {
  padding: var(--space-3) var(--space-4);
  color: var(--text-secondary);
}

.admin-table__thumb {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-md);
  overflow: hidden;
  background: var(--color-ivory-dark);
  flex-shrink: 0;
}

.admin-table__thumb-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.admin-table__thumb-placeholder {
  width: 100%;
  height: 100%;
  background: var(--color-ivory-dark);
}

.admin-table__name {
  font-weight: 500;
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 200px;
  display: block;
}

.admin-table__date {
  font-size: var(--text-xs);
  color: var(--text-muted);
}

.admin-table__actions {
  padding: var(--space-3) var(--space-4);
  display: flex;
  gap: var(--space-1);
}

.admin-action-btn {
  width: 30px;
  height: 30px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-md);
  color: var(--text-muted);
  transition: all var(--transition-fast);
}

.admin-action-btn:hover {
  background: var(--color-ivory-mid);
  color: var(--text-primary);
}

.admin-action-btn--danger:hover {
  background: rgba(155, 48, 48, 0.1);
  color: var(--color-error);
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

.featured-badge {
  font-size: var(--text-xs);
  color: var(--color-brass);
}

.text-muted-sm {
  font-size: var(--text-xs);
  color: var(--text-muted);
}

.admin-loading-state {
  padding: var(--space-4);
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.skeleton-row {
  height: 56px;
  background: var(--color-ivory-dark);
  border-radius: var(--radius-md);
  animation: shimmer 1.5s ease-in-out infinite;
}

.admin-empty-state {
  padding: var(--space-16);
  text-align: center;
  color: var(--text-muted);
}

.admin-pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-4);
  margin-top: var(--space-5);
}

.admin-pagination__info {
  font-size: var(--text-sm);
  color: var(--text-muted);
}

/* Modal */
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: var(--z-modal);
  padding: var(--space-6);
}

.modal {
  background: white;
  border-radius: var(--radius-lg);
  padding: var(--space-8);
  max-width: 420px;
  width: 100%;
  box-shadow: var(--shadow-lg);
}

.modal__title {
  font-family: var(--font-display);
  font-size: var(--text-xl);
  font-weight: 400;
  margin-bottom: var(--space-4);
}

.modal__body {
  color: var(--text-secondary);
  font-size: var(--text-sm);
  line-height: var(--leading-relaxed);
  margin-bottom: var(--space-6);
}

.modal__actions {
  display: flex;
  gap: var(--space-3);
  justify-content: flex-end;
}

.btn-danger {
  background: var(--color-error);
  color: white;
  border-color: var(--color-error);
  padding: 0.875rem 2rem;
  font-size: var(--text-sm);
  font-weight: 500;
  letter-spacing: var(--tracking-wide);
  text-transform: uppercase;
  border-radius: var(--radius-sm);
  transition: all var(--transition-base);
  border-style: solid;
  border-width: 1px;
}

.btn-danger:hover:not(:disabled) {
  opacity: 0.85;
}

@keyframes shimmer {
  0%, 100% { opacity: 0.5; }
  50% { opacity: 1; }
}

@media (max-width: 768px) {
  .admin-table th:nth-child(n+4):nth-child(-n+6),
  .admin-table td:nth-child(n+4):nth-child(-n+6) {
    display: none;
  }
}
</style>
