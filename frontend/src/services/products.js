import api from './api'

export const productsApi = {
  getAll: (params = {}) => api.get('/products', { params }),
  getBySlug: (slug) => api.get(`/products/${slug}`),
  getFeatured: (limit = 8) => api.get('/featured-products', { params: { limit } }),
  getTypes: () => api.get('/product-types'),

  // Admin
  adminGetAll: (params = {}) => api.get('/admin/products', { params }),
  adminGetById: (id) => api.get(`/admin/products/${id}`),
  adminCreate: (data) => api.post('/admin/products', data),
  adminUpdate: (id, data) => api.put(`/admin/products/${id}`, data),
  adminDelete: (id) => api.delete(`/admin/products/${id}`),

  // Images
  uploadImages: (productId, formData) =>
    api.post(`/admin/products/${productId}/images`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),
  deleteImage: (productId, imageId) =>
    api.delete(`/admin/products/${productId}/images/${imageId}`),
  reorderImages: (productId, order) =>
    api.put(`/admin/products/${productId}/images/reorder`, { order }),
  setPrimaryImage: (productId, imageId) =>
    api.put(`/admin/products/${productId}/images/${imageId}/primary`),
}
