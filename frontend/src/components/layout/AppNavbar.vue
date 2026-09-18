<template>
  <header class="navbar" :class="{ 'navbar--scrolled': isScrolled, 'navbar--dark': isDarkPage }">
    <div class="navbar__inner">
      <!-- Logo -->
      <RouterLink to="/" class="navbar__logo" aria-label="Good Luck Furniture — Home">
        <span class="navbar__logo-text">Good Luck Furniture</span>
      </RouterLink>

      <!-- Desktop Navigation -->
      <nav class="navbar__nav" aria-label="Main navigation">
        <RouterLink to="/" class="navbar__link" exact-active-class="navbar__link--active">Home</RouterLink>
        <RouterLink to="/collections" class="navbar__link" active-class="navbar__link--active">Collections</RouterLink>
        <RouterLink to="/products" class="navbar__link" active-class="navbar__link--active">Products</RouterLink>
        <RouterLink to="/about" class="navbar__link" active-class="navbar__link--active">About</RouterLink>
        <RouterLink to="/contact" class="navbar__link" active-class="navbar__link--active">Contact</RouterLink>
      </nav>

      <!-- CTA -->
      <div class="navbar__actions">
        <a
          href="https://wa.me/919415612726"
          target="_blank"
          rel="noopener"
          class="navbar__cta"
          aria-label="WhatsApp us"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
            <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/>
          </svg>
          <span>WhatsApp</span>
        </a>

        <!-- Mobile hamburger -->
        <button
          class="navbar__hamburger"
          @click="mobileOpen = true"
          aria-label="Open navigation menu"
          aria-expanded="false"
        >
          <span></span>
          <span></span>
          <span></span>
        </button>
      </div>
    </div>
  </header>

  <!-- Mobile Navigation -->
  <Teleport to="body">
    <Transition name="mobile-nav">
      <div v-if="mobileOpen" class="mobile-nav" role="dialog" aria-modal="true" aria-label="Navigation menu">
        <div class="mobile-nav__overlay" @click="mobileOpen = false"></div>
        <div class="mobile-nav__panel">
          <div class="mobile-nav__header">
            <span class="mobile-nav__logo">Good Luck Furniture</span>
            <button class="mobile-nav__close" @click="mobileOpen = false" aria-label="Close menu">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M18 6L6 18M6 6l12 12"/>
              </svg>
            </button>
          </div>
          <nav class="mobile-nav__links" aria-label="Mobile navigation">
            <RouterLink to="/" class="mobile-nav__link" @click="mobileOpen = false">Home</RouterLink>
            <RouterLink to="/collections" class="mobile-nav__link" @click="mobileOpen = false">Collections</RouterLink>
            <RouterLink to="/products" class="mobile-nav__link" @click="mobileOpen = false">Products</RouterLink>
            <RouterLink to="/about" class="mobile-nav__link" @click="mobileOpen = false">About</RouterLink>
            <RouterLink to="/contact" class="mobile-nav__link" @click="mobileOpen = false">Contact</RouterLink>
          </nav>
          <div class="mobile-nav__footer">
            <a href="tel:+919415612726" class="mobile-nav__contact">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">
                <path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07A19.5 19.5 0 013.07 9.81a19.79 19.79 0 01-3.07-8.66A2 2 0 012 .18h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L6.09 7.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7a2 2 0 011.72 2.03z"/>
              </svg>
              9415612726
            </a>
            <a href="https://wa.me/919415612726" target="_blank" rel="noopener" class="mobile-nav__whatsapp">
              WhatsApp Us
            </a>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useRoute } from 'vue-router'

const isScrolled = ref(false)
const mobileOpen = ref(false)
const route = useRoute()

// Pages where navbar starts transparent over dark hero
const isDarkPage = ref(false)

function onScroll() {
  isScrolled.value = window.scrollY > 40
}

onMounted(() => {
  window.addEventListener('scroll', onScroll, { passive: true })
})

onUnmounted(() => {
  window.removeEventListener('scroll', onScroll)
})

// Close mobile nav on route change
watch(() => route.path, () => {
  mobileOpen.value = false
})
</script>

<style scoped>
/* ─── Navbar ─────────────────────────────────────── */
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: var(--z-nav);
  transition: background var(--transition-base), box-shadow var(--transition-base);
  background: transparent;
}

.navbar--scrolled {
  background: rgba(248, 245, 240, 0.96);
  backdrop-filter: blur(12px);
  box-shadow: 0 1px 0 var(--border-light);
}

.navbar__inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 var(--container-pad);
  height: 72px;
  max-width: var(--container-wide);
  margin-inline: auto;
}

/* Logo */
.navbar__logo {
  display: flex;
  align-items: center;
  flex-shrink: 0;
}

.navbar__logo-text {
  font-family: var(--font-display);
  font-size: var(--text-lg);
  font-weight: 500;
  color: var(--color-charcoal);
  letter-spacing: var(--tracking-tight);
  transition: color var(--transition-fast);
}

.navbar__logo:hover .navbar__logo-text {
  color: var(--color-brass);
}

/* Desktop Nav Links */
.navbar__nav {
  display: flex;
  align-items: center;
  gap: var(--space-8);
}

.navbar__link {
  font-family: var(--font-sans);
  font-size: var(--text-xs);
  font-weight: 500;
  letter-spacing: var(--tracking-wider);
  text-transform: uppercase;
  color: var(--text-secondary);
  transition: color var(--transition-fast);
  position: relative;
}

.navbar__link::after {
  content: '';
  position: absolute;
  bottom: -4px;
  left: 0;
  right: 0;
  height: 1px;
  background: var(--color-brass);
  transform: scaleX(0);
  transition: transform var(--transition-base);
  transform-origin: left;
}

.navbar__link:hover,
.navbar__link--active {
  color: var(--text-primary);
}

.navbar__link:hover::after,
.navbar__link--active::after {
  transform: scaleX(1);
}

/* Actions */
.navbar__actions {
  display: flex;
  align-items: center;
  gap: var(--space-4);
}

.navbar__cta {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--text-xs);
  font-weight: 500;
  letter-spacing: var(--tracking-wide);
  text-transform: uppercase;
  color: var(--text-secondary);
  padding: 0.5rem 1rem;
  border: 1px solid var(--border-mid);
  border-radius: var(--radius-sm);
  transition: all var(--transition-base);
}

.navbar__cta:hover {
  background: var(--color-charcoal);
  color: var(--color-ivory);
  border-color: var(--color-charcoal);
}

/* Hamburger */
.navbar__hamburger {
  display: none;
  flex-direction: column;
  gap: 5px;
  padding: var(--space-2);
  cursor: pointer;
}

.navbar__hamburger span {
  display: block;
  width: 22px;
  height: 1.5px;
  background: var(--color-charcoal);
  transition: all var(--transition-base);
}

/* ─── Mobile Navigation ──────────────────────────── */
.mobile-nav {
  position: fixed;
  inset: 0;
  z-index: var(--z-overlay);
}

.mobile-nav__overlay {
  position: absolute;
  inset: 0;
  background: rgba(26, 26, 26, 0.5);
  backdrop-filter: blur(4px);
}

.mobile-nav__panel {
  position: absolute;
  right: 0;
  top: 0;
  bottom: 0;
  width: min(320px, 85vw);
  background: var(--color-ivory);
  display: flex;
  flex-direction: column;
  padding: var(--space-8);
}

.mobile-nav__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-12);
}

.mobile-nav__logo {
  font-family: var(--font-display);
  font-size: var(--text-md);
  font-weight: 500;
  color: var(--color-charcoal);
}

.mobile-nav__close {
  color: var(--text-muted);
  transition: color var(--transition-fast);
  padding: var(--space-1);
}

.mobile-nav__close:hover {
  color: var(--text-primary);
}

.mobile-nav__links {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
  flex: 1;
}

.mobile-nav__link {
  font-size: var(--text-lg);
  font-family: var(--font-display);
  font-weight: 400;
  color: var(--text-secondary);
  padding: var(--space-3) 0;
  border-bottom: 1px solid var(--border-light);
  transition: color var(--transition-fast);
}

.mobile-nav__link:hover {
  color: var(--text-primary);
}

.mobile-nav__footer {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  margin-top: var(--space-8);
}

.mobile-nav__contact {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--text-sm);
  color: var(--text-secondary);
}

.mobile-nav__whatsapp {
  display: block;
  text-align: center;
  padding: 0.75rem;
  background: #25D366;
  color: white;
  font-size: var(--text-sm);
  font-weight: 500;
  letter-spacing: var(--tracking-wide);
  text-transform: uppercase;
  border-radius: var(--radius-md);
}

/* ─── Transitions ────────────────────────────────── */
.mobile-nav-enter-active,
.mobile-nav-leave-active {
  transition: opacity var(--transition-base);
}

.mobile-nav-enter-active .mobile-nav__panel,
.mobile-nav-leave-active .mobile-nav__panel {
  transition: transform var(--transition-slow);
}

.mobile-nav-enter-from,
.mobile-nav-leave-to {
  opacity: 0;
}

.mobile-nav-enter-from .mobile-nav__panel,
.mobile-nav-leave-to .mobile-nav__panel {
  transform: translateX(100%);
}

/* ─── Responsive ─────────────────────────────────── */
@media (max-width: 768px) {
  .navbar__nav,
  .navbar__cta {
    display: none;
  }

  .navbar__hamburger {
    display: flex;
  }
}
</style>
