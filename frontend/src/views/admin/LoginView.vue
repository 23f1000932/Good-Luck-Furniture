<template>
  <div class="admin-login-page">
    <div class="admin-login-brand">
      <div class="admin-login-brand__inner">
        <RouterLink to="/" class="admin-login-brand__logo">Good Luck Furniture</RouterLink>
        <p class="admin-login-brand__tagline">Furniture for the way you live.</p>
        <img
          src="https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=1200&q=80"
          alt="Good Luck Furniture showroom"
          class="admin-login-brand__image"
          loading="lazy"
        />
      </div>
    </div>

    <div class="admin-login-form-wrap">
      <div class="admin-login-form-inner">
        <div class="admin-login-header">
          <h1 class="admin-login-header__title">Admin Access</h1>
          <p class="admin-login-header__sub">Sign in to manage your catalogue</p>
        </div>

        <form class="admin-form" @submit.prevent="handleLogin" novalidate id="admin-login-form">
          <div class="form-group">
            <label for="login-email" class="form-label">Email Address</label>
            <input
              id="login-email"
              v-model="email"
              type="email"
              class="form-input"
              placeholder="admin@example.com"
              required
              autocomplete="email"
              :disabled="loading"
            />
          </div>

          <div class="form-group">
            <label for="login-password" class="form-label">Password</label>
            <div style="position: relative;">
              <input
                id="login-password"
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                class="form-input"
                placeholder="••••••••"
                required
                autocomplete="current-password"
                :disabled="loading"
              />
              <button
                type="button"
                class="password-toggle"
                @click="showPassword = !showPassword"
                :aria-label="showPassword ? 'Hide password' : 'Show password'"
              >
                <svg v-if="showPassword" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M17.94 17.94A10.07 10.07 0 0112 20c-7 0-11-8-11-8a18.45 18.45 0 015.06-5.94M9.9 4.24A9.12 9.12 0 0112 4c7 0 11 8 11 8a18.5 18.5 0 01-2.16 3.19m-6.72-1.07a3 3 0 11-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/></svg>
                <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
              </button>
            </div>
          </div>

          <div v-if="error" class="admin-login-error" role="alert">
            {{ error }}
          </div>

          <button
            type="submit"
            class="btn btn-primary btn-lg admin-login-submit"
            :disabled="loading"
            id="login-submit"
          >
            <span v-if="loading">Signing in…</span>
            <span v-else>Sign In</span>
          </button>
        </form>

        <p class="admin-login-back">
          <RouterLink to="/" class="admin-login-back__link">← Back to website</RouterLink>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')
const showPassword = ref(false)

async function handleLogin() {
  if (!email.value || !password.value) {
    error.value = 'Please enter your email and password'
    return
  }

  loading.value = true
  error.value = ''

  const result = await authStore.login(email.value, password.value)
  loading.value = false

  if (result.success) {
    const redirect = route.query.redirect || '/admin'
    router.push(redirect)
  } else {
    error.value = result.error || 'Invalid credentials'
  }
}
</script>

<style scoped>
.admin-login-page {
  display: grid;
  grid-template-columns: 1.2fr 1fr;
  min-height: 100vh;
}

/* Brand side */
.admin-login-brand {
  position: relative;
  overflow: hidden;
}

.admin-login-brand__inner {
  position: sticky;
  top: 0;
  height: 100vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding: var(--space-12);
}

.admin-login-brand__image {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  filter: brightness(0.5);
}

.admin-login-brand__logo {
  position: relative;
  font-family: var(--font-display);
  font-size: var(--text-2xl);
  font-weight: 400;
  color: var(--color-ivory);
  margin-bottom: var(--space-3);
}

.admin-login-brand__tagline {
  position: relative;
  font-size: var(--text-md);
  color: rgba(240, 235, 227, 0.65);
}

/* Form side */
.admin-login-form-wrap {
  background: var(--color-ivory);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-12);
}

.admin-login-form-inner {
  width: 100%;
  max-width: 380px;
}

.admin-login-header {
  margin-bottom: var(--space-10);
}

.admin-login-header__title {
  font-family: var(--font-display);
  font-size: var(--text-3xl);
  font-weight: 400;
  margin-bottom: var(--space-2);
}

.admin-login-header__sub {
  color: var(--text-muted);
  font-size: var(--text-sm);
}

.admin-form {
  display: flex;
  flex-direction: column;
  gap: var(--space-5);
}

.password-toggle {
  position: absolute;
  right: var(--space-3);
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-muted);
  transition: color var(--transition-fast);
}

.password-toggle:hover {
  color: var(--text-primary);
}

.admin-login-error {
  padding: var(--space-3) var(--space-4);
  background: rgba(155, 48, 48, 0.1);
  border: 1px solid rgba(155, 48, 48, 0.25);
  border-radius: var(--radius-md);
  font-size: var(--text-sm);
  color: var(--color-error);
}

.admin-login-submit {
  width: 100%;
  justify-content: center;
}

.admin-login-back {
  margin-top: var(--space-8);
  text-align: center;
}

.admin-login-back__link {
  font-size: var(--text-sm);
  color: var(--text-muted);
  transition: color var(--transition-fast);
}

.admin-login-back__link:hover {
  color: var(--text-primary);
}

@media (max-width: 768px) {
  .admin-login-page {
    grid-template-columns: 1fr;
  }
  .admin-login-brand {
    display: none;
  }
}
</style>
