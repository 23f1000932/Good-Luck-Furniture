<template>
  <div class="settings-view">
    <div class="settings-card">
      <h2 class="settings-card__title">Change Password</h2>
      <form @submit.prevent="changePassword" novalidate id="change-password-form" style="max-width: 400px;">
        <div class="form-group" style="margin-bottom: var(--space-4);">
          <label for="current-password" class="form-label">Current Password</label>
          <input id="current-password" v-model="pwForm.current" type="password" class="form-input" required autocomplete="current-password" />
        </div>
        <div class="form-group" style="margin-bottom: var(--space-4);">
          <label for="new-password" class="form-label">New Password</label>
          <input id="new-password" v-model="pwForm.new_password" type="password" class="form-input" required autocomplete="new-password" />
        </div>
        <div class="form-group" style="margin-bottom: var(--space-6);">
          <label for="confirm-password" class="form-label">Confirm New Password</label>
          <input id="confirm-password" v-model="pwForm.confirm" type="password" class="form-input" required autocomplete="new-password" />
        </div>
        <div v-if="pwError" class="settings-error" role="alert">{{ pwError }}</div>
        <div v-if="pwSuccess" class="settings-success" role="status">Password updated successfully.</div>
        <button type="submit" class="btn btn-primary" :disabled="pwSaving" id="save-password-btn">
          {{ pwSaving ? 'Saving…' : 'Update Password' }}
        </button>
      </form>
    </div>

    <div class="settings-card">
      <h2 class="settings-card__title">Account Info</h2>
      <div class="settings-info">
        <div class="settings-info__row">
          <span class="settings-info__label">Email</span>
          <span class="settings-info__value">{{ authStore.user?.email }}</span>
        </div>
        <div class="settings-info__row">
          <span class="settings-info__label">Name</span>
          <span class="settings-info__value">{{ authStore.user?.name || 'Admin' }}</span>
        </div>
        <div class="settings-info__row">
          <span class="settings-info__label">Role</span>
          <span class="settings-info__value">Administrator</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'

const authStore = useAuthStore()
const pwForm = reactive({ current: '', new_password: '', confirm: '' })
const pwSaving = ref(false)
const pwError = ref('')
const pwSuccess = ref(false)

async function changePassword() {
  pwError.value = ''
  pwSuccess.value = false
  if (!pwForm.current || !pwForm.new_password || !pwForm.confirm) {
    pwError.value = 'All fields are required'
    return
  }
  if (pwForm.new_password !== pwForm.confirm) {
    pwError.value = 'New passwords do not match'
    return
  }
  if (pwForm.new_password.length < 8) {
    pwError.value = 'New password must be at least 8 characters'
    return
  }
  pwSaving.value = true
  try {
    await api.put('/auth/change-password', { current_password: pwForm.current, new_password: pwForm.new_password })
    pwSuccess.value = true
    Object.assign(pwForm, { current: '', new_password: '', confirm: '' })
  } catch (err) {
    pwError.value = err.response?.data?.error?.message || 'Failed to update password'
  } finally {
    pwSaving.value = false
  }
}
</script>

<style scoped>
.settings-view { max-width: 600px; display: flex; flex-direction: column; gap: var(--space-6); }
.settings-card { background: white; border-radius: var(--radius-lg); border: 1px solid var(--border-light); padding: var(--space-6); }
.settings-card__title { font-size: var(--text-md); font-weight: 600; margin-bottom: var(--space-6); padding-bottom: var(--space-4); border-bottom: 1px solid var(--border-light); }
.settings-error { padding: var(--space-3); background: rgba(155,48,48,0.08); border: 1px solid rgba(155,48,48,0.25); border-radius: var(--radius-md); font-size: var(--text-sm); color: var(--color-error); margin-bottom: var(--space-4); }
.settings-success { padding: var(--space-3); background: rgba(45,106,79,0.08); border: 1px solid rgba(45,106,79,0.25); border-radius: var(--radius-md); font-size: var(--text-sm); color: var(--color-success); margin-bottom: var(--space-4); }
.settings-info { display: flex; flex-direction: column; gap: var(--space-4); }
.settings-info__row { display: flex; gap: var(--space-6); padding-bottom: var(--space-4); border-bottom: 1px solid var(--border-light); font-size: var(--text-sm); }
.settings-info__row:last-child { border-bottom: none; }
.settings-info__label { color: var(--text-muted); min-width: 80px; }
.settings-info__value { color: var(--text-primary); font-weight: 500; }
</style>
