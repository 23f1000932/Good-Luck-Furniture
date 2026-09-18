<template>
  <article class="product-card" :class="`product-card--${variant}`">
    <RouterLink :to="`/products/${product.slug}`" class="product-card__image-link" :aria-label="product.name">
      <div class="product-card__image-wrap" :class="aspectClass">
        <img
          v-if="primaryImage"
          :src="primaryImage.image_url"
          :alt="primaryImage.alt_text || product.name"
          class="product-card__image img-cover"
          loading="lazy"
          width="600"
          height="750"
        />
        <div v-else class="product-card__placeholder">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" opacity="0.3" aria-hidden="true">
            <rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/>
            <polyline points="21 15 16 10 5 21"/>
          </svg>
        </div>

        <!-- Hover overlay with CTA -->
        <div class="product-card__overlay" aria-hidden="true">
          <span class="product-card__cta">View Product</span>
        </div>

        <!-- Badges -->
        <div class="product-card__badges">
          <span v-if="product.is_featured" class="badge badge--featured">Featured</span>
        </div>
      </div>
    </RouterLink>

    <div class="product-card__info">
      <div class="product-card__meta">
        <span v-if="product.collection?.name" class="product-card__category">{{ product.collection.name }}</span>
        <span v-if="product.product_type" class="product-card__type"> · {{ product.product_type }}</span>
      </div>
      <h3 class="product-card__name">
        <RouterLink :to="`/products/${product.slug}`">{{ product.name }}</RouterLink>
      </h3>
      <div class="product-card__price">
        <span v-if="product.price_visibility === 'visible' && product.price" class="product-card__price-value">
          ₹{{ formatPrice(product.price) }}
        </span>
        <span v-else-if="product.price_visibility === 'contact_for_price'" class="product-card__price-contact">
          Contact for Price
        </span>
      </div>
    </div>
  </article>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  product: { type: Object, required: true },
  variant: { type: String, default: 'default' }, // default | large | compact
})

const primaryImage = computed(() =>
  props.product.primary_image ||
  (props.product.images && props.product.images[0]) ||
  null
)

const aspectClass = computed(() => {
  if (props.variant === 'large') return 'aspect-portrait'
  if (props.variant === 'compact') return 'aspect-landscape'
  return 'aspect-product'
})

function formatPrice(price) {
  return Number(price).toLocaleString('en-IN')
}
</script>

<style scoped>
.product-card {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

/* Image */
.product-card__image-link {
  display: block;
  overflow: hidden;
}

.product-card__image-wrap {
  position: relative;
  overflow: hidden;
  background: var(--color-ivory-mid);
}

.product-card__image {
  transition: transform var(--transition-image);
}

.product-card__image-link:hover .product-card__image {
  transform: scale(1.04);
}

/* Placeholder */
.product-card__placeholder {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-ivory-mid);
  color: var(--text-muted);
}

/* Hover overlay */
.product-card__overlay {
  position: absolute;
  inset: 0;
  background: rgba(26, 26, 26, 0.35);
  display: flex;
  align-items: flex-end;
  padding: var(--space-5);
  opacity: 0;
  transition: opacity var(--transition-base);
}

.product-card__image-link:hover .product-card__overlay {
  opacity: 1;
}

.product-card__cta {
  font-size: var(--text-xs);
  font-weight: 500;
  letter-spacing: var(--tracking-wider);
  text-transform: uppercase;
  color: var(--color-ivory);
  border-bottom: 1px solid rgba(248, 245, 240, 0.5);
  padding-bottom: 2px;
}

/* Badges */
.product-card__badges {
  position: absolute;
  top: var(--space-3);
  left: var(--space-3);
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

/* Info */
.product-card__info {
  padding: 0 var(--space-1);
}

.product-card__meta {
  font-size: var(--text-xs);
  color: var(--text-muted);
  letter-spacing: var(--tracking-wide);
  text-transform: uppercase;
  margin-bottom: var(--space-1);
}

.product-card__name {
  font-family: var(--font-display);
  font-size: var(--text-lg);
  font-weight: 400;
  line-height: var(--leading-snug);
  margin-bottom: var(--space-2);
}

.product-card__name a {
  color: var(--text-primary);
  transition: color var(--transition-fast);
}

.product-card__name a:hover {
  color: var(--color-brass);
}

.product-card__price-value {
  font-size: var(--text-md);
  font-weight: 500;
  color: var(--text-primary);
}

.product-card__price-contact {
  font-size: var(--text-xs);
  letter-spacing: var(--tracking-wide);
  text-transform: uppercase;
  color: var(--color-brass);
}

/* ─── Variants ────────────────────── */
.product-card--large .product-card__name {
  font-size: var(--text-xl);
}

.product-card--compact .product-card__name {
  font-size: var(--text-base);
}
</style>
