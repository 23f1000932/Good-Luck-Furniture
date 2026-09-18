<template>
  <div class="product-form-view">

    <!-- Loading (edit mode) -->
    <div v-if="loadingProduct" class="admin-loading-state">
      <div v-for="n in 3" :key="n" class="skeleton-row" style="height: 60px; margin-bottom: 12px;"></div>
    </div>

    <form v-else @submit.prevent="handleSubmit" novalidate :id="isEdit ? 'edit-product-form' : 'new-product-form'">
      <div class="form-layout">

        <!-- ─── Main Details ──────────────────────── -->
        <div class="form-card">
          <h2 class="form-card__title">Product Details</h2>

          <div class="form-grid">
            <div class="form-group form-col--full">
              <label for="product-name" class="form-label">Product Name *</label>
              <input id="product-name" v-model="form.name" type="text" class="form-input" placeholder="e.g. Queen Size Bed with Storage" required :class="{ 'form-input--error': errors.name }" />
              <span v-if="errors.name" class="form-error">{{ errors.name }}</span>
            </div>

            <div class="form-group form-col--full">
              <label for="product-slug" class="form-label">URL Slug</label>
              <div class="slug-field">
                <span class="slug-field__prefix">/products/</span>
                <input id="product-slug" v-model="form.slug" type="text" class="form-input" placeholder="auto-generated from name" />
              </div>
            </div>

            <div class="form-group">
              <label for="product-collection" class="form-label">Collection *</label>
              <select id="product-collection" v-model="form.collection_id" class="form-select" required :class="{ 'form-input--error': errors.collection_id }">
                <option value="">Select a collection</option>
                <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
              </select>
              <span v-if="errors.collection_id" class="form-error">{{ errors.collection_id }}</span>
            </div>

            <div class="form-group">
              <label for="product-type" class="form-label">Product Type</label>
              <input id="product-type" v-model="form.product_type" type="text" class="form-input" placeholder="e.g. Sofa, Wardrobe, Dining Table" list="product-type-suggestions" />
              <datalist id="product-type-suggestions">
                <option v-for="t in commonTypes" :key="t" :value="t" />
              </datalist>
            </div>

            <div class="form-group form-col--full">
              <label for="product-short-desc" class="form-label">Short Description</label>
              <textarea id="product-short-desc" v-model="form.short_description" class="form-textarea" style="min-height: 80px;" placeholder="A brief, compelling description (shown on product page header)"></textarea>
            </div>

            <div class="form-group form-col--full">
              <label for="product-description" class="form-label">Full Description</label>
              <textarea id="product-description" v-model="form.description" class="form-textarea" placeholder="Detailed description — construction, materials, care, etc."></textarea>
            </div>
          </div>
        </div>

        <!-- ─── Pricing & Status ──────────────────── -->
        <div class="form-card">
          <h2 class="form-card__title">Pricing & Status</h2>
          <div class="form-grid">

            <div class="form-group">
              <label for="product-price-visibility" class="form-label">Price Display</label>
              <select id="product-price-visibility" v-model="form.price_visibility" class="form-select">
                <option value="hidden">Hidden</option>
                <option value="visible">Show Price</option>
                <option value="contact_for_price">Contact for Price</option>
              </select>
            </div>

            <div class="form-group" v-if="form.price_visibility === 'visible'">
              <label for="product-price" class="form-label">Price (₹)</label>
              <input id="product-price" v-model="form.price" type="number" min="0" step="1" class="form-input" placeholder="0" />
            </div>

            <div class="form-group">
              <label class="form-label">Status</label>
              <div class="toggle-group">
                <label class="toggle">
                  <input id="product-active" type="checkbox" v-model="form.is_active" />
                  <span class="toggle__track"><span class="toggle__thumb"></span></span>
                  <span class="toggle__label">{{ form.is_active ? 'Published' : 'Draft' }}</span>
                </label>
              </div>
            </div>

            <div class="form-group">
              <label class="form-label">Featured</label>
              <div class="toggle-group">
                <label class="toggle">
                  <input id="product-featured" type="checkbox" v-model="form.is_featured" />
                  <span class="toggle__track"><span class="toggle__thumb"></span></span>
                  <span class="toggle__label">{{ form.is_featured ? 'Featured on homepage' : 'Not featured' }}</span>
                </label>
              </div>
            </div>
          </div>
        </div>

        <!-- ─── Specifications ────────────────────── -->
        <div class="form-card">
          <h2 class="form-card__title">Specifications</h2>
          <div class="form-grid">
            <div class="form-group">
              <label for="product-material" class="form-label">Material</label>
              <input id="product-material" v-model="form.material" type="text" class="form-input" placeholder="e.g. Solid Sheesham Wood" />
            </div>
            <div class="form-group">
              <label for="product-finish" class="form-label">Finish</label>
              <input id="product-finish" v-model="form.finish" type="text" class="form-input" placeholder="e.g. Walnut Polish" />
            </div>
            <div class="form-group">
              <label for="product-color" class="form-label">Color</label>
              <input id="product-color" v-model="form.color" type="text" class="form-input" placeholder="e.g. Brown" />
            </div>
            <div class="form-group">
              <label for="product-dimensions" class="form-label">Dimensions</label>
              <input id="product-dimensions" v-model="form.dimensions" type="text" class="form-input" placeholder="e.g. 180cm × 200cm (King)" />
            </div>
          </div>
        </div>

        <!-- ─── Images ────────────────────────────── -->
        <div class="form-card" v-if="isEdit">
          <h2 class="form-card__title">Product Images</h2>
          <p class="form-card__hint">Upload high-quality photos. First image is shown as the main product image. Drag to reorder.</p>

          <!-- Existing Images -->
          <div class="images-grid" v-if="existingImages.length > 0">
            <div v-for="img in existingImages" :key="img.id" class="image-item">
              <div class="image-item__preview">
                <img :src="img.image_url" :alt="img.alt_text || 'Product image'" class="img-cover" loading="lazy" />
                <button
                  class="image-item__remove"
                  @click="removeImage(img)"
                  :aria-label="`Remove image`"
                  type="button"
                >
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M18 6L6 18M6 6l12 12"/></svg>
                </button>
                <div v-if="img.is_primary" class="image-item__primary-badge">Primary</div>
              </div>
              <button
                v-if="!img.is_primary"
                type="button"
                class="image-item__set-primary"
                @click="setPrimary(img)"
              >Set as primary</button>
            </div>
          </div>

          <!-- Upload Area -->
          <div
            class="upload-area"
            :class="{ 'upload-area--drag': isDragging }"
            @dragover.prevent="isDragging = true"
            @dragleave="isDragging = false"
            @drop.prevent="handleDrop"
            @click="$refs.fileInput.click()"
            role="button"
            tabindex="0"
            @keydown.enter="$refs.fileInput.click()"
            aria-label="Upload images"
          >
            <input
              ref="fileInput"
              type="file"
              accept="image/*"
              multiple
              class="visually-hidden"
              @change="handleFileSelect"
              id="image-upload-input"
            />
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" opacity="0.4" aria-hidden="true">
              <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/>
            </svg>
            <p class="upload-area__text">Click to upload or drag images here</p>
            <p class="upload-area__hint">JPEG, PNG or WebP · Max 5 MB each</p>
          </div>

          <!-- Upload progress -->
          <div v-if="uploading" class="upload-progress">
            <div class="upload-progress__bar">
              <div class="upload-progress__fill" :style="{ width: uploadProgress + '%' }"></div>
            </div>
            <span class="upload-progress__text">Uploading {{ uploadProgress }}%…</span>
          </div>
        </div>

        <div class="form-card" v-else>
          <h2 class="form-card__title">Images</h2>
          <p class="form-card__hint" style="padding-bottom: var(--space-4);">
            Save the product first, then you can upload images from the edit page.
          </p>
        </div>

      </div><!-- /form-layout -->

      <!-- Submit -->
      <div class="form-actions">
        <RouterLink to="/admin/products" class="btn btn-ghost">Cancel</RouterLink>
        <button type="submit" class="btn btn-primary" :disabled="saving" id="save-product-btn">
          {{ saving ? 'Saving…' : (isEdit ? 'Save Changes' : 'Create Product') }}
        </button>
      </div>

      <!-- Error Summary -->
      <div v-if="submitError" class="submit-error" role="alert">{{ submitError }}</div>
    </form>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { productsApi } from '@/services/products'
import { categoriesApi } from '@/services/categories'

const route = useRoute()
const router = useRouter()

const isEdit = computed(() => !!route.params.id)
const productId = computed(() => route.params.id)

const loadingProduct = ref(isEdit.value)
const saving = ref(false)
const uploading = ref(false)
const uploadProgress = ref(0)
const isDragging = ref(false)
const submitError = ref('')
const errors = ref({})
const categories = ref([])
const existingImages = ref([])
const fileInput = ref(null)

const commonTypes = [
  'Sofa', 'Sectional Sofa', 'Loveseat', 'Armchair', 'Coffee Table', 'TV Unit',
  'Bed', 'Wardrobe', 'Dressing Table', 'Side Table', 'Chest of Drawers',
  'Dining Table', 'Dining Chair', 'Crockery Unit', 'Dining Set',
  'Office Chair', 'Office Desk', 'Bookshelf', 'Filing Cabinet',
  'Shoe Rack', 'Wall Unit', 'Display Cabinet', 'Mirror'
]

const form = reactive({
  name: '', slug: '', collection_id: '', product_type: '',
  short_description: '', description: '',
  price_visibility: 'contact_for_price', price: '',
  material: '', finish: '', color: '', dimensions: '',
  is_active: true, is_featured: false,
})

// Auto-generate slug from name
watch(() => form.name, (name) => {
  if (!isEdit.value || !form.slug) {
    form.slug = name.toLowerCase()
      .replace(/[^\w\s-]/g, '')
      .replace(/[\s_]+/g, '-')
      .replace(/-+/g, '-')
      .trim()
  }
})

function validate() {
  errors.value = {}
  if (!form.name.trim()) errors.value.name = 'Product name is required'
  if (!form.collection_id) errors.value.collection_id = 'Please select a collection'
  return Object.keys(errors.value).length === 0
}

async function handleSubmit() {
  if (!validate()) return
  saving.value = true
  submitError.value = ''
  try {
    const payload = {
      name: form.name,
      slug: form.slug || undefined,
      collection_id: form.collection_id || undefined,
      product_type: form.product_type || undefined,
      short_description: form.short_description || undefined,
      description: form.description || undefined,
      price_visibility: form.price_visibility,
      price: form.price || undefined,
      material: form.material || undefined,
      finish: form.finish || undefined,
      color: form.color || undefined,
      dimensions: form.dimensions || undefined,
      is_active: form.is_active,
      is_featured: form.is_featured,
    }

    if (isEdit.value) {
      await productsApi.adminUpdate(productId.value, payload)
      router.push('/admin/products')
    } else {
      const res = await productsApi.adminCreate(payload)
      // Navigate to edit page so user can add images
      router.push(`/admin/products/${res.data.id}/edit`)
    }
  } catch (err) {
    submitError.value = err.response?.data?.error?.message || 'Failed to save product'
  } finally {
    saving.value = false
  }
}

async function handleFileSelect(e) {
  const files = Array.from(e.target.files)
  await uploadFiles(files)
  e.target.value = ''
}

async function handleDrop(e) {
  isDragging.value = false
  const files = Array.from(e.dataTransfer.files).filter(f => f.type.startsWith('image/'))
  await uploadFiles(files)
}

async function uploadFiles(files) {
  if (!files.length) return
  uploading.value = true
  uploadProgress.value = 0
  try {
    const formData = new FormData()
    files.forEach(f => formData.append('images', f))
    await productsApi.uploadImages(productId.value, formData)
    await loadImages()
    uploadProgress.value = 100
  } catch (err) {
    alert('Upload failed: ' + (err.response?.data?.error?.message || err.message))
  } finally {
    setTimeout(() => { uploading.value = false; uploadProgress.value = 0 }, 800)
  }
}

async function removeImage(img) {
  if (!confirm('Remove this image?')) return
  try {
    await productsApi.deleteImage(productId.value, img.id)
    await loadImages()
  } catch (err) {
    alert('Failed to remove image')
  }
}

async function setPrimary(img) {
  try {
    await productsApi.setPrimaryImage(productId.value, img.id)
    await loadImages()
  } catch (err) {
    alert('Failed to set primary image')
  }
}

async function loadImages() {
  const res = await productsApi.adminGetById(productId.value)
  existingImages.value = res.data.images || []
}

onMounted(async () => {
  const [catsRes] = await Promise.all([categoriesApi.adminGetAll()])
  categories.value = catsRes.data || []

  if (isEdit.value) {
    try {
      const res = await productsApi.adminGetById(productId.value)
      const p = res.data
      Object.assign(form, {
        name: p.name || '', slug: p.slug || '',
        collection_id: p.collection_id || '',
        product_type: p.product_type || '',
        short_description: p.short_description || '',
        description: p.description || '',
        price_visibility: p.price_visibility || 'contact_for_price',
        price: p.price || '',
        material: p.material || '', finish: p.finish || '',
        color: p.color || '', dimensions: p.dimensions || '',
        is_active: p.is_active ?? true, is_featured: p.is_featured ?? false,
      })
      existingImages.value = p.images || []
    } catch (err) {
      submitError.value = 'Failed to load product'
    } finally {
      loadingProduct.value = false
    }
  }
})
</script>

<style scoped>
.form-layout {
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
  max-width: 800px;
}

.form-card {
  background: white;
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-light);
  padding: var(--space-6);
}

.form-card__title {
  font-family: var(--font-sans);
  font-size: var(--text-md);
  font-weight: 600;
  margin-bottom: var(--space-6);
  padding-bottom: var(--space-4);
  border-bottom: 1px solid var(--border-light);
}

.form-card__hint {
  font-size: var(--text-sm);
  color: var(--text-muted);
  margin-top: calc(0px - var(--space-4));
  margin-bottom: var(--space-5);
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-4);
}

.form-col--full {
  grid-column: 1 / -1;
}

.form-input--error {
  border-color: var(--color-error) !important;
}

/* Slug field */
.slug-field {
  display: flex;
  align-items: center;
  border: 1px solid var(--border-light);
  border-radius: var(--radius-md);
  overflow: hidden;
  background: white;
  transition: border-color var(--transition-fast);
}

.slug-field:focus-within {
  border-color: var(--color-brass);
  box-shadow: 0 0 0 3px rgba(176, 141, 87, 0.12);
}

.slug-field__prefix {
  padding: 0.75rem 0.75rem;
  background: var(--color-ivory-mid);
  font-size: var(--text-sm);
  color: var(--text-muted);
  white-space: nowrap;
  border-right: 1px solid var(--border-light);
}

.slug-field .form-input {
  border: none;
  border-radius: 0;
  box-shadow: none;
}

.slug-field .form-input:focus {
  outline: none;
  box-shadow: none;
}

/* Toggle */
.toggle {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  cursor: pointer;
  user-select: none;
}

.toggle input[type="checkbox"] {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle__track {
  width: 44px;
  height: 24px;
  background: var(--border-mid);
  border-radius: var(--radius-full);
  position: relative;
  transition: background var(--transition-base);
  flex-shrink: 0;
}

.toggle input:checked + .toggle__track {
  background: var(--color-charcoal);
}

.toggle__thumb {
  position: absolute;
  top: 3px;
  left: 3px;
  width: 18px;
  height: 18px;
  background: white;
  border-radius: var(--radius-full);
  transition: transform var(--transition-base);
  box-shadow: 0 1px 3px rgba(0,0,0,0.2);
}

.toggle input:checked + .toggle__track .toggle__thumb {
  transform: translateX(20px);
}

.toggle__label {
  font-size: var(--text-sm);
  color: var(--text-secondary);
}

/* Images */
.images-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: var(--space-3);
  margin-bottom: var(--space-5);
}

.image-item {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.image-item__preview {
  position: relative;
  aspect-ratio: 1;
  overflow: hidden;
  border-radius: var(--radius-md);
  border: 2px solid var(--border-light);
}

.image-item__remove {
  position: absolute;
  top: 4px;
  right: 4px;
  width: 20px;
  height: 20px;
  background: rgba(26,26,26,0.8);
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  transition: background var(--transition-fast);
}

.image-item__remove:hover {
  background: var(--color-error);
}

.image-item__primary-badge {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(26,26,26,0.7);
  color: white;
  font-size: 9px;
  text-align: center;
  padding: 2px;
  letter-spacing: 0.05em;
}

.image-item__set-primary {
  font-size: var(--text-xs);
  color: var(--color-brass);
  text-align: center;
  cursor: pointer;
  text-decoration: underline;
}

/* Upload area */
.upload-area {
  border: 2px dashed var(--border-mid);
  border-radius: var(--radius-lg);
  padding: var(--space-10);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-2);
  cursor: pointer;
  transition: all var(--transition-base);
  text-align: center;
}

.upload-area:hover,
.upload-area--drag {
  border-color: var(--color-brass);
  background: rgba(176, 141, 87, 0.04);
}

.upload-area__text {
  font-size: var(--text-sm);
  font-weight: 500;
  color: var(--text-secondary);
}

.upload-area__hint {
  font-size: var(--text-xs);
  color: var(--text-muted);
}

/* Upload progress */
.upload-progress {
  margin-top: var(--space-4);
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.upload-progress__bar {
  flex: 1;
  height: 4px;
  background: var(--border-light);
  border-radius: var(--radius-full);
  overflow: hidden;
}

.upload-progress__fill {
  height: 100%;
  background: var(--color-brass);
  transition: width 0.3s ease;
}

.upload-progress__text {
  font-size: var(--text-xs);
  color: var(--text-muted);
  white-space: nowrap;
}

/* Submit */
.form-actions {
  display: flex;
  gap: var(--space-3);
  justify-content: flex-end;
  max-width: 800px;
  margin-top: var(--space-6);
  padding-top: var(--space-6);
  border-top: 1px solid var(--border-light);
}

.submit-error {
  max-width: 800px;
  margin-top: var(--space-4);
  padding: var(--space-4);
  background: rgba(155,48,48,0.08);
  border: 1px solid rgba(155,48,48,0.25);
  border-radius: var(--radius-md);
  font-size: var(--text-sm);
  color: var(--color-error);
}

.admin-loading-state {
  background: white;
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-light);
  padding: var(--space-8);
}

.skeleton-row {
  background: var(--color-ivory-dark);
  border-radius: var(--radius-md);
  animation: shimmer 1.5s ease-in-out infinite;
}

@keyframes shimmer {
  0%, 100% { opacity: 0.5; }
  50% { opacity: 1; }
}

@media (max-width: 600px) {
  .form-grid { grid-template-columns: 1fr; }
}
</style>
