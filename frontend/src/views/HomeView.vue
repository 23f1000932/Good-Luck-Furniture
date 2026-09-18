<template>
  <div class="home">

    <!-- ─── Hero ─────────────────────────────────────── -->
    <section class="hero" aria-label="Hero">
      <div class="hero__image-wrap">
        <img
          src="https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=1800&q=80"
          alt="Elegant living room furniture at Good Luck Furniture"
          class="hero__image"
          loading="eager"
          fetchpriority="high"
          width="1800"
          height="1200"
        />
        <div class="hero__tint" aria-hidden="true"></div>
      </div>

      <div class="hero__content">
        <p class="section-label hero__eyebrow">Prayagraj's Furniture Showroom</p>
        <h1 class="hero__title">Furniture for<br />the way you live</h1>
        <p class="hero__subtitle">
          Crafted for comfort. Chosen for longevity.<br />
          Visit our showroom at Rajrooppur.
        </p>
        <div class="hero__actions">
          <RouterLink to="/products" class="btn btn-primary btn-lg">Browse Collection</RouterLink>
          <RouterLink to="/contact" class="btn btn-outline hero__contact-btn btn-lg">Find Our Showroom</RouterLink>
        </div>
      </div>

      <!-- Scroll hint -->
      <div class="hero__scroll" aria-hidden="true">
        <span>Scroll</span>
        <div class="hero__scroll-line"></div>
      </div>
    </section>

    <!-- ─── Brand Introduction ────────────────────────── -->
    <section class="section brand-intro" aria-labelledby="brand-heading">
      <div class="container">
        <div class="brand-intro__layout">
          <div class="brand-intro__text">
            <p class="section-label">About Us</p>
            <hr class="divider--brass" style="margin-block: 1.25rem;" />
            <h2 id="brand-heading" class="heading-md">
              A showroom built on honest craftsmanship
            </h2>
            <p class="brand-intro__body">
              At Good Luck Furniture, we believe that well-made furniture isn't a luxury —
              it's a decision about how you want to live. Our showroom in Rajrooppur carries
              pieces that are built to last: beds that anchor a bedroom, sofas that hold a family
              together, dining tables that witness daily life.
            </p>
            <p class="brand-intro__body">
              Every piece is selected for its materials, its construction, and its character.
              We don't carry furniture that won't stand the test of time.
            </p>
            <RouterLink to="/about" class="brand-intro__link">
              Our story
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">
                <path d="M5 12h14M12 5l7 7-7 7"/>
              </svg>
            </RouterLink>
          </div>
          <div class="brand-intro__image-wrap">
            <div class="aspect-portrait overflow-hidden">
              <img
                src="https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=800&q=80"
                alt="Interior of Good Luck Furniture showroom"
                class="img-cover"
                loading="lazy"
                width="800"
                height="1066"
              />
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ─── Collections ───────────────────────────────── -->
    <section class="section--sm collections-section" style="background: var(--color-ivory-mid);" aria-labelledby="collections-heading">
      <div class="container">
        <div class="collections-section__header">
          <div>
            <p class="section-label">Browse by Room</p>
            <hr class="divider--brass" style="margin-block: 1.25rem;" />
            <h2 id="collections-heading" class="heading-sm">Our Collections</h2>
          </div>
          <RouterLink to="/collections" class="btn btn-outline btn-sm">View All</RouterLink>
        </div>
      </div>

      <!-- Horizontal scroll collection cards -->
      <div class="collections-strip" v-if="categories.length > 0">
        <div class="collections-strip__inner">
          <RouterLink
            v-for="cat in categories"
            :key="cat.id"
            :to="`/products?collection=${cat.slug}`"
            class="collection-card"
          >
            <div class="collection-card__image-wrap aspect-portrait overflow-hidden">
              <img
                v-if="cat.image_url"
                :src="cat.image_url"
                :alt="cat.name"
                class="collection-card__image img-cover"
                loading="lazy"
                width="400"
                height="533"
              />
              <div v-else class="collection-card__placeholder" :style="{ background: categoryColors[cat.slug] || '#DDD8D0' }"></div>
              <div class="collection-card__overlay" aria-hidden="true"></div>
            </div>
            <div class="collection-card__label">
              <span class="collection-card__name">{{ cat.name }}</span>
              <span v-if="cat.product_count > 0" class="collection-card__count">{{ cat.product_count }} pieces</span>
            </div>
          </RouterLink>
        </div>
      </div>

      <!-- Loading skeleton -->
      <div v-else-if="categoriesLoading" class="collections-strip">
        <div class="collections-strip__inner">
          <div v-for="n in 5" :key="n" class="collection-card collection-card--skeleton">
            <div class="aspect-portrait" style="background: var(--color-ivory-dark);"></div>
          </div>
        </div>
      </div>
    </section>

    <!-- ─── Featured Products ─────────────────────────── -->
    <section class="section featured-section" aria-labelledby="featured-heading" v-if="featuredProducts.length > 0 || featuredLoading">
      <div class="container">
        <div class="featured-section__header">
          <div>
            <p class="section-label">Curated Selection</p>
            <hr class="divider--brass" style="margin-block: 1.25rem;" />
            <h2 id="featured-heading" class="heading-sm">Featured Pieces</h2>
          </div>
          <RouterLink to="/products" class="btn btn-outline btn-sm">Browse All Products</RouterLink>
        </div>

        <!-- Editorial asymmetric grid -->
        <div class="featured-grid" v-if="featuredProducts.length > 0">
          <!-- Large featured card -->
          <div class="featured-grid__main" v-if="featuredProducts[0]">
            <ProductCard :product="featuredProducts[0]" variant="large" />
          </div>
          <!-- Side cards -->
          <div class="featured-grid__side">
            <ProductCard
              v-for="product in featuredProducts.slice(1, 3)"
              :key="product.id"
              :product="product"
            />
          </div>
        </div>

        <!-- More products if available -->
        <div class="product-grid" style="margin-top: var(--space-8);" v-if="featuredProducts.length > 3">
          <ProductCard
            v-for="product in featuredProducts.slice(3)"
            :key="product.id"
            :product="product"
          />
        </div>

        <!-- Loading -->
        <div v-if="featuredLoading" class="featured-grid">
          <div class="featured-grid__main">
            <div class="skeleton-card aspect-portrait"></div>
          </div>
          <div class="featured-grid__side">
            <div v-for="n in 2" :key="n" class="skeleton-card aspect-product"></div>
          </div>
        </div>
      </div>
    </section>

    <!-- ─── Craftsmanship Banner ──────────────────────── -->
    <section class="craft-banner" aria-labelledby="craft-heading">
      <div class="craft-banner__image-wrap">
        <img
          src="https://images.unsplash.com/photo-1581539250439-c96689b516dd?w=1600&q=80"
          alt="Furniture craftsmanship and quality materials"
          class="craft-banner__image img-cover"
          loading="lazy"
          width="1600"
          height="900"
        />
        <div class="craft-banner__tint" aria-hidden="true"></div>
      </div>
      <div class="craft-banner__content container">
        <p class="section-label" style="color: rgba(240,235,227,0.6);">Our Promise</p>
        <hr class="divider--brass" style="margin-block: 1.25rem;" />
        <h2 id="craft-heading" class="heading-md craft-banner__title">
          Made to last.<br />Designed to belong.
        </h2>
        <div class="craft-banner__points">
          <div class="craft-point">
            <h3 class="craft-point__title">Materials</h3>
            <p class="craft-point__desc">Solid wood, quality engineered wood and durable fabrics — selected for longevity, not just appearance.</p>
          </div>
          <div class="craft-point">
            <h3 class="craft-point__title">Construction</h3>
            <p class="craft-point__desc">Every joint, every finish, every detail is considered. Furniture that won't disappoint you in five years.</p>
          </div>
          <div class="craft-point">
            <h3 class="craft-point__title">Service</h3>
            <p class="craft-point__desc">Visit our showroom, see pieces in person, and get honest advice on what suits your space.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- ─── Showroom / Contact CTA ────────────────────── -->
    <section class="section showroom-section" aria-labelledby="showroom-heading">
      <div class="container">
        <div class="showroom-section__layout">
          <div class="showroom-section__image-wrap">
            <div class="aspect-landscape overflow-hidden">
              <img
                src="https://images.unsplash.com/photo-1556228453-efd6c1ff04f6?w=800&q=80"
                alt="Good Luck Furniture showroom exterior"
                class="img-cover"
                loading="lazy"
                width="800"
                height="600"
              />
            </div>
          </div>

          <div class="showroom-section__info">
            <p class="section-label">Visit Us</p>
            <hr class="divider--brass" style="margin-block: 1.25rem;" />
            <h2 id="showroom-heading" class="heading-sm">Come see it in person</h2>
            <p class="showroom-section__desc">
              Furniture looks different on a screen than it does in a room.
              Visit our showroom to sit, touch, and decide what's right for your home.
            </p>

            <address class="showroom-address">
              <div class="showroom-info-item">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg>
                <div>
                  <strong>Good Luck Furniture</strong><br>
                  Opposite Sai Dham Apartments,<br>
                  Rehmat Complex, Rajrooppur,<br>
                  Prayagraj, UP 211015
                </div>
              </div>
              <div class="showroom-info-item">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                <span>Monday – Sunday &nbsp;|&nbsp; 11 AM – 9 PM</span>
              </div>
            </address>

            <div class="showroom-section__actions">
              <a href="tel:+919415612726" class="btn btn-primary">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07A19.5 19.5 0 013.07 9.81a19.79 19.79 0 01-3.07-8.66A2 2 0 012 .18h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L6.09 7.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7a2 2 0 011.72 2.03z"/></svg>
                Call Us
              </a>
              <a href="https://wa.me/919415612726" target="_blank" rel="noopener" class="btn btn-outline">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/></svg>
                WhatsApp
              </a>
              <RouterLink to="/contact" class="btn btn-ghost">View on Map →</RouterLink>
            </div>
          </div>
        </div>
      </div>
    </section>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { productsApi } from '@/services/products'
import { categoriesApi } from '@/services/categories'
import ProductCard from '@/components/product/ProductCard.vue'

const featuredProducts = ref([])
const categories = ref([])
const featuredLoading = ref(true)
const categoriesLoading = ref(true)

const categoryColors = {
  bedroom: '#C8B89A',
  'living-room': '#B8A896',
  'dining-room': '#A89880',
  office: '#98887A',
  'home-decor': '#B0A090',
  'custom-furniture': '#887870',
}

onMounted(async () => {
  try {
    const [featuredRes, catsRes] = await Promise.all([
      productsApi.getFeatured(6),
      categoriesApi.getAll(),
    ])
    featuredProducts.value = featuredRes.data || []
    categories.value = catsRes.data || []
  } catch (error) {
    console.error('Failed to load homepage data:', error)
  } finally {
    featuredLoading.value = false
    categoriesLoading.value = false
  }
})
</script>

<style scoped>
/* ─── Hero ───────────────────────── */
.hero {
  position: relative;
  height: 100svh;
  min-height: 600px;
  display: flex;
  align-items: center;
}

.hero__image-wrap {
  position: absolute;
  inset: 0;
  overflow: hidden;
}

.hero__image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}

.hero__tint {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    to right,
    rgba(26, 26, 26, 0.55) 0%,
    rgba(26, 26, 26, 0.2) 60%,
    transparent 100%
  );
}

.hero__content {
  position: relative;
  z-index: 1;
  padding-inline: var(--container-pad);
  max-width: var(--container-max);
  margin-inline: auto;
  width: 100%;
}

.hero__eyebrow {
  color: rgba(240, 235, 227, 0.7);
  margin-bottom: var(--space-5);
}

.hero__title {
  font-family: var(--font-display);
  font-size: clamp(3rem, 6vw, 5.5rem);
  font-weight: 400;
  color: var(--color-ivory);
  line-height: 1.1;
  letter-spacing: -0.02em;
  margin-bottom: var(--space-6);
  max-width: 14ch;
}

.hero__subtitle {
  font-size: var(--text-md);
  color: rgba(240, 235, 227, 0.8);
  line-height: var(--leading-relaxed);
  margin-bottom: var(--space-10);
  max-width: 40ch;
}

.hero__actions {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-4);
}

.hero__contact-btn {
  border-color: rgba(240, 235, 227, 0.5);
  color: var(--color-ivory);
}

.hero__contact-btn:hover {
  background: rgba(240, 235, 227, 0.1);
  border-color: var(--color-ivory);
}

/* Scroll hint */
.hero__scroll {
  position: absolute;
  bottom: var(--space-8);
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-2);
  z-index: 1;
}

.hero__scroll span {
  font-size: var(--text-xs);
  letter-spacing: var(--tracking-widest);
  text-transform: uppercase;
  color: rgba(240, 235, 227, 0.5);
}

.hero__scroll-line {
  width: 1px;
  height: 40px;
  background: rgba(240, 235, 227, 0.3);
  animation: scrollPulse 2s ease-in-out infinite;
}

@keyframes scrollPulse {
  0%, 100% { opacity: 0.3; transform: scaleY(1); }
  50% { opacity: 0.8; transform: scaleY(0.7); }
}

/* ─── Brand Intro ────────────────── */
.brand-intro__layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-20);
  align-items: center;
}

.brand-intro__body {
  color: var(--text-secondary);
  line-height: var(--leading-relaxed);
  margin-bottom: var(--space-5);
  max-width: 50ch;
}

.brand-intro__link {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--text-sm);
  font-weight: 500;
  letter-spacing: var(--tracking-wide);
  text-transform: uppercase;
  color: var(--text-primary);
  border-bottom: 1px solid var(--color-charcoal);
  padding-bottom: 2px;
  transition: all var(--transition-base);
  margin-top: var(--space-4);
}

.brand-intro__link:hover {
  color: var(--color-brass);
  border-color: var(--color-brass);
  gap: var(--space-3);
}

/* ─── Collections Strip ──────────── */
.collections-section__header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  margin-bottom: var(--space-10);
}

.collections-strip {
  overflow-x: auto;
  padding-inline: var(--container-pad);
  padding-bottom: var(--space-4);
  scrollbar-width: thin;
  max-width: var(--container-wide);
  margin-inline: auto;
}

.collections-strip__inner {
  display: flex;
  gap: var(--space-5);
  min-width: max-content;
}

.collection-card {
  flex-shrink: 0;
  width: 220px;
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.collection-card__image-wrap {
  position: relative;
  overflow: hidden;
}

.collection-card__placeholder {
  position: absolute;
  inset: 0;
}

.collection-card__image {
  transition: transform var(--transition-image);
}

.collection-card:hover .collection-card__image {
  transform: scale(1.05);
}

.collection-card__overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(26,26,26,0.4), transparent 50%);
}

.collection-card__label {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.collection-card__name {
  font-family: var(--font-display);
  font-size: var(--text-lg);
  font-weight: 400;
  color: var(--text-primary);
  transition: color var(--transition-fast);
}

.collection-card:hover .collection-card__name {
  color: var(--color-brass);
}

.collection-card__count {
  font-size: var(--text-xs);
  color: var(--text-muted);
  letter-spacing: var(--tracking-wide);
  text-transform: uppercase;
}

.collection-card--skeleton .aspect-portrait {
  animation: shimmer 1.5s ease-in-out infinite;
}

@keyframes shimmer {
  0%, 100% { opacity: 0.5; }
  50% { opacity: 1; }
}

/* ─── Featured Grid ──────────────── */
.featured-section__header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  margin-bottom: var(--space-10);
}

.featured-grid {
  display: grid;
  grid-template-columns: 1.4fr 1fr;
  gap: var(--space-6);
}

.featured-grid__side {
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
}

.skeleton-card {
  background: var(--color-ivory-dark);
  animation: shimmer 1.5s ease-in-out infinite;
}

/* ─── Craft Banner ───────────────── */
.craft-banner {
  position: relative;
  min-height: 500px;
  display: flex;
  align-items: center;
  padding-block: var(--space-24);
}

.craft-banner__image-wrap {
  position: absolute;
  inset: 0;
  overflow: hidden;
}

.craft-banner__image {
  width: 100%;
  height: 100%;
}

.craft-banner__tint {
  position: absolute;
  inset: 0;
  background: rgba(26, 26, 26, 0.72);
}

.craft-banner__content {
  position: relative;
  z-index: 1;
}

.craft-banner__title {
  color: var(--color-ivory);
  margin-bottom: var(--space-12);
}

.craft-banner__points {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-10);
}

.craft-point__title {
  font-family: var(--font-display);
  font-size: var(--text-lg);
  font-weight: 400;
  color: var(--color-ivory);
  margin-bottom: var(--space-3);
}

.craft-point__desc {
  font-size: var(--text-sm);
  color: rgba(232, 228, 220, 0.7);
  line-height: var(--leading-relaxed);
}

/* ─── Showroom Section ───────────── */
.showroom-section__layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-20);
  align-items: center;
}

.showroom-section__desc {
  color: var(--text-secondary);
  line-height: var(--leading-relaxed);
  margin-bottom: var(--space-8);
  max-width: 46ch;
}

.showroom-address {
  font-style: normal;
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
  margin-bottom: var(--space-8);
}

.showroom-info-item {
  display: flex;
  align-items: flex-start;
  gap: var(--space-3);
  font-size: var(--text-sm);
  color: var(--text-secondary);
  line-height: var(--leading-relaxed);
}

.showroom-info-item svg {
  flex-shrink: 0;
  margin-top: 2px;
  color: var(--color-brass);
}

.showroom-info-item strong {
  color: var(--text-primary);
}

.showroom-section__actions {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-3);
  align-items: center;
}

/* ─── Responsive ─────────────────── */
@media (max-width: 900px) {
  .brand-intro__layout,
  .showroom-section__layout {
    grid-template-columns: 1fr;
    gap: var(--space-10);
  }

  .featured-grid {
    grid-template-columns: 1fr;
  }

  .featured-grid__side {
    flex-direction: row;
  }

  .craft-banner__points {
    grid-template-columns: 1fr;
    gap: var(--space-8);
  }
}

@media (max-width: 600px) {
  .hero__title {
    font-size: 2.5rem;
  }
  .hero__actions {
    flex-direction: column;
    align-items: flex-start;
  }
  .collections-section__header {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--space-4);
  }
  .featured-section__header {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--space-4);
  }
  .featured-grid__side {
    flex-direction: column;
  }
  .showroom-section__actions {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
