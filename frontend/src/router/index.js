import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) return savedPosition
    if (to.hash) return { el: to.hash, behavior: 'smooth' }
    return { top: 0, behavior: 'smooth' }
  },
  routes: [
    // ─── Public Routes ──────────────────────────────────
    {
      path: '/',
      component: () => import('@/layouts/PublicLayout.vue'),
      children: [
        {
          path: '',
          name: 'home',
          component: () => import('@/views/HomeView.vue'),
          meta: {
            title: 'Good Luck Furniture — Premium Furniture Showroom, Prayagraj',
            description: 'Bedroom, living room, dining and office furniture. Visit our showroom at Rajrooppur, Prayagraj.',
          }
        },
        {
          path: 'collections',
          name: 'collections',
          component: () => import('@/views/CollectionsView.vue'),
          meta: {
            title: 'Collections — Good Luck Furniture',
            description: 'Browse our furniture collections by room — bedroom, living room, dining, office and more.'
          }
        },
        {
          path: 'products',
          name: 'products',
          component: () => import('@/views/ProductsView.vue'),
          meta: {
            title: 'Products — Good Luck Furniture',
            description: 'Browse our full range of furniture. Filter by collection and type.'
          }
        },
        {
          path: 'products/:slug',
          name: 'product-detail',
          component: () => import('@/views/ProductDetailView.vue'),
          meta: { title: 'Good Luck Furniture' }
        },
        {
          path: 'about',
          name: 'about',
          component: () => import('@/views/AboutView.vue'),
          meta: {
            title: 'About — Good Luck Furniture',
            description: 'Learn about Good Luck Furniture — our commitment to quality craftsmanship and materials.'
          }
        },
        {
          path: 'contact',
          name: 'contact',
          component: () => import('@/views/ContactView.vue'),
          meta: {
            title: 'Contact Us — Good Luck Furniture',
            description: 'Visit our showroom at Rajrooppur, Prayagraj. Open 11 AM – 9 PM. Call or WhatsApp 9415612726.'
          }
        },
      ]
    },

    // ─── Admin Routes ────────────────────────────────────
    {
      path: '/admin/login',
      name: 'admin-login',
      component: () => import('@/views/admin/LoginView.vue'),
      meta: { title: 'Admin Login — Good Luck Furniture', isAdminLogin: true }
    },
    {
      path: '/admin',
      component: () => import('@/layouts/AdminLayout.vue'),
      meta: { requiresAuth: true },
      children: [
        {
          path: '',
          name: 'admin-dashboard',
          component: () => import('@/views/admin/DashboardView.vue'),
          meta: { title: 'Dashboard — Admin' }
        },
        {
          path: 'products',
          name: 'admin-products',
          component: () => import('@/views/admin/ProductsListView.vue'),
          meta: { title: 'Products — Admin' }
        },
        {
          path: 'products/new',
          name: 'admin-product-new',
          component: () => import('@/views/admin/ProductFormView.vue'),
          meta: { title: 'New Product — Admin' }
        },
        {
          path: 'products/:id/edit',
          name: 'admin-product-edit',
          component: () => import('@/views/admin/ProductFormView.vue'),
          meta: { title: 'Edit Product — Admin' }
        },
        {
          path: 'categories',
          name: 'admin-categories',
          component: () => import('@/views/admin/CategoriesView.vue'),
          meta: { title: 'Categories — Admin' }
        },
        {
          path: 'settings',
          name: 'admin-settings',
          component: () => import('@/views/admin/SettingsView.vue'),
          meta: { title: 'Settings — Admin' }
        },
      ]
    },

    // ─── 404 ─────────────────────────────────────────────
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('@/views/NotFoundView.vue'),
      meta: { title: 'Page Not Found — Good Luck Furniture' }
    }
  ]
})

// Navigation guard — protect admin routes
router.beforeEach((to, from, next) => {
  // Update page title
  document.title = to.meta.title || 'Good Luck Furniture'

  if (to.meta.requiresAuth) {
    const authStore = useAuthStore()
    if (!authStore.isAuthenticated) {
      return next({ name: 'admin-login', query: { redirect: to.fullPath } })
    }
  }

  // Redirect already-authenticated users away from login
  if (to.meta.isAdminLogin) {
    const authStore = useAuthStore()
    if (authStore.isAuthenticated) {
      return next({ name: 'admin-dashboard' })
    }
  }

  next()
})

export default router
