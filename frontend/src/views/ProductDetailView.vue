<template>
  <div class="product-detail-view">
    <!-- Loading -->
    <div v-if="loading" class="detail-loading">
      <div class="container">
        <div class="detail-skeleton">
          <div class="skeleton-img aspect-product" style="background: var(--color-ivory-dark); animation: shimmer 1.5s ease-in-out infinite;"></div>
          <div class="detail-skeleton__info">
            <div style="height: 12px; background: var(--color-ivory-dark); width: 40%; border-radius: 2px; margin-bottom: 16px; animation: shimmer 1.5s ease-in-out infinite;"></div>
            <div style="height: 36px; background: var(--color-ivory-dark); width: 70%; border-radius: 2px; margin-bottom: 24px; animation: shimmer 1.5s ease-in-out infinite;"></div>
            <div style="height: 16px; background: var(--color-ivory-dark); width: 100%; border-radius: 2px; margin-bottom: 8px; animation: shimmer 1.5s ease-in-out infinite;"></div>
            <div style="height: 16px; background: var(--color-ivory-dark); width: 80%; border-radius: 2px; animation: shimmer 1.5s ease-in-out infinite;"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Not Found -->
    <div v-else-if="notFound" class="detail-not-found">
      <div class="container text-center" style="padding-top: 120px; padding-bottom: 60px;">
        <h1 class="heading-sm" style="margin-bottom: var(--space-5);">Product Not Found</h1>
        <p style="color: var(--text-muted); margin-bottom: var(--space-8);">This product may have been removed or is temporarily unavailable.</p>
        <RouterLink to="/products" class="btn btn-primary">Browse All Products</RouterLink>
      </div>
    </div>

    <!-- Product Content -->
    <div v-else-if="product" class="detail-content">

      <!-- Breadcrumb -->
      <nav class="breadcrumb" aria-label="Breadcrumb">
        <div class="container">
          <ol class="breadcrumb__list">
            <li><RouterLink to="/" class="breadcrumb__link">Home</RouterLink></li>
            <li><span aria-hidden="true">›</span></li>
            <li><RouterLink to="/products" class="breadcrumb__link">Products</RouterLink></li>
            <li v-if="product.collection"><span aria-hidden="true">›</span></li>
            <li v-if="product.collection">
              <RouterLink :to="`/products?collection=${product.collection.slug}`" class="breadcrumb__link">{{ product.collection.name }}</RouterLink>
            </li>
            <li><span aria-hidden="true">›</span></li>
            <li><span class="breadcrumb__current" aria-current="page">{{ product.name }}</span></li>
          </ol>
        </div>
      </nav>

      <!-- Main Product Section -->
      <section class="product-main section">
        <div class="container">
          <div class="product-main__grid">

            <!-- Gallery Column -->
            <div class="product-main__gallery">
              <ProductGallery
                :images="product.images || []"
                :product-name="product.name"
              />
            </div>

            <!-- Info Column -->
            <div class="product-main__info">
              <!-- Category & Type -->
              <div class="product-meta">
                <RouterLink
                  v-if="product.collection"
                  :to="`/products?collection=${product.collection.slug}`"
                  class="product-meta__tag"
                >{{ product.collection.name }}</RouterLink>
                <span v-if="product.collection && product.product_type" class="product-meta__sep">·</span>
                <span v-if="product.product_type" class="product-meta__tag product-meta__tag--plain">{{ product.product_type }}</span>
              </div>

              <!-- Name -->
              <h1 class="product-name">{{ product.name }}</h1>

              <!-- Price -->
              <div class="product-price">
                <span v-if="product.price_visibility === 'visible' && product.price" class="product-price__value">
                  ₹{{ formatPrice(product.price) }}
                </span>
                <span v-else-if="product.price_visibility === 'contact_for_price'" class="product-price__contact">
                  Contact for Price
                </span>
              </div>

              <hr class="divider" style="margin-block: var(--space-6);" />

              <!-- Short Description -->
              <p v-if="product.short_description" class="product-short-desc">
                {{ product.short_description }}
              </p>

              <!-- Enquiry CTAs -->
              <div class="product-ctas">
                <a
                  :href="whatsappLink"
                  target="_blank"
                  rel="noopener"
                  class="btn btn-primary btn-lg product-cta--primary"
                >
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                    <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/>
                  </svg>
                  Enquire on WhatsApp
                </a>
                <a href="tel:+919415612726" class="btn btn-outline btn-lg">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">
                    <path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07A19.5 19.5 0 013.07 9.81a19.79 19.79 0 01-3.07-8.66A2 2 0 012 .18h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L6.09 7.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7a2 2 0 011.72 2.03z"/>
                  </svg>
                  Call Us
                </a>
              </div>

              <!-- Specifications -->
              <div class="product-specs" v-if="hasSpecs">
                <h2 class="product-specs__title">Specifications</h2>
                <dl class="product-specs__list">
                  <div v-if="product.material" class="product-specs__row">
                    <dt>Material</dt>
                    <dd>{{ product.material }}</dd>
                  </div>
                  <div v-if="product.finish" class="product-specs__row">
                    <dt>Finish</dt>
                    <dd>{{ product.finish }}</dd>
                  </div>
                  <div v-if="product.color" class="product-specs__row">
                    <dt>Color</dt>
                    <dd>{{ product.color }}</dd>
                  </div>
                  <div v-if="product.dimensions" class="product-specs__row">
                    <dt>Dimensions</dt>
                    <dd>{{ product.dimensions }}</dd>
                  </div>
                  <div v-if="product.product_type" class="product-specs__row">
                    <dt>Type</dt>
                    <dd>{{ product.product_type }}</dd>
                  </div>
                </dl>
              </div>

              <!-- Visit showroom note -->
              <div class="product-showroom-note">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">
                  <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/>
                </svg>
                <span>See this piece in person at our Rajrooppur showroom — open daily 11 AM to 9 PM.</span>
              </div>
            </div>
          </div>

          <!-- Full Description -->
          <div class="product-description" v-if="product.description">
            <h2 class="product-description__title">About This Piece</h2>
            <div class="product-description__body" v-html="formattedDescription"></div>
          </div>
        </div>
      </section>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { productsApi } from '@/services/products'
import ProductGallery from '@/components/product/ProductGallery.vue'

const route = useRoute()

const product = ref(null)
const loading = ref(true)
const notFound = ref(false)

const hasSpecs = computed(() =>
  product.value &&
  (product.value.material || product.value.finish || product.value.color ||
   product.value.dimensions || product.value.product_type)
)

const whatsappLink = computed(() => {
  if (!product.value) return 'https://wa.me/919415612726'
  const msg = encodeURIComponent(
    `Hi, I'm interested in the "${product.value.name}" — could you share more details?`
  )
  return `https://wa.me/919415612726?text=${msg}`
})

const formattedDescription = computed(() => {
  if (!product.value?.description) return ''
  return product.value.description.replace(/\n/g, '<br>')
})

function formatPrice(price) {
  return Number(price).toLocaleString('en-IN')
}

async function loadProduct() {
  loading.value = true
  notFound.value = false
  try {
    const res = await productsApi.getBySlug(route.params.slug)
    product.value = res.data
    // Update page title with product name
    if (product.value) {
      document.title = `${product.value.name} — Good Luck Furniture`
    }
  } catch (err) {
    if (err.response?.status === 404) {
      notFound.value = true
    }
  } finally {
    loading.value = false
  }
}

onMounted(loadProduct)
watch(() => route.params.slug, loadProduct)
</script>

<style scoped>
.detail-loading {
  padding-top: calc(72px + var(--space-12));
}

.detail-skeleton {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-12);
  padding-block: var(--space-12);
}

.detail-skeleton__info {
  padding-top: var(--space-8);
}

/* ─── Breadcrumb ──────────────────── */
.breadcrumb {
  padding-top: calc(72px + var(--space-6));
  padding-bottom: var(--space-4);
  border-bottom: 1px solid var(--border-light);
  background: var(--color-ivory-mid);
}

.breadcrumb__list {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--text-xs);
  letter-spacing: var(--tracking-wide);
  text-transform: uppercase;
}

.breadcrumb__link {
  color: var(--text-muted);
  transition: color var(--transition-fast);
}

.breadcrumb__link:hover {
  color: var(--text-primary);
}

.breadcrumb__current {
  color: var(--text-secondary);
}

/* ─── Product Grid ────────────────── */
.product-main__grid {
  display: grid;
  grid-template-columns: 1.1fr 1fr;
  gap: var(--space-16);
  align-items: start;
}

/* ─── Info ────────────────────────── */
.product-meta {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  margin-bottom: var(--space-4);
}

.product-meta__tag {
  font-size: var(--text-xs);
  letter-spacing: var(--tracking-wider);
  text-transform: uppercase;
  color: var(--color-brass);
  transition: color var(--transition-fast);
}

.product-meta__tag:hover {
  color: var(--color-espresso);
}

.product-meta__tag--plain {
  color: var(--text-muted);
}

.product-meta__sep {
  color: var(--text-muted);
  font-size: var(--text-xs);
}

.product-name {
  font-family: var(--font-display);
  font-size: clamp(var(--text-2xl), 3vw, var(--text-4xl));
  font-weight: 400;
  line-height: var(--leading-snug);
  color: var(--text-primary);
  margin-bottom: var(--space-5);
}

.product-price__value {
  font-size: var(--text-2xl);
  font-weight: 500;
  color: var(--text-primary);
}

.product-price__contact {
  font-size: var(--text-sm);
  font-weight: 500;
  letter-spacing: var(--tracking-wide);
  text-transform: uppercase;
  color: var(--color-brass);
}

.product-short-desc {
  color: var(--text-secondary);
  line-height: var(--leading-relaxed);
  margin-bottom: var(--space-6);
  font-size: var(--text-md);
}

.product-ctas {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-3);
  margin-bottom: var(--space-8);
}

.product-cta--primary {
  flex: 1;
  justify-content: center;
  min-width: 200px;
}

/* Specs */
.product-specs {
  border-top: 1px solid var(--border-light);
  padding-top: var(--space-6);
  margin-bottom: var(--space-6);
}

.product-specs__title {
  font-family: var(--font-sans);
  font-size: var(--text-xs);
  font-weight: 500;
  letter-spacing: var(--tracking-widest);
  text-transform: uppercase;
  color: var(--text-muted);
  margin-bottom: var(--space-4);
}

.product-specs__list {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.product-specs__row {
  display: flex;
  gap: var(--space-4);
  font-size: var(--text-sm);
  border-bottom: 1px solid var(--border-light);
  padding-bottom: var(--space-3);
}

.product-specs__row dt {
  min-width: 100px;
  color: var(--text-muted);
  flex-shrink: 0;
}

.product-specs__row dd {
  color: var(--text-primary);
}

/* Showroom note */
.product-showroom-note {
  display: flex;
  align-items: flex-start;
  gap: var(--space-2);
  font-size: var(--text-xs);
  color: var(--text-muted);
  line-height: var(--leading-relaxed);
  padding: var(--space-4);
  background: var(--color-ivory-mid);
  border-radius: var(--radius-md);
}

.product-showroom-note svg {
  flex-shrink: 0;
  margin-top: 1px;
  color: var(--color-brass);
}

/* Full Description */
.product-description {
  margin-top: var(--space-16);
  padding-top: var(--space-16);
  border-top: 1px solid var(--border-light);
  max-width: 720px;
}

.product-description__title {
  font-family: var(--font-display);
  font-size: var(--text-2xl);
  font-weight: 400;
  margin-bottom: var(--space-6);
}

.product-description__body {
  color: var(--text-secondary);
  line-height: var(--leading-relaxed);
  font-size: var(--text-md);
}

/* Not found */
.detail-not-found {
  min-height: 80vh;
  display: flex;
  align-items: center;
}

@keyframes shimmer {
  0%, 100% { opacity: 0.5; }
  50% { opacity: 1; }
}

@media (max-width: 900px) {
  .product-main__grid {
    grid-template-columns: 1fr;
    gap: var(--space-8);
  }
  .detail-skeleton {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 600px) {
  .product-ctas {
    flex-direction: column;
  }
  .product-cta--primary {
    flex: none;
    width: 100%;
  }
}
</style>
