<template>
  <div class="admin-account" ref="menuRef">
    <button class="admin-account__trigger" type="button" @click="toggleMenu">
      <img v-if="avatarUrl" :src="avatarUrl" alt="Admin" @error="avatarUrl = ''" />
      <span v-else class="admin-account__initials">{{ userInitials }}</span>
    </button>

    <Transition name="account-dropdown">
      <div v-if="menuOpen" class="admin-account__dropdown">
        <div class="admin-account__profile">
          <div class="admin-account__profile-avatar">
            <img v-if="avatarUrl" :src="avatarUrl" alt="Admin" @error="avatarUrl = ''" />
            <span v-else class="admin-account__initials admin-account__initials--large">{{ userInitials }}</span>
          </div>
          <div class="admin-account__profile-meta">
            <p class="admin-account__name">{{ fullName }}</p>
            <p class="admin-account__email">{{ userEmail }}</p>
          </div>
        </div>

        <div class="admin-account__divider"></div>

        <button class="admin-account__item" type="button" @click="openProfile">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
            <circle cx="12" cy="7" r="4" />
          </svg>
          Edit Profile
        </button>
        <button class="admin-account__item admin-account__item--logout" type="button" @click="handleLogout">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
            <polyline points="16 17 21 12 16 7" />
            <line x1="21" y1="12" x2="9" y2="12" />
          </svg>
          Logout
        </button>
      </div>
    </Transition>

    <Transition name="profile-panel">
      <div v-if="showProfile" class="profile-panel__backdrop" @click.self="closeProfile">
        <div class="profile-panel">
          <div class="profile-panel__header">
            <div>
              <h2 class="profile-panel__title">Edit Profile</h2>
              <p class="profile-panel__subtitle">Perubahan nama dan avatar akan tampil di seluruh dashboard admin.</p>
            </div>
            <button class="profile-panel__close" type="button" @click="closeProfile">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4">
                <line x1="18" y1="6" x2="6" y2="18" />
                <line x1="6" y1="6" x2="18" y2="18" />
              </svg>
            </button>
          </div>

          <div class="profile-panel__body">
            <div class="profile-panel__avatar-block">
              <div class="profile-panel__avatar">
                <img v-if="form.avatarPreview" :src="form.avatarPreview" alt="Preview" />
                <span v-else class="admin-account__initials admin-account__initials--xlarge">{{ formInitials }}</span>
              </div>

              <label class="profile-panel__upload">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z" />
                  <circle cx="12" cy="13" r="4" />
                </svg>
                Ganti Foto
                <input type="file" accept="image/*" hidden @change="onAvatarChange" />
              </label>
              <p class="profile-panel__hint">Format JPG atau PNG, maksimum 2MB.</p>
            </div>

            <div class="profile-panel__form">
              <div class="profile-panel__grid">
                <div class="profile-panel__field">
                  <label>Nama Depan</label>
                  <input v-model="form.firstName" type="text" placeholder="Masukkan nama depan" />
                </div>
                <div class="profile-panel__field">
                  <label>Nama Belakang</label>
                  <input v-model="form.lastName" type="text" placeholder="Masukkan nama belakang" />
                </div>
                <div class="profile-panel__field profile-panel__field--full">
                  <label>Username</label>
                  <input v-model="form.username" type="text" placeholder="Masukkan username" />
                </div>
                <div class="profile-panel__field profile-panel__field--full">
                  <label>Email</label>
                  <input v-model="form.email" type="email" placeholder="Masukkan email" />
                </div>
              </div>

              <div class="profile-panel__actions">
                <button class="profile-panel__btn profile-panel__btn--ghost" type="button" @click="closeProfile">Batalkan</button>
                <button class="profile-panel__btn profile-panel__btn--primary" type="button" @click="saveProfile">
                  {{ justSaved ? 'Tersimpan' : 'Simpan Perubahan' }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const menuRef = ref(null)
const menuOpen = ref(false)
const showProfile = ref(false)
const justSaved = ref(false)
const avatarUrl = ref('')
const user = ref({})
const form = ref({
  firstName: '',
  lastName: '',
  username: '',
  email: '',
  avatarPreview: '',
})

const syncUser = () => {
  try {
    user.value = JSON.parse(localStorage.getItem('user') || '{}')
  } catch {
    user.value = {}
  }
  avatarUrl.value = localStorage.getItem('admin_avatar') || ''
}

const fullName = computed(() => {
  const firstName = user.value.first_name || ''
  const lastName = user.value.last_name || ''
  return `${firstName} ${lastName}`.trim() || user.value.username || 'Admin'
})

const userEmail = computed(() =>
  user.value.email || (user.value.username ? `${user.value.username}@sisi.com` : 'admin@sisi.com')
)

const userInitials = computed(() => {
  const firstName = user.value.first_name?.[0] || ''
  const lastName = user.value.last_name?.[0] || ''
  return (firstName + lastName).toUpperCase() || 'A'
})

const formInitials = computed(() => {
  const firstName = form.value.firstName?.[0] || ''
  const lastName = form.value.lastName?.[0] || ''
  return (firstName + lastName).toUpperCase() || 'A'
})

const toggleMenu = () => {
  menuOpen.value = !menuOpen.value
}

const closeProfile = () => {
  showProfile.value = false
}

const onClickOutside = (event) => {
  if (menuRef.value && !menuRef.value.contains(event.target)) {
    menuOpen.value = false
  }
}

const openProfile = () => {
  menuOpen.value = false
  form.value = {
    firstName: user.value.first_name || '',
    lastName: user.value.last_name || '',
    username: user.value.username || '',
    email: user.value.email || (user.value.username ? `${user.value.username}@sisi.com` : ''),
    avatarPreview: avatarUrl.value,
  }
  showProfile.value = true
}

const onAvatarChange = (event) => {
  const file = event.target.files?.[0]
  if (!file) return

  const reader = new FileReader()
  reader.onload = (loadEvent) => {
    form.value.avatarPreview = loadEvent.target?.result || ''
  }
  reader.readAsDataURL(file)
}

const saveProfile = () => {
  const updatedUser = {
    first_name: (form.value.firstName || '').trim(),
    last_name: (form.value.lastName || '').trim(),
    username: (form.value.username || '').trim(),
    email: (form.value.email || '').trim(),
  }

  user.value = updatedUser
  localStorage.setItem('user', JSON.stringify(updatedUser))

  if (form.value.avatarPreview) {
    avatarUrl.value = form.value.avatarPreview
    localStorage.setItem('admin_avatar', form.value.avatarPreview)
  }

  justSaved.value = true
  window.dispatchEvent(new Event('admin-profile-updated'))

  setTimeout(() => {
    justSaved.value = false
    showProfile.value = false
  }, 1200)
}

const handleLogout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('role')
  localStorage.removeItem('user')
  localStorage.removeItem('admin_avatar')
  router.push('/login')
}

onMounted(() => {
  syncUser()
  document.addEventListener('click', onClickOutside)
  window.addEventListener('storage', syncUser)
  window.addEventListener('admin-profile-updated', syncUser)
})

onUnmounted(() => {
  document.removeEventListener('click', onClickOutside)
  window.removeEventListener('storage', syncUser)
  window.removeEventListener('admin-profile-updated', syncUser)
})
</script>

<style scoped>
.admin-account {
  position: relative;
}

.admin-account__trigger {
  width: 48px;
  height: 48px;
  border: none;
  border-radius: 50%;
  background: #1b7a6e;
  color: #fff;
  cursor: pointer;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 10px 24px rgba(27, 122, 110, 0.18);
}

.admin-account__trigger img,
.admin-account__profile-avatar img,
.profile-panel__avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.admin-account__initials {
  font-family: 'Montserrat', sans-serif;
  font-size: 16px;
  font-weight: 700;
  line-height: 1;
}

.admin-account__initials--large {
  font-size: 20px;
}

.admin-account__initials--xlarge {
  font-size: 34px;
}

.admin-account__dropdown {
  position: absolute;
  top: calc(100% + 12px);
  right: 0;
  width: 272px;
  background: #fff;
  border: 1px solid #ececec;
  border-radius: 20px;
  box-shadow: 0 24px 40px rgba(15, 23, 42, 0.14);
  overflow: hidden;
  z-index: 40;
}

.admin-account__profile {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 18px 20px;
}

.admin-account__profile-avatar {
  width: 54px;
  height: 54px;
  border-radius: 50%;
  overflow: hidden;
  background: #1b7a6e;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.admin-account__name {
  margin: 0;
  font-size: 14px;
  font-weight: 700;
  color: #1f2937;
}

.admin-account__email {
  margin: 4px 0 0;
  font-size: 12px;
  color: #94a3b8;
}

.admin-account__divider {
  height: 1px;
  background: #ececec;
}

.admin-account__item {
  width: 100%;
  border: none;
  background: transparent;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 20px;
  font-family: 'Montserrat', sans-serif;
  font-size: 14px;
  color: #374151;
  cursor: pointer;
  transition: background 0.2s ease, color 0.2s ease;
}

.admin-account__item:hover {
  background: #f8fafc;
  color: #1b7a6e;
}

.admin-account__item--logout {
  color: #ef4444;
}

.admin-account__item--logout:hover {
  background: #fef2f2;
  color: #dc2626;
}

.profile-panel__backdrop {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.18);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  z-index: 80;
}

.profile-panel {
  width: min(880px, 100%);
  background: #fff;
  border-radius: 28px;
  box-shadow: 0 30px 60px rgba(15, 23, 42, 0.16);
  overflow: hidden;
}

.profile-panel__header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  padding: 28px 30px 18px;
  border-bottom: 1px solid #f1f5f9;
}

.profile-panel__title {
  margin: 0;
  font-size: 24px;
  font-weight: 700;
  color: #0f172a;
}

.profile-panel__subtitle {
  margin: 8px 0 0;
  font-size: 13px;
  color: #64748b;
}

.profile-panel__close {
  width: 38px;
  height: 38px;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  background: #fff;
  color: #334155;
  cursor: pointer;
}

.profile-panel__body {
  display: grid;
  grid-template-columns: 220px minmax(0, 1fr);
  gap: 28px;
  padding: 28px 30px 30px;
}

.profile-panel__avatar-block {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.profile-panel__avatar {
  width: 146px;
  height: 146px;
  border-radius: 50%;
  overflow: hidden;
  background: #1b7a6e;
  display: flex;
  align-items: center;
  justify-content: center;
}

.profile-panel__upload {
  margin-top: 18px;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  border-radius: 999px;
  padding: 10px 16px;
  background: #1b7a6e;
  color: #fff;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
}

.profile-panel__hint {
  margin: 10px 0 0;
  font-size: 12px;
  color: #94a3b8;
}

.profile-panel__grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18px;
}

.profile-panel__field {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.profile-panel__field--full {
  grid-column: 1 / -1;
}

.profile-panel__field label {
  font-size: 13px;
  font-weight: 600;
  color: #334155;
}

.profile-panel__field input {
  width: 100%;
  border: 1px solid #dbe3ea;
  border-radius: 16px;
  padding: 14px 16px;
  font-family: 'Montserrat', sans-serif;
  font-size: 14px;
  color: #111827;
  background: #fff;
  outline: none;
}

.profile-panel__field input:focus {
  border-color: #1b7a6e;
  box-shadow: 0 0 0 4px rgba(27, 122, 110, 0.12);
}

.profile-panel__actions {
  margin-top: 28px;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.profile-panel__btn {
  min-width: 148px;
  border-radius: 999px;
  padding: 12px 18px;
  font-family: 'Montserrat', sans-serif;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
}

.profile-panel__btn--ghost {
  border: 1px solid #dbe3ea;
  background: #fff;
  color: #475569;
}

.profile-panel__btn--primary {
  border: none;
  background: #1b7a6e;
  color: #fff;
}

.account-dropdown-enter-active,
.account-dropdown-leave-active,
.profile-panel-enter-active,
.profile-panel-leave-active {
  transition: all 0.22s ease;
}

.account-dropdown-enter-from,
.account-dropdown-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

.profile-panel-enter-from,
.profile-panel-leave-to {
  opacity: 0;
}

@media (max-width: 860px) {
  .profile-panel__body {
    grid-template-columns: 1fr;
  }

  .profile-panel__grid {
    grid-template-columns: 1fr;
  }

  .profile-panel__field--full {
    grid-column: auto;
  }
}
</style>
