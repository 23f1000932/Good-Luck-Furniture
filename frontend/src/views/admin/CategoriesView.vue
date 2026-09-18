<template>
  <div class="categories-view">
    <div class="admin-toolbar">
      <h2 style="font-size: var(--text-lg); font-weight: 600;">Manage Collections</h2>
      <button class="btn btn-primary" @click="openAdd" id="add-category-btn">+ Add Collection</button>
    </div>

    <div class="admin-table-wrap">
      <div v-if="loading" class="admin-loading-state">
        <div v-for="n in 4" :key="n" class="skeleton-row" style="height: 56px; margin-bottom: 8px;"></div>
      </div>

      <table v-else-if="categories.length > 0" class="admin-table" aria-label="Categories list">
        <thead>
          <tr>
            <th scope="col">Name</th>
            <th scope="col">Slug</th>
            <th scope="col">Products</th>
            <th scope="col">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="cat in categories" :key="cat.id" class="admin-table__row">
            <td style="padding: var(--space-3) var(--space-4); font-weight: 500;">{{ cat.name }}</td>
            <td style="padding: var(--space-3) var(--space-4);" class="admin-table__cell">{{ cat.slug }}</td>
            <td style="padding: var(--space-3) var(--space-4);" class="admin-table__cell">{{ cat.product_count || 0 }}</td>
            <td class="admin-table__actions" style="padding: var(--space-3) var(--space-4);">
              <button class="admin-action-btn" @click="openEdit(cat)" :aria-label="`Edit ${cat.name}`">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
              </button>
              <button class="admin-action-btn admin-action-btn--danger" @click="confirmDelete(cat)" :aria-label="`Delete ${cat.name}`" :id="`delete-cat-${cat.id}`">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a1 1 0 011-1h4a1 1 0 011 1v2"/></svg>
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-else class="admin-empty-state">No categories found.</div>
    </div>

    <!-- Add / Edit Modal -->
    <Teleport to="body">
      <div v-if="modalOpen" class="modal-backdrop" @click.self="modalOpen = false" role="dialog" aria-modal="true" :aria-label="editTarget ? 'Edit collection' : 'Add collection'">
        <div class="modal">
          <h3 class="modal__title">{{ editTarget ? 'Edit Collection' : 'Add Collection' }}</h3>
          <form @submit.prevent="saveCategory" novalidate>
            <div class="form-group" style="margin-bottom: var(--space-4);">
              <label for="cat-name" class="form-label">Name *</label>
              <input id="cat-name" v-model="catForm.name" type="text" class="form-input" placeholder="e.g. Bedroom" required />
            </div>
            <div class="form-group" style="margin-bottom: var(--space-4);">
              <label for="cat-slug" class="form-label">Slug</label>
              <input id="cat-slug" v-model="catForm.slug" type="text" class="form-input" placeholder="auto-generated" />
            </div>
            <div class="form-group" style="margin-bottom: var(--space-6);">
              <label for="cat-description" class="form-label">Description</label>
              <textarea id="cat-description" v-model="catForm.description" class="form-textarea" style="min-height: 80px;" placeholder="Optional description"></textarea>
            </div>
            <div v-if="catError" class="submit-error" style="margin-bottom: var(--space-4);" role="alert">{{ catError }}</div>
            <div class="modal__actions">
              <button type="button" class="btn btn-outline" @click="modalOpen = false">Cancel</button>
              <button type="submit" class="btn btn-primary" :disabled="catSaving" id="save-category-btn">
                {{ catSaving ? 'Saving…' : 'Save' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </Teleport>

    <!-- Delete Confirm -->
    <Teleport to="body">
      <div v-if="deleteTarget" class="modal-backdrop" @click.self="deleteTarget = null" role="dialog" aria-modal="true">
        <div class="modal">
          <h3 class="modal__title">Delete "{{ deleteTarget?.name }}"?</h3>
          <p class="modal__body">This collection will be removed. Products in it will lose their collection assignment.</p>
          <div class="modal__actions">
            <button class="btn btn-outline" @click="deleteTarget = null">Cancel</button>
            <button class="btn btn-danger" @click="executeDelete" :disabled="deleting">{{ deleting ? 'Deleting…' : 'Delete' }}</button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, reactive, watch, onMounted } from 'vue'
import { categoriesApi } from '@/services/categories'

const categories = ref([])
const loading = ref(true)
const modalOpen = ref(false)
const editTarget = ref(null)
const deleteTarget = ref(null)
const catSaving = ref(false)
const deleting = ref(false)
const catError = ref('')

const catForm = reactive({ name: '', slug: '', description: '' })

watch(() => catForm.name, (name) => {
  if (!editTarget.value) {
    catForm.slug = name.toLowerCase().replace(/[^\w\s-]/g, '').replace(/[\s_]+/g, '-').replace(/-+/g, '-').trim()
  }
})

function openAdd() {
  editTarget.value = null
  Object.assign(catForm, { name: '', slug: '', description: '' })
  catError.value = ''
  modalOpen.value = true
}

function openEdit(cat) {
  editTarget.value = cat
  Object.assign(catForm, { name: cat.name, slug: cat.slug, description: cat.description || '' })
  catError.value = ''
  modalOpen.value = true
}

function confirmDelete(cat) { deleteTarget.value = cat }

async function load() {
  loading.value = true
  try {
    const res = await categoriesApi.adminGetAll()
    categories.value = res.data || []
  } catch(e) { console.error(e) }
  finally { loading.value = false }
}

async function saveCategory() {
  catSaving.value = true
  catError.value = ''
  try {
    if (editTarget.value) {
      await categoriesApi.adminUpdate(editTarget.value.id, catForm)
    } else {
      await categoriesApi.adminCreate(catForm)
    }
    modalOpen.value = false
    await load()
  } catch (err) {
    catError.value = err.response?.data?.error?.message || 'Failed to save'
  } finally {
    catSaving.value = false
  }
}

async function executeDelete() {
  deleting.value = true
  try {
    await categoriesApi.adminDelete(deleteTarget.value.id)
    deleteTarget.value = null
    await load()
  } catch (err) {
    alert('Failed to delete category')
  } finally {
    deleting.value = false
  }
}

onMounted(load)
</script>

<style scoped>
.categories-view { max-width: 700px; }
.admin-toolbar { display: flex; align-items: center; justify-content: space-between; margin-bottom: var(--space-5); }
.admin-table-wrap { background: white; border-radius: var(--radius-lg); border: 1px solid var(--border-light); overflow: hidden; }
.admin-table { width: 100%; border-collapse: collapse; font-size: var(--text-sm); }
.admin-table thead { background: var(--color-ivory-mid); border-bottom: 1px solid var(--border-light); }
.admin-table th { padding: var(--space-3) var(--space-4); text-align: left; font-size: var(--text-xs); font-weight: 600; letter-spacing: var(--tracking-wide); text-transform: uppercase; color: var(--text-muted); }
.admin-table__row { border-bottom: 1px solid var(--border-light); transition: background var(--transition-fast); }
.admin-table__row:last-child { border-bottom: none; }
.admin-table__row:hover { background: var(--color-ivory-mid); }
.admin-table__cell { color: var(--text-secondary); }
.admin-table__actions { display: flex; gap: var(--space-1); }
.admin-action-btn { width: 30px; height: 30px; display: inline-flex; align-items: center; justify-content: center; border-radius: var(--radius-md); color: var(--text-muted); transition: all var(--transition-fast); }
.admin-action-btn:hover { background: var(--color-ivory-mid); color: var(--text-primary); }
.admin-action-btn--danger:hover { background: rgba(155,48,48,0.1); color: var(--color-error); }
.admin-empty-state { padding: var(--space-12); text-align: center; color: var(--text-muted); }
.admin-loading-state { padding: var(--space-4); }
.skeleton-row { background: var(--color-ivory-dark); border-radius: var(--radius-md); animation: shimmer 1.5s ease-in-out infinite; }
@keyframes shimmer { 0%, 100% { opacity: 0.5; } 50% { opacity: 1; } }
.modal-backdrop { position: fixed; inset: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: var(--z-modal); padding: var(--space-6); }
.modal { background: white; border-radius: var(--radius-lg); padding: var(--space-8); max-width: 420px; width: 100%; box-shadow: var(--shadow-lg); }
.modal__title { font-family: var(--font-display); font-size: var(--text-xl); font-weight: 400; margin-bottom: var(--space-6); }
.modal__body { color: var(--text-secondary); font-size: var(--text-sm); line-height: var(--leading-relaxed); margin-bottom: var(--space-6); }
.modal__actions { display: flex; gap: var(--space-3); justify-content: flex-end; }
.btn-danger { background: var(--color-error); color: white; border-color: var(--color-error); padding: 0.875rem 2rem; font-size: var(--text-sm); font-weight: 500; letter-spacing: var(--tracking-wide); text-transform: uppercase; border-radius: var(--radius-sm); border: 1px solid; transition: all var(--transition-base); }
.submit-error { padding: var(--space-3); background: rgba(155,48,48,0.08); border: 1px solid rgba(155,48,48,0.25); border-radius: var(--radius-md); font-size: var(--text-sm); color: var(--color-error); }
</style>
