<template>
  <div class="collections-view">

    <!-- Page Header -->
    <div class="page-header">
      <div class="container">
        <p class="section-label">Browse by Room</p>
        <hr class="divider--brass" style="margin-block: 1.25rem;" />
        <h1 class="heading-md">Our Collections</h1>
        <p class="page-header__desc">
          Each collection represents a room — and the furniture that makes it complete.
          Browse by space to discover pieces that work together.
        </p>
      </div>
    </div>

    <!-- Collections Grid -->
    <section class="section" aria-label="Furniture collections">
      <div class="container">
        <div class="collections-grid" v-if="categories.length > 0">
          <RouterLink
            v-for="(cat, idx) in categories"
            :key="cat.id"
            :to="`/products?collection=${cat.slug}`"
            class="cat-card"
            :class="{ 'cat-card--wide': idx === 0 || idx === 3 }"
          >
            <div class="cat-card__image-wrap overflow-hidden">
              <img
                v-if="cat.image_url"
                :src="cat.image_url"
                :alt="cat.name"
                class="cat-card__image img-cover"
                loading="lazy"
                width="800"
                height="600"
              />
              <div v-else class="cat-card__placeholder" :style="{ background: fallbackColors[idx % fallbackColors.length] }"></div>
              <div class="cat-card__overlay" aria-hidden="true"></div>
            </div>
            <div class="cat-card__content">
              <div>
                <h2 class="cat-card__name">{{ cat.name }}</h2>
                <p v-if="cat.description" class="cat-card__desc">{{ cat.description }}</p>
                <p v-if="cat.product_count > 0" class="cat-card__count">{{ cat.product_count }} pieces</p>
              </div>
              <span class="cat-card__cta">Browse Collection →</span>
            </div>
          </RouterLink>
        </div>

        <!-- Loading skeletons -->
        <div v-else-if="loading" class="collections-grid">
          <div v-for="n in 6" :key="n" class="cat-card cat-card--skeleton" :class="{ 'cat-card--wide': n === 1 || n === 4 }">
            <div class="cat-card__image-wrap" style="background: var(--color-ivory-dark); animation: shimmer 1.5s ease-in-out infinite;"></div>
          </div>
        </div>

        <div v-else-if="error" class="empty-state">
          <p>Failed to load collections. <button @click="load" class="text-link">Try again</button></p>
        </div>
      </div>
    </section>

    <!-- CTA Banner -->
    <section class="section--sm cta-banner" style="background: var(--color-charcoal);">
      <div class="container text-center">
        <p class="section-label" style="color: var(--color-stone-light);">Can't find what you need?</p>
        <h2 class="heading-sm cta-banner__title" style="color: var(--color-ivory); margin-block: var(--space-5);">
          We also do custom furniture
        </h2>
        <p class="cta-banner__desc">
          Tell us what you have in mind — size, material, finish — and we'll make it happen.
        </p>
        <RouterLink to="/contact" class="btn btn-brass btn-lg" style="margin-top: var(--space-8);">
          Enquire About Custom
        </RouterLink>
      </div>
    </section>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { categoriesApi } from '@/services/categories'

const categories = ref([])
const loading = ref(true)
const error = ref(null)

const fallbackColors = ['#C8B89A', '#B8A896', '#A89880', '#98887A', '#B0A090', '#887870']

async function load() {
  loading.value = true
  error.value = null
  try {
    const res = await categoriesApi.getAll()
    categories.value = res.data || []
  } catch (err) {
    error.value = true
    console.error('Failed to load categories:', err)
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>

<style scoped>
.page-header {
  padding-top: calc(72px + var(--space-16));
  padding-bottom: var(--space-12);
  background: var(--color-ivory-mid);
  border-bottom: 1px solid var(--border-light);
}

.page-header__desc {
  max-width: 52ch;
  color: var(--text-secondary);
  line-height: var(--leading-relaxed);
  margin-top: var(--space-4);
}

.collections-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-auto-rows: 360px;
  gap: var(--space-5);
}

.cat-card {
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  cursor: pointer;
}

.cat-card--wide {
  grid-column: span 2;
}

.cat-card__image-wrap {
  position: absolute;
  inset: 0;
}

.cat-card__image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform var(--transition-image);
}

.cat-card:hover .cat-card__image {
  transform: scale(1.05);
}

.cat-card__placeholder {
  width: 100%;
  height: 100%;
}

.cat-card__overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(26,26,26,0.75) 0%, transparent 60%);
}

.cat-card__content {
  position: relative;
  z-index: 1;
  padding: var(--space-6);
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  gap: var(--space-4);
}

.cat-card__name {
  font-family: var(--font-display);
  font-size: var(--text-2xl);
  font-weight: 400;
  color: var(--color-ivory);
  line-height: var(--leading-tight);
}

.cat-card--wide .cat-card__name {
  font-size: var(--text-3xl);
}

.cat-card__desc {
  font-size: var(--text-sm);
  color: rgba(240, 235, 227, 0.75);
  line-height: var(--leading-relaxed);
  max-width: 45ch;
  margin-top: var(--space-2);
}

.cat-card__count {
  font-size: var(--text-xs);
  letter-spacing: var(--tracking-wide);
  text-transform: uppercase;
  color: rgba(240, 235, 227, 0.55);
  margin-top: var(--space-1);
}

.cat-card__cta {
  font-size: var(--text-xs);
  font-weight: 500;
  letter-spacing: var(--tracking-wider);
  text-transform: uppercase;
  color: var(--color-brass-light);
  opacity: 0;
  transform: translateY(8px);
  transition: all var(--transition-base);
}

.cat-card:hover .cat-card__cta {
  opacity: 1;
  transform: translateY(0);
}

.cat-card--skeleton {
  background: var(--color-ivory-dark);
}

.cta-banner__title { margin-block: var(--space-5); }
.cta-banner__desc {
  max-width: 44ch;
  margin-inline: auto;
  color: var(--color-stone-light);
  font-size: var(--text-md);
}

.text-link {
  color: var(--color-brass);
  text-decoration: underline;
}

@keyframes shimmer {
  0%, 100% { opacity: 0.5; }
  50% { opacity: 1; }
}

@media (max-width: 900px) {
  .collections-grid {
    grid-template-columns: 1fr 1fr;
    grid-auto-rows: 280px;
  }
  .cat-card--wide {
    grid-column: span 1;
  }
}

@media (max-width: 600px) {
  .collections-grid {
    grid-template-columns: 1fr;
    grid-auto-rows: 260px;
  }
}
</style>
