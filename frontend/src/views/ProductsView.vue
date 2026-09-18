<template>
  <div class="products-view">
    <!-- Page Header -->
    <div class="page-header">
      <div class="container">
        <p class="section-label">
          <span v-if="activeCollection">{{ activeCollection.name }}</span>
          <span v-else>All Products</span>
        </p>
        <hr class="divider--brass" style="margin-block: 1.25rem;" />
        <h1 class="heading-md">
          <span v-if="activeCollection">{{ activeCollection.name }} Furniture</span>
          <span v-else>Our Furniture</span>
        </h1>
      </div>
    </div>

    <div class="products-layout section">
      <div class="container">
        <div class="products-layout__inner">

          <!-- ─── Sidebar Filters ──────────────────── -->
          <aside class="filters" aria-label="Product filters">
            <div class="filters__inner">
              <!-- Search -->
              <div class="filters__group">
                <label for="search" class="form-label">Search</label>
                <div class="filters__search-wrap">
                  <input
                    id="search"
                    v-model="searchQuery"
                    type="search"
                    placeholder="Search products…"
                    class="form-input"
                    @input="debouncedSearch"
                  />
                </div>
              </div>

              <!-- Collection filter -->
              <div class="filters__group">
                <p class="form-label">Collection</p>
                <div class="filters__radio-list">
                  <label class="filters__radio">
                    <input type="radio" name="collection" :value="''" v-model="selectedCollection" @change="applyFilters" />
                    <span>All Collections</span>
                  </label>
                  <label v-for="cat in categories" :key="cat.id" class="filters__radio">
                    <input type="radio" name="collection" :value="cat.slug" v-model="selectedCollection" @change="applyFilters" />
                    <span>{{ cat.name }}</span>
                    <span v-if="cat.product_count" class="filters__count">{{ cat.product_count }}</span>
                  </label>
                </div>
              </div>

              <!-- Product type filter -->
              <div class="filters__group" v-if="productTypes.length > 0">
                <p class="form-label">Product Type</p>
                <div class="filters__radio-list">
                  <label class="filters__radio">
                    <input type="radio" name="type" :value="''" v-model="selectedType" @change="applyFilters" />
                    <span>All Types</span>
                  </label>
                  <label v-for="type in productTypes" :key="type" class="filters__radio">
                    <input type="radio" name="type" :value="type" v-model="selectedType" @change="applyFilters" />
                    <span>{{ type }}</span>
                  </label>
                </div>
              </div>

              <!-- Clear filters -->
              <button v-if="hasFilters" class="filters__clear" @click="clearFilters">
                Clear all filters
              </button>
            </div>
          </aside>

          <!-- ─── Products Area ────────────────────── -->
          <div class="products-area">
            <!-- Toolbar -->
            <div class="products-toolbar">
              <p class="products-toolbar__count">
                <span v-if="!loading">{{ total }} product{{ total !== 1 ? 's' : '' }}</span>
                <span v-else>Loading…</span>
              </p>
              <div class="products-toolbar__right">
                <label for="sort" class="form-label" style="white-space: nowrap;">Sort by</label>
                <select id="sort" v-model="sortBy" @change="applyFilters" class="form-select filters__sort">
                  <option value="newest">Newest</option>
                  <option value="oldest">Oldest</option>
                  <option value="name_asc">Name A–Z</option>
                  <option value="name_desc">Name Z–A</option>
                </select>

                <!-- Mobile filter toggle -->
                <button class="filters__mobile-toggle" @click="filtersOpen = !filtersOpen" aria-label="Toggle filters">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">
                    <line x1="4" y1="6" x2="20" y2="6"/><line x1="8" y1="12" x2="20" y2="12"/><line x1="12" y1="18" x2="20" y2="18"/>
                  </svg>
                  Filters
                </button>
              </div>
            </div>

            <!-- Loading -->
            <div v-if="loading" class="product-grid">
              <div v-for="n in 8" :key="n" class="skeleton-card aspect-product" style="background: var(--color-ivory-dark); animation: shimmer 1.5s ease-in-out infinite;"></div>
            </div>

            <!-- Products grid -->
            <div v-else-if="products.length > 0" class="product-grid">
              <ProductCard
                v-for="product in products"
                :key="product.id"
                :product="product"
              />
            </div>

            <!-- Empty state -->
            <div v-else class="products-empty">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" opacity="0.3" aria-hidden="true">
                <path d="M21 16V8a2 2 0 00-1-1.73l-7-4a2 2 0 00-2 0l-7 4A2 2 0 003 8v8a2 2 0 001 1.73l7 4a2 2 0 002 0l7-4A2 2 0 0021 16z"/>
              </svg>
              <p class="products-empty__title">No products found</p>
              <p class="products-empty__desc">
                <span v-if="hasFilters">Try adjusting your filters.</span>
                <span v-else>Our catalogue is being updated. Check back soon.</span>
              </p>
              <button v-if="hasFilters" @click="clearFilters" class="btn btn-outline btn-sm" style="margin-top: var(--space-5);">
                Clear filters
              </button>
            </div>

            <!-- Pagination -->
            <div v-if="totalPages > 1" class="pagination">
              <button
                class="pagination__btn"
                :disabled="currentPage === 1"
                @click="goToPage(currentPage - 1)"
                aria-label="Previous page"
              >
                ← Prev
              </button>
              <span class="pagination__info">{{ currentPage }} / {{ totalPages }}</span>
              <button
                class="pagination__btn"
                :disabled="currentPage === totalPages"
                @click="goToPage(currentPage + 1)"
                aria-label="Next page"
              >
                Next →
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Mobile Filters Drawer -->
    <Teleport to="body">
      <Transition name="mobile-nav">
        <div v-if="filtersOpen" class="mobile-filters" role="dialog" aria-modal="true" aria-label="Filters">
          <div class="mobile-nav__overlay" @click="filtersOpen = false"></div>
          <div class="mobile-nav__panel" style="overflow-y: auto;">
            <div class="mobile-nav__header">
              <span style="font-family: var(--font-display); font-size: var(--text-lg);">Filters</span>
              <button class="mobile-nav__close" @click="filtersOpen = false" aria-label="Close filters">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M18 6L6 18M6 6l12 12"/></svg>
              </button>
            </div>

            <div class="filters__group">
              <p class="form-label">Collection</p>
              <div class="filters__radio-list">
                <label class="filters__radio">
                  <input type="radio" name="m-collection" :value="''" v-model="selectedCollection" @change="applyFilters(); filtersOpen = false" />
                  <span>All Collections</span>
                </label>
                <label v-for="cat in categories" :key="cat.id" class="filters__radio">
                  <input type="radio" name="m-collection" :value="cat.slug" v-model="selectedCollection" @change="applyFilters(); filtersOpen = false" />
                  <span>{{ cat.name }}</span>
                </label>
              </div>
            </div>

            <div class="filters__group" v-if="productTypes.length > 0">
              <p class="form-label">Product Type</p>
              <div class="filters__radio-list">
                <label class="filters__radio">
                  <input type="radio" name="m-type" :value="''" v-model="selectedType" @change="applyFilters(); filtersOpen = false" />
                  <span>All Types</span>
                </label>
                <label v-for="type in productTypes" :key="type" class="filters__radio">
                  <input type="radio" name="m-type" :value="type" v-model="selectedType" @change="applyFilters(); filtersOpen = false" />
                  <span>{{ type }}</span>
                </label>
              </div>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { productsApi } from '@/services/products'
import { categoriesApi } from '@/services/categories'
import ProductCard from '@/components/product/ProductCard.vue'

const route = useRoute()
const router = useRouter()

const products = ref([])
const categories = ref([])
const productTypes = ref([])
const loading = ref(true)
const total = ref(0)
const currentPage = ref(1)
const perPage = 12
const filtersOpen = ref(false)

const searchQuery = ref(route.query.search || '')
const selectedCollection = ref(route.query.collection || '')
const selectedType = ref(route.query.product_type || '')
const sortBy = ref(route.query.sort || 'newest')

const totalPages = computed(() => Math.max(1, Math.ceil(total.value / perPage)))
const hasFilters = computed(() => searchQuery.value || selectedCollection.value || selectedType.value)
const activeCollection = computed(() =>
  selectedCollection.value
    ? categories.value.find(c => c.slug === selectedCollection.value)
    : null
)

let searchTimer = null
function debouncedSearch() {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(() => applyFilters(), 350)
}

async function loadProducts() {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      per_page: perPage,
      sort: sortBy.value,
    }
    if (searchQuery.value) params.search = searchQuery.value
    if (selectedCollection.value) params.collection = selectedCollection.value
    if (selectedType.value) params.product_type = selectedType.value

    const res = await productsApi.getAll(params)
    products.value = res.data || []
    total.value = res.meta?.total || 0
  } catch (error) {
    console.error('Failed to load products:', error)
    products.value = []
  } finally {
    loading.value = false
  }
}

function applyFilters() {
  currentPage.value = 1
  router.replace({
    query: {
      ...(searchQuery.value && { search: searchQuery.value }),
      ...(selectedCollection.value && { collection: selectedCollection.value }),
      ...(selectedType.value && { product_type: selectedType.value }),
      ...(sortBy.value !== 'newest' && { sort: sortBy.value }),
    }
  })
  loadProducts()
}

function clearFilters() {
  searchQuery.value = ''
  selectedCollection.value = ''
  selectedType.value = ''
  sortBy.value = 'newest'
  applyFilters()
}

function goToPage(page) {
  currentPage.value = page
  loadProducts()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

onMounted(async () => {
  const [, catsRes, typesRes] = await Promise.all([
    loadProducts(),
    categoriesApi.getAll(),
    productsApi.getTypes(),
  ])
  categories.value = catsRes?.data || []
  productTypes.value = typesRes?.data || []
})
</script>

<style scoped>
.page-header {
  padding-top: calc(72px + var(--space-12));
  padding-bottom: var(--space-10);
  background: var(--color-ivory-mid);
  border-bottom: 1px solid var(--border-light);
}

.products-layout__inner {
  display: grid;
  grid-template-columns: 240px 1fr;
  gap: var(--space-12);
  align-items: start;
}

/* ─── Filters ──────────────────────── */
.filters__inner {
  position: sticky;
  top: calc(72px + var(--space-6));
  display: flex;
  flex-direction: column;
  gap: var(--space-8);
}

.filters__group {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.filters__radio-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.filters__radio {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--text-sm);
  color: var(--text-secondary);
  cursor: pointer;
  transition: color var(--transition-fast);
}

.filters__radio:hover {
  color: var(--text-primary);
}

.filters__radio input[type="radio"] {
  accent-color: var(--color-charcoal);
  width: 14px;
  height: 14px;
  flex-shrink: 0;
}

.filters__count {
  margin-left: auto;
  font-size: var(--text-xs);
  color: var(--text-muted);
}

.filters__search-wrap {
  position: relative;
}

.filters__sort {
  width: auto;
  padding-inline: var(--space-3);
}

.filters__clear {
  font-size: var(--text-xs);
  letter-spacing: var(--tracking-wide);
  text-transform: uppercase;
  color: var(--color-brass);
  text-decoration: underline;
  text-align: left;
}

.filters__mobile-toggle {
  display: none;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--text-sm);
  color: var(--text-secondary);
  padding: 0.5rem 0.75rem;
  border: 1px solid var(--border-mid);
  border-radius: var(--radius-sm);
}

/* ─── Products Area ──────────────── */
.products-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-8);
  padding-bottom: var(--space-5);
  border-bottom: 1px solid var(--border-light);
}

.products-toolbar__count {
  font-size: var(--text-sm);
  color: var(--text-muted);
}

.products-toolbar__right {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

/* Empty State */
.products-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: var(--space-20) 0;
}

.products-empty__title {
  font-family: var(--font-display);
  font-size: var(--text-xl);
  color: var(--text-secondary);
  margin-top: var(--space-5);
}

.products-empty__desc {
  color: var(--text-muted);
  margin-top: var(--space-2);
}

/* Pagination */
.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-5);
  margin-top: var(--space-12);
}

.pagination__btn {
  font-size: var(--text-sm);
  font-weight: 500;
  letter-spacing: var(--tracking-wide);
  text-transform: uppercase;
  color: var(--text-primary);
  padding: 0.625rem 1.25rem;
  border: 1px solid var(--border-mid);
  border-radius: var(--radius-sm);
  transition: all var(--transition-base);
}

.pagination__btn:hover:not(:disabled) {
  background: var(--color-charcoal);
  color: var(--color-ivory);
  border-color: var(--color-charcoal);
}

.pagination__btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.pagination__info {
  font-size: var(--text-sm);
  color: var(--text-muted);
}

@keyframes shimmer {
  0%, 100% { opacity: 0.5; }
  50% { opacity: 1; }
}

/* Mobile */
.mobile-filters {
  position: fixed;
  inset: 0;
  z-index: var(--z-overlay);
}

@media (max-width: 900px) {
  .products-layout__inner {
    grid-template-columns: 1fr;
  }
  .filters {
    display: none;
  }
  .filters__mobile-toggle {
    display: flex;
  }
}
</style>
