<template>
  <div class="not-found" style="min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: var(--space-12);">
    <p class="section-label" style="margin-bottom: var(--space-4);">404</p>
    <h1 class="heading-sm" style="margin-bottom: var(--space-5);">Page Not Found</h1>
    <p style="color: var(--text-muted); max-width: 38ch; margin-bottom: var(--space-10); line-height: var(--leading-relaxed);">
      The page you're looking for doesn't exist or has been moved.
    </p>
    <div style="display: flex; gap: var(--space-4); flex-wrap: wrap; justify-content: center;">
      <RouterLink to="/" class="btn btn-primary">Back to Home</RouterLink>
      <RouterLink to="/products" class="btn btn-outline">Browse Products</RouterLink>
    </div>
  </div>
</template>
