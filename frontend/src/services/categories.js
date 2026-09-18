import api from './api'

export const categoriesApi = {
  getAll: () => api.get('/categories'),
  getBySlug: (slug) => api.get(`/categories/${slug}`),

  // Admin
  adminGetAll: () => api.get('/admin/categories'),
  adminCreate: (data) => api.post('/admin/categories', data),
  adminUpdate: (id, data) => api.put(`/admin/categories/${id}`, data),
  adminDelete: (id) => api.delete(`/admin/categories/${id}`),
}
