<template>
  <div class="gallery">
    <!-- Main Image -->
    <div class="gallery__main" @click="openLightbox(activeIndex)">
      <div class="aspect-product gallery__main-wrap">
        <img
          v-if="images[activeIndex]"
          :key="images[activeIndex].id"
          :src="images[activeIndex].image_url"
          :alt="images[activeIndex].alt_text || productName"
          class="gallery__main-image img-cover"
          loading="eager"
        />
        <div v-else class="gallery__placeholder">No image available</div>
      </div>
      <button v-if="images.length > 0" class="gallery__zoom-hint" aria-label="Click to zoom">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">
          <circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35M11 8v6M8 11h6"/>
        </svg>
      </button>

      <!-- Nav arrows for main image -->
      <button
        v-if="images.length > 1"
        class="gallery__arrow gallery__arrow--prev"
        @click.stop="prev"
        aria-label="Previous image"
      >
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">
          <polyline points="15 18 9 12 15 6"/>
        </svg>
      </button>
      <button
        v-if="images.length > 1"
        class="gallery__arrow gallery__arrow--next"
        @click.stop="next"
        aria-label="Next image"
      >
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">
          <polyline points="9 18 15 12 9 6"/>
        </svg>
      </button>
    </div>

    <!-- Thumbnails -->
    <div v-if="images.length > 1" class="gallery__thumbs" role="list" aria-label="Product images">
      <button
        v-for="(img, idx) in images"
        :key="img.id"
        class="gallery__thumb"
        :class="{ 'gallery__thumb--active': idx === activeIndex }"
        @click="activeIndex = idx"
        :aria-label="`View image ${idx + 1}`"
        :aria-pressed="idx === activeIndex"
        role="listitem"
      >
        <img
          :src="img.image_url"
          :alt="img.alt_text || productName"
          class="gallery__thumb-image img-cover"
          loading="lazy"
          width="120"
          height="120"
        />
      </button>
    </div>

    <!-- Lightbox -->
    <Teleport to="body">
      <Transition name="lightbox">
        <div
          v-if="lightboxOpen"
          class="lightbox"
          @click.self="lightboxOpen = false"
          role="dialog"
          aria-modal="true"
          aria-label="Image lightbox"
          @keydown.esc="lightboxOpen = false"
          @keydown.left="prev"
          @keydown.right="next"
          tabindex="0"
        >
          <button class="lightbox__close" @click="lightboxOpen = false" aria-label="Close lightbox">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">
              <path d="M18 6L6 18M6 6l12 12"/>
            </svg>
          </button>
          <button v-if="images.length > 1" class="lightbox__arrow lightbox__arrow--prev" @click="prev" aria-label="Previous">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">
              <polyline points="15 18 9 12 15 6"/>
            </svg>
          </button>
          <img
            :src="images[lightboxIndex]?.image_url"
            :alt="images[lightboxIndex]?.alt_text || productName"
            class="lightbox__image"
          />
          <button v-if="images.length > 1" class="lightbox__arrow lightbox__arrow--next" @click="next" aria-label="Next">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">
              <polyline points="9 18 15 12 9 6"/>
            </svg>
          </button>
          <div class="lightbox__counter" aria-live="polite">{{ lightboxIndex + 1 }} / {{ images.length }}</div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  images: { type: Array, required: true },
  productName: { type: String, default: 'Product image' },
})

const activeIndex = ref(0)
const lightboxOpen = ref(false)
const lightboxIndex = ref(0)

function prev() {
  const target = (activeIndex.value - 1 + props.images.length) % props.images.length
  activeIndex.value = target
  lightboxIndex.value = target
}

function next() {
  const target = (activeIndex.value + 1) % props.images.length
  activeIndex.value = target
  lightboxIndex.value = target
}

function openLightbox(idx) {
  lightboxIndex.value = idx
  lightboxOpen.value = true
}
</script>

<style scoped>
/* ─── Main Image ──────────────────── */
.gallery__main {
  position: relative;
  cursor: zoom-in;
}

.gallery__main-wrap {
  overflow: hidden;
  background: var(--color-ivory-mid);
}

.gallery__main-image {
  transition: transform var(--transition-image);
}

.gallery__main:hover .gallery__main-image {
  transform: scale(1.02);
}

.gallery__placeholder {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-ivory-mid);
  color: var(--text-muted);
  font-size: var(--text-sm);
}

/* Zoom hint */
.gallery__zoom-hint {
  position: absolute;
  bottom: var(--space-4);
  right: var(--space-4);
  width: 36px;
  height: 36px;
  background: rgba(248, 245, 240, 0.9);
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
  opacity: 0;
  transition: opacity var(--transition-base);
}

.gallery__main:hover .gallery__zoom-hint {
  opacity: 1;
}

/* Arrows */
.gallery__arrow {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 40px;
  height: 40px;
  background: rgba(248, 245, 240, 0.9);
  backdrop-filter: blur(4px);
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-primary);
  opacity: 0;
  transition: opacity var(--transition-fast);
  z-index: 2;
}

.gallery__main:hover .gallery__arrow {
  opacity: 1;
}

.gallery__arrow:hover {
  background: var(--color-ivory);
}

.gallery__arrow--prev { left: var(--space-3); }
.gallery__arrow--next { right: var(--space-3); }

/* ─── Thumbnails ──────────────────── */
.gallery__thumbs {
  display: flex;
  gap: var(--space-2);
  margin-top: var(--space-3);
  overflow-x: auto;
  padding-bottom: var(--space-1);
  scrollbar-width: thin;
}

.gallery__thumb {
  flex-shrink: 0;
  width: 72px;
  height: 72px;
  overflow: hidden;
  border: 2px solid transparent;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: border-color var(--transition-fast);
}

.gallery__thumb--active,
.gallery__thumb:hover {
  border-color: var(--color-charcoal);
}

.gallery__thumb-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform var(--transition-base);
}

.gallery__thumb:hover .gallery__thumb-image {
  transform: scale(1.05);
}

/* ─── Lightbox ────────────────────── */
.lightbox {
  position: fixed;
  inset: 0;
  background: rgba(10, 10, 10, 0.95);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: var(--z-modal);
  padding: var(--space-6);
}

.lightbox__close {
  position: absolute;
  top: var(--space-5);
  right: var(--space-5);
  color: rgba(255,255,255,0.7);
  transition: color var(--transition-fast);
  padding: var(--space-2);
}

.lightbox__close:hover {
  color: white;
}

.lightbox__image {
  max-width: 90vw;
  max-height: 90vh;
  object-fit: contain;
  border-radius: var(--radius-sm);
}

.lightbox__arrow {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  color: rgba(255,255,255,0.7);
  padding: var(--space-4);
  transition: color var(--transition-fast);
}

.lightbox__arrow:hover { color: white; }
.lightbox__arrow--prev { left: var(--space-4); }
.lightbox__arrow--next { right: var(--space-4); }

.lightbox__counter {
  position: absolute;
  bottom: var(--space-5);
  left: 50%;
  transform: translateX(-50%);
  font-size: var(--text-sm);
  color: rgba(255,255,255,0.5);
  letter-spacing: var(--tracking-wide);
}

.lightbox-enter-active, .lightbox-leave-active {
  transition: opacity 0.2s ease;
}
.lightbox-enter-from, .lightbox-leave-to {
  opacity: 0;
}
</style>
