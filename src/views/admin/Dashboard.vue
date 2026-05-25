<template>

    <div class="admin-wrapper">

  <!-- CONTENT -->
  <main class="admin-content">

    <!-- Top Bar -->
    <div class="topbar">
      <div class="topbar__greeting">
        <h1 class="topbar__hello">Hello, <span class="topbar__name">{{ userName }}</span></h1>
        <p class="topbar__sub">Selamat Datang di Dashboard Admin <span class="topbar__brand">SISI Interior</span></p>
      </div>
      <div class="topbar__right">
        <button class="topbar__search">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
          </svg>
        </button>

        <AdminAccountMenu />
      </div>
    </div>

    <!-- ══════════════════════════════════════════
         PROFILE EDIT PANEL (inline, not modal)
    ══════════════════════════════════════════ -->
    <Transition name="panel-slide">
      <div class="profile-panel" v-if="showProfile">

        <!-- Panel Header -->
        <div class="panel-header">
          <div class="panel-header__left">
            <div class="panel-header__icon">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>
              </svg>
            </div>
            <div>
              <h2 class="panel-header__title">Edit Profile</h2>
              <p class="panel-header__sub">Perubahan nama akan langsung muncul di sapaan dashboard</p>
            </div>
          </div>
          <button class="panel-close" @click="closeProfile">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>

        <!-- Panel Body -->
        <div class="panel-body">

          <!-- Kiri: Avatar Upload -->
          <div class="panel-left">
            <div class="avatar-upload-wrap">
              <div class="avatar-upload">
                <img v-if="form.avatarPreview" :src="form.avatarPreview" alt="Preview" />
                <span v-else class="avatar-initials avatar-initials--xl">{{ formInitials }}</span>
              </div>
              <label class="avatar-upload__btn" title="Ganti foto">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                  <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/>
                  <circle cx="12" cy="13" r="4"/>
                </svg>
                Ganti Foto
                <input type="file" accept="image/*" style="display:none" @change="onAvatarChange" />
              </label>
              <p class="avatar-hint">Format JPG, PNG. Maks 2MB</p>
              <div class="avatar-badge">Administrator</div>
            </div>
          </div>

          <!-- Kanan: Form Fields -->
          <div class="panel-right">
            <div class="form-grid">

              <!-- Nama Depan -->
              <div class="form-group">
                <label class="form-label">
                  <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                  Nama Depan
                </label>
                <input
                  class="form-input"
                  type="text"
                  v-model="form.firstName"
                  placeholder="Masukkan nama depan"
                  @input="onNameInput"
                />
                <span class="form-hint">Akan tampil di: <b>Hello, {{ previewName }}</b></span>
              </div>

              <!-- Nama Belakang -->
              <div class="form-group">
                <label class="form-label">
                  <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                  Nama Belakang
                </label>
                <input
                  class="form-input"
                  type="text"
                  v-model="form.lastName"
                  placeholder="Masukkan nama belakang"
                />
              </div>

              <!-- Username -->
              <div class="form-group form-group--full">
                <label class="form-label">
                  <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="4"/><path d="M16 8v5a3 3 0 0 0 6 0v-1a10 10 0 1 0-3.92 7.94"/></svg>
                  Username
                </label>
                <div class="input-prefix-wrap">
                  <span class="input-prefix">@</span>
                  <input
                    class="form-input form-input--prefix"
                    type="text"
                    v-model="form.username"
                    placeholder="username"
                  />
                </div>
              </div>

              <!-- Email -->
              <div class="form-group form-group--full">
                <label class="form-label">
                  <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
                  Email
                </label>
                <input
                  class="form-input"
                  type="email"
                  v-model="form.email"
                  placeholder="admin@sisi.com"
                />
              </div>

            </div>

            <!-- Action Buttons -->
            <div class="panel-actions">
              <button class="btn-cancel" @click="cancelEdit">Batalkan</button>
              <button class="btn-save" @click="persistAdminProfile" :disabled="isSavingProfile" :class="{ 'btn-save--saved': justSaved }">
                <Transition name="btn-swap" mode="out-in">
                  <span v-if="justSaved" key="saved" class="btn-save__content">
                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
                    Tersimpan!
                  </span>
                  <span v-else-if="isSavingProfile" key="loading" class="btn-save__content">
                    <span class="btn-spinner"></span>
                    Menyimpan...
                  </span>
                  <span v-else key="save" class="btn-save__content">
                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>
                    Simpan Perubahan
                  </span>
                </Transition>
              </button>
            </div>

          </div>
        </div>
      </div>
    </Transition>

    <!-- Stat Cards -->
    <div class="stat-cards">
      <div class="stat-card" v-for="(card, i) in statCards" :key="i" :style="{ '--delay': i * 0.07 + 's' }">
        <div class="stat-card__icon-wrap">
          <span class="stat-card__icon" v-html="card.icon"></span>
        </div>
        <div class="stat-card__body">
          <template v-if="card.sub">
            <p class="stat-card__label bold">{{ card.label }}</p>
            <p class="stat-card__sub">{{ card.sub }}</p>
          </template>
          <template v-else>
            <p class="stat-card__number">{{ card.number }}</p>
            <p class="stat-card__label">{{ card.label }}</p>
          </template>
        </div>
      </div>
    </div>

    <!-- Analytics Section -->
    <div class="section-header">
      <h2 class="section-title">Ringkasan Analitik</h2>
      <a href="#" class="section-viewall" @click.prevent="goToAnalytics">
        View all
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"/></svg>
      </a>
    </div>

    <div class="chart-card">
      <div class="chart-card__header">
        <h3 class="chart-card__title">Grafik Tren Biaya Proyek</h3>
        <div class="select-wrap">
          <select v-model="chartPeriod" class="period-select">
            <option value="this_month">This Month</option>
            <option value="last_month">Last Month</option>
            <option value="this_year">This Year</option>
          </select>
          <svg class="select-arrow" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg>
        </div>
      </div>
      <div class="chart-wrap">
        <svg v-if="chartSvg.points.length" class="chart-svg" viewBox="0 0 760 270" xmlns="http://www.w3.org/2000/svg">
          <line
            v-for="line in chartSvg.gridLines"
            :key="`grid-${line.y}`"
            x1="50"
            :y1="line.y"
            x2="740"
            :y2="line.y"
            stroke="#E5E7EB"
            stroke-width="1"
            :stroke-dasharray="line.dashed ? '4,4' : null"
          />
          <text
            v-for="tick in chartSvg.yTicks"
            :key="`tick-${tick.y}`"
            x="44"
            :y="tick.y + 4"
            font-size="10"
            fill="#9CA3AF"
            text-anchor="end"
            font-family="Montserrat,sans-serif"
          >
            {{ tick.label }}
          </text>
          <path :d="chartSvg.areaPath" fill="url(#areaGradDashboard)" />
          <path
            :d="chartSvg.linePath"
            fill="none"
            stroke="#1B7A6E"
            stroke-width="2.5"
            stroke-linejoin="round"
            stroke-linecap="round"
          />
          <circle
            :cx="chartSvg.peakPoint.x"
            :cy="chartSvg.peakPoint.y"
            r="6"
            fill="#FFFFFF"
            stroke="#1B7A6E"
            stroke-width="2.5"
          />
          <line
            :x1="chartSvg.peakPoint.x"
            :y1="chartSvg.peakPoint.y + 14"
            :x2="chartSvg.peakPoint.x"
            y2="235"
            stroke="#EF4444"
            stroke-width="1.5"
            stroke-dasharray="5,4"
          />
          <rect
            :x="chartSvg.peakBubble.x"
            :y="chartSvg.peakBubble.y"
            :width="chartSvg.peakBubble.width"
            height="22"
            rx="6"
            fill="#1B7A6E"
          />
          <text
            :x="chartSvg.peakPoint.x"
            :y="chartSvg.peakBubble.y + 15"
            font-size="11"
            fill="#FFFFFF"
            text-anchor="middle"
            font-family="Montserrat,sans-serif"
            font-weight="700"
          >
            {{ chartSvg.peakBubble.label }}
          </text>
          <text
            v-for="point in chartSvg.points"
            :key="`label-${point.index}`"
            :x="point.x"
            :y="point.index === chartSvg.peakIndex ? 252 : 250"
            :font-size="point.index === chartSvg.peakIndex ? 11 : 10"
            :fill="point.index === chartSvg.peakIndex ? '#1B7A6E' : '#9CA3AF'"
            text-anchor="middle"
            font-family="Montserrat,sans-serif"
            :font-weight="point.index === chartSvg.peakIndex ? '700' : '400'"
          >
            {{ point.label }}
          </text>
          <defs>
            <linearGradient id="areaGradDashboard" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stop-color="#1B7A6E" stop-opacity="0.35"/>
              <stop offset="100%" stop-color="#1B7A6E" stop-opacity="0"/>
            </linearGradient>
          </defs>
        </svg>
        <div v-else class="chart-empty">Belum ada data estimasi untuk periode ini.</div>
      </div>
    </div>

    <!-- Recent Projects -->
    <div class="section-header mt">
      <h2 class="section-title">Data Proyek Terbaru</h2>
      <a href="#" class="section-viewall" @click="goToProjects">
        View all
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"/></svg>
      </a>
    </div>

    <div class="table-card">
      <table class="table">
        <thead>
          <tr>
            <th>No</th>
            <th>Jenis Proyek</th>
            <th>Jenis Pekerjaan</th>
            <th>Biaya</th>
            <th>Tanggal</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, i) in projects" :key="i">
            <td class="td-no">{{ i + 1 }}</td>
            <td class="td-client">
              <div class="client-row">
                <div class="avatar-table" :style="{ background: row.color }">{{ row.initials }}</div>
                <div>
                  <p class="client-name">{{ row.name }}</p>
                  <p class="client-project">{{ row.project }}</p>
                </div>
              </div>
            </td>
            <td>
              <span class="badge" :class="'badge--' + row.typeKey">{{ row.type }}</span>
            </td>
            <td class="td-biaya">{{ row.biaya }}</td>
            <td class="td-tanggal">{{ row.tanggal }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import AdminAccountMenu from '@/components/AdminAccountMenu.vue'

const router        = useRouter()
const API_BASE_URL  = import.meta.env.VITE_API_BASE_URL || 'https://rent-installation-utc-remedy.trycloudflare.com/api'
const menuOpen      = ref(false)
const showProfile   = ref(false)
const avatarMenuRef = ref(null)
const avatarUrl     = ref('')
const justSaved     = ref(false)
const isSavingProfile = ref(false)
const avatarFile = ref(null)


// ───────────────────────
// STATE
// ───────────────────────
const user = ref({})
const projects = ref([])
const chartPeriod = ref('this_month')
const chartData = ref({
  labels: [],
  values: [],
  peak: { index: 0, label: '', value: 0 },
})

const goToProjects = () => {
  router.push('/admin/proyek')
}

const goToAnalytics = () => {
  router.push('/admin/analitik')
}

const form = ref({
  firstName: '',
  lastName: '',
  username: '',
  email: '',
  avatarPreview: '',
})

const syncAdminSession = (adminUser, token) => {
  if (!adminUser) return

  user.value = { ...adminUser }
  localStorage.setItem('user', JSON.stringify(adminUser))
  localStorage.setItem('username', adminUser.username || '')

  if (token) {
    localStorage.setItem('token', token)
  }

  if (adminUser.avatar_url) {
    avatarUrl.value = adminUser.avatar_url
    localStorage.setItem('admin_avatar', adminUser.avatar_url)
  }
}

const fetchAdminProfile = async () => {
  try {
    const token = localStorage.getItem('token')
    if (!token) return

    const response = await fetch(`${API_BASE_URL}/admin/profile`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })

    const data = await response.json()
    if (!response.ok) {
      throw new Error(data.message || 'Gagal memuat profil admin.')
    }

    syncAdminSession({
      id: data.id,
      first_name: data.first_name || '',
      last_name: data.last_name || '',
      username: data.username || '',
      email: data.email || '',
      avatar_url: data.avatar_url || '',
      role: 'admin',
    })
  } catch (error) {
    console.error('Gagal memuat profil admin:', error)
  }
}

onMounted(() => {
  initUser()
  fetchAdminProfile()
  initDashboard()
  loadTrendData()

  const savedAvatar = localStorage.getItem('admin_avatar')
  if (savedAvatar) {
    avatarUrl.value = savedAvatar
  }
  document.addEventListener('click', onClickOutside)
  window.addEventListener('admin-profile-updated', initUser)
})

onUnmounted(() => {
  document.removeEventListener('click', onClickOutside)
  window.removeEventListener('admin-profile-updated', initUser)
})

const fullName = computed(() => {
  const fn = user.value.first_name || ''
  const ln = user.value.last_name  || ''
  return (fn + ' ' + ln).trim() || user.value.username || 'Admin'
})

const userEmail = computed(() =>
  user.value.email || (user.value.username ? user.value.username + '@sisi.com' : 'admin@sisi.com')
)

const userInitials = computed(() => {
  const fn = user.value.first_name?.[0] || ''
  const ln = user.value.last_name?.[0]  || ''
  return (fn + ln).toUpperCase() || 'A'
})

// Live preview for form
const previewName = computed(() =>
  form.value.firstName || form.value.username || 'Admin'
)

const formInitials = computed(() => {
  const fn = form.value.firstName?.[0] || ''
  const ln = form.value.lastName?.[0]  || ''
  return (fn + ln).toUpperCase() || 'A'
})

// ── Menu ──
const toggleMenu = () => { menuOpen.value = !menuOpen.value }

const onClickOutside = (e) => {
  if (avatarMenuRef.value && !avatarMenuRef.value.contains(e.target)) {
    menuOpen.value = false
  }
}

const openProfile = () => {
  menuOpen.value = false
  // Populate form with current user data
  form.value = {
    firstName:     user.value.first_name || '',
    lastName:      user.value.last_name  || '',
    username:      user.value.username   || '',
    email:         user.value.email      || (user.value.username ? user.value.username + '@sisi.com' : ''),
    avatarPreview: avatarUrl.value,
  }
  showProfile.value = true
}

const closeProfile = () => {
  showProfile.value = false
}

const cancelEdit = () => {
  avatarFile.value = null
  showProfile.value = false
}

const saveProfile = () => {
  localStorage.setItem('admin_avatar', avatarUrl.value)
  // Rebuild object fully — ensures Vue reactive ref triggers computed re-evaluation
  const updated = {
    first_name: (form.value.firstName || '').trim(),
    last_name:  (form.value.lastName  || '').trim(),
    username:   (form.value.username  || '').trim(),
    email:      (form.value.email     || '').trim(),
  }
  user.value = updated
  localStorage.setItem('user', JSON.stringify(updated))

  // Save avatar
  if (form.value.avatarPreview) {
    avatarUrl.value = form.value.avatarPreview
    localStorage.setItem('admin_avatar', form.value.avatarPreview)
  }

  justSaved.value = true
  setTimeout(() => {
    justSaved.value   = false
    showProfile.value = false
  }, 1400)
}

const persistAdminProfile = async () => {
  const firstName = (form.value.firstName || '').trim()
  const lastName = (form.value.lastName || '').trim()
  const username = (form.value.username || '').trim()
  const email = (form.value.email || '').trim()

  if (!username) {
    alert('Username admin wajib diisi.')
    return
  }

  isSavingProfile.value = true
  try {
    const token = localStorage.getItem('token')
    let response

    if (avatarFile.value) {
      const formData = new FormData()
      formData.append('first_name', firstName)
      formData.append('last_name', lastName)
      formData.append('username', username)
      formData.append('email', email)
      formData.append('avatar', avatarFile.value)

      response = await fetch(`${API_BASE_URL}/admin/profile`, {
        method: 'PUT',
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      })
    } else {
      response = await fetch(`${API_BASE_URL}/admin/profile`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          first_name: firstName,
          last_name: lastName,
          username,
          email,
        }),
      })
    }

    const data = await response.json()
    if (!response.ok) {
      throw new Error(data.message || 'Gagal menyimpan profil admin.')
    }

    syncAdminSession(data.user, data.token)

    if (data.user?.avatar_url) {
      form.value.avatarPreview = data.user.avatar_url
      avatarUrl.value = data.user.avatar_url
    }

    avatarFile.value = null
    justSaved.value = true
    window.dispatchEvent(new Event('admin-profile-updated'))
    setTimeout(() => {
      justSaved.value = false
      showProfile.value = false
    }, 1400)
  } catch (error) {
    alert(error.message || 'Gagal menyimpan profil admin.')
  } finally {
    isSavingProfile.value = false
  }
}

const onNameInput = () => {
  // reactive — previewName computed handles it
}

const onAvatarChange = (e) => {
  const file = e.target.files[0]
  if (!file) return
  avatarFile.value = file
  const reader = new FileReader()
  reader.onload = (ev) => {
    form.value.avatarPreview = ev.target.result
  }
  reader.readAsDataURL(file)
}

const handleLogout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('role')
  localStorage.removeItem('user')
  router.push('/login')
}


const statCards = ref([
  {
    number:'0',
    label:'Data proyek',
    icon:`<svg xmlns="http://www.w3.org/2000/svg"
    width="20" height="20"
    fill="none"
    stroke="currentColor"
    stroke-width="2"
    viewBox="0 0 24 24">
    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
    <polyline points="14 2 14 8 20 8"/>
    </svg>`
  },
  {
    number:'0',
    label:'Jumlah estimasi',
    icon:`<svg xmlns="http://www.w3.org/2000/svg"
    width="20"
    height="20"
    fill="none"
    stroke="currentColor"
    stroke-width="2"
    viewBox="0 0 24 24">
    <polygon points="23 7 16 12 23 17 23 7"/>
    <rect x="1" y="5" width="15" height="14" rx="2"/>
    </svg>`
  },
  {
    label: 'Model Aktif',
    sub: 'Last trained: -',
    icon:`<svg xmlns="http://www.w3.org/2000/svg"
    width="20"
    height="20"
    fill="none"
    stroke="currentColor"
    stroke-width="2"
    viewBox="0 0 24 24">
    <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
    <circle cx="9" cy="7" r="4"/>
    <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
    <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
    </svg>`
  },
  {
  label:'Total User Terdaftar',
  icon:`<svg xmlns="http://www.w3.org/2000/svg"
  width="20"
  height="20"
  fill="none"
  stroke="currentColor"
  stroke-width="2"
  viewBox="0 0 24 24">
  <circle cx="12" cy="8" r="4"/>
  <path d="M6 20v-1a6 6 0 0 1 12 0v1"/>
  </svg>`
},
])


// ───────────────────────
// INIT USER
// ───────────────────────
const initUser = () => {
  try {
    user.value = JSON.parse(localStorage.getItem('user') || '{}')
  } catch {
    user.value = {}
  }
}

// ───────────────────────
// FETCH DASHBOARD (SINGLE SOURCE OF TRUTH)
// ───────────────────────
const initDashboard = async () => {
  try {
    const token = localStorage.getItem('token')

    const response = await axios.get(
      'https://rent-installation-utc-remedy.trycloudflare.com/api/admin/dashboard',
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    )

    const data = response.data.data

    // ── STATS ──
    statCards.value[0].number = data.total_project ?? 0
    statCards.value[1].number = data.total_estimasi ?? 0
    statCards.value[2].sub =
    `${data.model_name || 'Model Estimasi'} • Last trained: ${data.last_trained ?? '-'}${data.model_status ? ` • ${data.model_status}` : ''}`
    statCards.value[3].number = data.total_user ?? 0

    if (!data.last_trained || data.last_trained === '-') {
      try {
        const mlResponse = await axios.get('http://127.0.0.1:5000/train/riwayat')
        const latestTraining = mlResponse.data?.data?.[0]

        if (latestTraining) {
          const modelName = latestTraining.nama_training || data.model_name || 'Model Estimasi'
          const modelStatus = latestTraining.status || data.model_status || ''
          const lastTrained = formatTanggalPanjang(latestTraining.tanggal_training)

          statCards.value[2].sub =
            `${modelName} • Last trained: ${lastTrained}${modelStatus ? ` • ${modelStatus}` : ''}`
        }
      } catch (mlError) {
        console.warn('Fallback riwayat training gagal diambil:', mlError)
      }
    }

    // ── CHART ──

    // ── RECENT PROJECTS ──
    projects.value = (data.latest_projects ?? []).map(item => ({
      initials: item.jenis_proyek
        ?.split(' ')
        .map(n => n[0])
        .join('')
        .toUpperCase()
        .slice(0, 2) || 'PR',

      name: item.jenis_proyek || '-',
      project: item.jenis_pekerjaan || '-',
      type: item.jenis_pekerjaan || '-',
      typeKey: getJobBadgeKey(item.jenis_pekerjaan),
      biaya: formatRupiah(item.harga_satuan),
      tanggal: formatTanggal(item.created_at ?? item.CreatedAt),
      color: '#1B7A6E'
    }))

  } catch (error) {
    console.error('Gagal fetch dashboard:', error)
  }
}

// ───────────────────────
// FORMATTERS
// ───────────────────────
const loadTrendData = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await fetch(`${API_BASE_URL}/admin/dashboard/trend?period=${chartPeriod.value}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })

    if (!response.ok) {
      throw new Error('Gagal mengambil data tren dashboard')
    }

    const result = await response.json()
    const data = result.data || {}

    chartData.value = {
      labels: Array.isArray(data.labels) ? data.labels : [],
      values: Array.isArray(data.values) ? data.values.map(Number) : [],
      peak: {
        index: Number(data.peak?.index ?? 0),
        label: data.peak?.label ?? '',
        value: Number(data.peak?.value ?? 0),
      },
    }
  } catch (error) {
    console.error('Gagal mengambil tren dashboard:', error)
    chartData.value = { labels: [], values: [], peak: { index: 0, label: '', value: 0 } }
  }
}

const formatRupiah = (angka) => {
  if (angka == null) return 'Rp 0'

  return new Intl.NumberFormat('id-ID', {
    style: 'currency',
    currency: 'IDR',
    minimumFractionDigits: 0
  }).format(angka)
}

const formatTanggal = (tanggal) => {
  if (!tanggal) return '-'
  return new Date(tanggal).toLocaleDateString('id-ID')
}

const formatTanggalPanjang = (tanggal) => {
  if (!tanggal) return '-'

  const date = new Date(tanggal)
  if (Number.isNaN(date.getTime())) return '-'

  return date.toLocaleDateString('id-ID', {
    day: '2-digit',
    month: 'long',
    year: 'numeric',
  })
}

const formatCompactCurrency = (value) => {
  const amount = Number(value || 0)
  if (amount >= 1000000000) return `${(amount / 1000000000).toFixed(1).replace('.0', '')}M`
  if (amount >= 1000000) return `${(amount / 1000000).toFixed(1).replace('.0', '')}Jt`
  if (amount >= 1000) return `${(amount / 1000).toFixed(0)}K`
  return `${amount}`
}

const getJobBadgeKey = (jenisPekerjaan) => {
  const value = (jenisPekerjaan || '').trim().toLowerCase()

  if (value === 'renovasi') return 'renovasi'
  if (value === 'custome furnitur' || value === 'custom furniture' || value === 'furniture') return 'custom-furnitur'
  if (value === 'new build' || value === 'build / fit out') return 'new-build'

  return 'custom'
}

const chartSvg = computed(() => {
  const labels = chartData.value.labels || []
  const values = (chartData.value.values || []).map((value) => Number(value || 0))
  const peakIndex = Number(chartData.value.peak?.index ?? 0)

  if (!labels.length || !values.length) {
    return {
      points: [],
      gridLines: [],
      yTicks: [],
      linePath: '',
      areaPath: '',
      peakIndex: 0,
      peakPoint: { x: 75, y: 235 },
      peakBubble: { x: 40, y: 8, width: 78, label: '0' },
    }
  }

  const left = 75
  const right = 740
  const top = 20
  const bottom = 235
  const maxValue = Math.max(...values, 0)
  const scaleMax = maxValue > 0 ? Math.ceil((maxValue * 1.05) / 1000000) * 1000000 : 1000000
  const usableHeight = bottom - top
  const stepX = labels.length > 1 ? (right - left) / (labels.length - 1) : 0

  const points = labels.map((label, index) => {
    const value = values[index] || 0
    const ratio = scaleMax > 0 ? value / scaleMax : 0
    const x = left + (stepX * index)
    const y = bottom - (ratio * usableHeight)
    return {
      index,
      label,
      value,
      x: Number(x.toFixed(2)),
      y: Number(y.toFixed(2)),
    }
  })

  const linePath = points.map((point, index) => `${index === 0 ? 'M' : 'L'}${point.x},${point.y}`).join(' ')
  const areaPath = `${linePath} L${right},${bottom} L${left},${bottom} Z`
  const gridLines = [20, 67, 114, 161, 208, 235].map((y, index) => ({ y, dashed: index < 5 }))
  const yTicks = [20, 67, 114, 161, 208].map((y, index) => {
    const value = scaleMax - ((scaleMax / 5) * index)
    return { y, label: formatCompactCurrency(value) }
  })

  const peakPoint = points[Math.min(peakIndex, points.length - 1)] || points[0]
  const bubbleLabel = formatCompactCurrency(peakPoint?.value || 0)
  const bubbleWidth = Math.max(78, (bubbleLabel.length * 7) + 18)

  return {
    points,
    gridLines,
    yTicks,
    linePath,
    areaPath,
    peakIndex,
    peakPoint,
    peakBubble: {
      x: peakPoint.x - (bubbleWidth / 2),
      y: Math.max(8, peakPoint.y - 22),
      width: bubbleWidth,
      label: bubbleLabel,
    },
  }
})

// ───────────────────────
// COMPUTED USER
// ───────────────────────
const userName = computed(() =>
  user.value.first_name || user.value.username || 'Admin'
)

watch(chartPeriod, loadTrendData)
</script>

<style scoped>

.admin-wrapper {
  width: 100%;
  min-height: 100vh;
  background: #F5F5F5;
}

.admin-content {
  width: 100%;
  overflow: auto;
  padding: 36px;
}

/* ── Topbar ── */
.topbar {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 32px;
}
.topbar{
  padding-top:8px;
}
.topbar__hello  { font-size: 20px; font-weight: 600; color: #1A1A1A; margin: 0 0 5px; }
.topbar__name   { color: #1B7A6E; font-weight: 700; }
.topbar__sub    { font-size: 16px; font-weight: 700; color: #1A1A1A; margin: 0; }
.topbar__brand  { color: #C8A135; font-weight: 800; }
.topbar__right  { display: flex; align-items: center; gap: 12px; margin-top: 6px; }

.topbar__search {
  width: 40px; height: 40px;
  border-radius: 10px;
  border: 1.5px solid #E5E7EB;
  background: #FFFFFF;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer; color: #6B7280;
  transition: border-color 0.2s, color 0.2s;
}
.topbar__search:hover { border-color: #1B7A6E; color: #1B7A6E; }

.avatar-menu { position: relative; }

.topbar__avatar {
  width: 40px; height: 40px;
  border-radius: 50%;
  overflow: hidden;
  border: 2px solid #E5E7EB;
  cursor: pointer;
  background: #1B7A6E;
  display: flex; align-items: center; justify-content: center;
  padding: 0;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.topbar__avatar:hover { border-color: #1B7A6E; box-shadow: 0 0 0 3px rgba(27,122,110,0.15); }
.topbar__avatar img   { width: 100%; height: 100%; object-fit: cover; display: block; }

.avatar-initials        { font-size: 13px; font-weight: 700; color: #FFFFFF; font-family: 'Montserrat', sans-serif; line-height: 1; }
.avatar-initials--lg    { font-size: 20px; }
.avatar-initials--xl    { font-size: 30px; }

/* ── Dropdown ── */
.dropdown {
  position: absolute;
  top: calc(100% + 10px); right: 0;
  width: 220px;
  background: #FFFFFF;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.14);
  border: 1px solid #F0F0F0;
  overflow: hidden; z-index: 100;
}
.dropdown__profile { display: flex; align-items: center; gap: 12px; padding: 16px; }
.dropdown__avatar  { width: 42px; height: 42px; border-radius: 50%; overflow: hidden; background: #1B7A6E; display: flex; align-items: center; justify-content: center; flex-shrink: 0; border: 2px solid #E5E5E5; }
.dropdown__avatar img { width: 100%; height: 100%; object-fit: cover; }
.dropdown__name  { font-size: 13px; font-weight: 700; color: #1A1A1A; margin: 0 0 2px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 130px; }
.dropdown__email { font-size: 11px; color: #9CA3AF; margin: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 130px; }
.dropdown__divider { height: 1px; background: #F3F3F3; }
.dropdown__item {
  display: flex; align-items: center; gap: 10px;
  width: 100%; padding: 12px 16px;
  background: none; border: none;
  font-size: 13px; font-weight: 500; font-family: 'Montserrat', sans-serif;
  color: #374151; cursor: pointer; text-align: left;
  transition: background 0.15s, color 0.15s;
}
.dropdown__item:hover          { background: #F5F5F5; color: #1B7A6E; }
.dropdown__item--logout        { color: #EF4444; }
.dropdown__item--logout:hover  { background: #FEF2F2; color: #DC2626; }

.dropdown-enter-active, .dropdown-leave-active { transition: opacity 0.18s ease, transform 0.18s ease; }
.dropdown-enter-from, .dropdown-leave-to       { opacity: 0; transform: translateY(-6px); }

/* ══════════════════════════════════════════
   PROFILE PANEL — Inline Edit Form
══════════════════════════════════════════ */
.profile-panel {
  background: #FFFFFF;
  border-radius: 16px;
  border: 1.5px solid #E8F5F3;
  box-shadow: 0 4px 24px rgba(27, 122, 110, 0.08);
  margin-bottom: 28px;
  overflow: hidden;
}

/* Slide-in transition */
.panel-slide-enter-active { transition: all 0.32s cubic-bezier(0.34, 1.2, 0.64, 1); }
.panel-slide-leave-active { transition: all 0.22s ease; }
.panel-slide-enter-from   { opacity: 0; transform: translateY(-16px); }
.panel-slide-leave-to     { opacity: 0; transform: translateY(-8px); }

/* Panel Header */
.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 18px 24px;
  border-bottom: 1.5px solid #F0F0F0;
  background: linear-gradient(135deg, #F0FAF8 0%, #FFFFFF 100%);
}
.panel-header__left {
  display: flex;
  align-items: center;
  gap: 14px;
}
.panel-header__icon {
  width: 38px; height: 38px;
  border-radius: 10px;
  background: #1B7A6E;
  display: flex; align-items: center; justify-content: center;
  color: #FFFFFF;
  flex-shrink: 0;
}
.panel-header__title { font-size: 15px; font-weight: 700; color: #1A1A1A; margin: 0 0 2px; }
.panel-header__sub   { font-size: 11.5px; color: #9CA3AF; margin: 0; }

.panel-close {
  width: 32px; height: 32px;
  border-radius: 8px;
  border: 1.5px solid #E5E5E5;
  background: #FFFFFF;
  cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  color: #9CA3AF;
  transition: all 0.2s;
  flex-shrink: 0;
}
.panel-close:hover { background: #FEF2F2; color: #EF4444; border-color: #EF4444; }

/* Panel Body: 2-column layout */
.panel-body {
  display: flex;
  gap: 0;
}

/* Left: Avatar */
.panel-left {
  width: 220px;
  flex-shrink: 0;
  padding: 32px 24px;
  border-right: 1.5px solid #F0F0F0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-upload-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.avatar-upload {
  width: 100px; height: 100px;
  border-radius: 50%;
  background: #1B7A6E;
  display: flex; align-items: center; justify-content: center;
  overflow: hidden;
  border: 3px solid #E5E5E5;
  box-shadow: 0 4px 16px rgba(27,122,110,0.18);
}
.avatar-upload img { width: 100%; height: 100%; object-fit: cover; display: block; }

.avatar-upload__btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 7px 16px;
  background: #1B7A6E;
  color: #FFFFFF;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  font-family: 'Montserrat', sans-serif;
  cursor: pointer;
  border: none;
  transition: background 0.2s, transform 0.15s, box-shadow 0.2s;
  box-shadow: 0 2px 8px rgba(27,122,110,0.2);
}
.avatar-upload__btn:hover { background: #156358; transform: translateY(-1px); box-shadow: 0 4px 12px rgba(27,122,110,0.3); }

.avatar-hint {
  font-size: 11px;
  color: #9CA3AF;
  text-align: center;
  margin: 0;
  line-height: 1.4;
}

.avatar-badge {
  display: inline-block;
  background: #F0FAF8;
  color: #1B7A6E;
  border: 1px solid #B2DDD8;
  font-size: 11px;
  font-weight: 700;
  padding: 4px 12px;
  border-radius: 20px;
  text-transform: uppercase;
  letter-spacing: 0.8px;
}

/* Right: Form */
.panel-right {
  flex: 1;
  padding: 28px 28px 24px;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18px;
  margin-bottom: 24px;
}

.form-group          { display: flex; flex-direction: column; gap: 6px; }
.form-group--full    { grid-column: 1 / -1; }

.form-label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11.5px;
  font-weight: 700;
  color: #6B7280;
  text-transform: uppercase;
  letter-spacing: 0.6px;
}

.form-input {
  height: 42px;
  border: 1.5px solid #E5E7EB;
  border-radius: 10px;
  padding: 0 14px;
  font-size: 13.5px;
  font-family: 'Montserrat', sans-serif;
  font-weight: 500;
  color: #1A1A1A;
  background: #FAFAFA;
  transition: border-color 0.2s, background 0.2s, box-shadow 0.2s;
  outline: none;
}
.form-input:focus {
  border-color: #1B7A6E;
  background: #FFFFFF;
  box-shadow: 0 0 0 3px rgba(27,122,110,0.1);
}
.form-input::placeholder { color: #C4C4C4; }

/* Input with @ prefix */
.input-prefix-wrap {
  position: relative;
  display: flex;
  align-items: center;
}
.input-prefix {
  position: absolute;
  left: 14px;
  font-size: 14px;
  font-weight: 700;
  color: #9CA3AF;
  pointer-events: none;
  font-family: 'Montserrat', sans-serif;
}
.form-input--prefix { padding-left: 28px; }

/* Live preview hint */
.form-hint {
  font-size: 11px;
  color: #9CA3AF;
  margin-top: 2px;
}
.form-hint b {
  color: #1B7A6E;
  font-weight: 700;
}

/* Action buttons */
.panel-actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 10px;
  padding-top: 4px;
  border-top: 1.5px solid #F0F0F0;
}

.btn-cancel {
  height: 40px;
  padding: 0 20px;
  border-radius: 10px;
  border: 1.5px solid #E5E7EB;
  background: #FFFFFF;
  font-size: 13px;
  font-weight: 600;
  font-family: 'Montserrat', sans-serif;
  color: #6B7280;
  cursor: pointer;
  transition: all 0.15s;
}
.btn-cancel:hover { border-color: #9CA3AF; color: #374151; background: #F9F9F9; }

.btn-save {
  height: 40px;
  padding: 0 22px;
  border-radius: 10px;
  border: none;
  background: #1B7A6E;
  font-size: 13px;
  font-weight: 700;
  font-family: 'Montserrat', sans-serif;
  color: #FFFFFF;
  cursor: pointer;
  transition: background 0.2s, transform 0.15s, box-shadow 0.2s;
  box-shadow: 0 2px 8px rgba(27,122,110,0.25);
}
.btn-save:hover         { background: #156358; box-shadow: 0 4px 14px rgba(27,122,110,0.35); transform: translateY(-1px); }
.btn-save--saved        { background: #059669; }
.btn-save--saved:hover  { background: #047857; }

.btn-save__content {
  display: flex;
  align-items: center;
  gap: 7px;
}

/* Button text swap transition */
.btn-save:disabled { opacity: 0.72; cursor: not-allowed; }
.btn-spinner {
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255,255,255,0.45);
  border-top-color: #FFFFFF;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}
.btn-swap-enter-active, .btn-swap-leave-active { transition: opacity 0.15s ease, transform 0.15s ease; }
.btn-swap-enter-from  { opacity: 0; transform: scale(0.85); }
.btn-swap-leave-to    { opacity: 0; transform: scale(0.85); }
@keyframes spin {
  to { transform: rotate(360deg); }
}

/* ── Stat Cards ── */
.stat-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 32px;
}
.stat-card {
  background: #FFFFFF;
  border-radius: 14px;
  padding: 20px;
  display: flex; align-items: center; gap: 16px;
  box-shadow: 0 1px 8px rgba(0,0,0,0.06);
  animation: fadeUp 0.4s ease both;
  animation-delay: var(--delay, 0s);
}
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(10px); }
  to   { opacity: 1; transform: translateY(0); }
}
.stat-card__icon-wrap {
  width: 50px; height: 50px;
  border-radius: 50%;
  background: #FFF3CD;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0; color: #C8A135;
}
.stat-card__number { font-size: 26px; font-weight: 800; color: #1A1A1A; margin: 0 0 2px; line-height: 1; }
.stat-card__label  { font-size: 12px; color: #6B7280; margin: 0; font-weight: 500; }
.stat-card__label.bold { font-weight: 700; color: #1A1A1A; font-size: 13px; }
.stat-card__sub    { font-size: 11px; color: #9CA3AF; margin: 3px 0 0; }

/* ── Section Header ── */
.section-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px; }
.section-header.mt { margin-top: 28px; }
.section-title  { font-size: 16px; font-weight: 700; color: #1A1A1A; margin: 0; }
.section-viewall { display: flex; align-items: center; gap: 4px; font-size: 13px; font-weight: 600; color: #6B7280; text-decoration: none; transition: color 0.2s; }
.section-viewall:hover { color: #1B7A6E; }

/* ── Chart ── */
.chart-card { background: #FFFFFF; border-radius: 14px; padding: 24px 24px 16px; box-shadow: 0 1px 8px rgba(0,0,0,0.06); }
.chart-card__header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; }
.chart-card__title  { font-size: 15px; font-weight: 700; color: #1A1A1A; margin: 0; }
.select-wrap { position: relative; }
.period-select {
  appearance: none;
  border: 1px solid #B2DDD8;
  background: #F0FAF8;
  color: #1B7A6E;
  font-size: 13px;
  font-weight: 600;
  padding: 9px 36px 9px 14px;
  border-radius: 10px;
  font-family: 'Montserrat', sans-serif;
  cursor: pointer;
}
.select-arrow {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #1B7A6E;
  pointer-events: none;
}
.chart-wrap { width: 100%; }
.chart-svg  { width: 100%; height: 280px; display: block; }
.chart-empty {
  height: 280px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #9CA3AF;
  font-size: 12px;
}

/* ── Table ── */
.table-card { background: #FFFFFF; border-radius: 14px; box-shadow: 0 1px 8px rgba(0,0,0,0.06); overflow: hidden; }
.table      { width: 100%; border-collapse: collapse; font-size: 13.5px; }
.table thead tr { border-bottom: 1.5px solid #F0F0F0; }
.table th { padding: 14px 18px; text-align: left; font-size: 12px; font-weight: 600; color: #9CA3AF; white-space: nowrap; font-family: 'Montserrat', sans-serif; }
.table tbody tr { border-bottom: 1px solid #F7F7F7; transition: background 0.15s; }
.table tbody tr:last-child { border-bottom: none; }
.table tbody tr:hover { background: #FAFAFA; }
.table td { padding: 13px 18px; vertical-align: middle; }
.td-no    { color: #9CA3AF; font-weight: 500; width: 40px; }

.table-card{
  overflow-x:auto;
}

.client-row { display: flex; align-items: center; gap: 12px; }
.avatar-table { width: 34px; height: 34px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 700; color: #FFFFFF; flex-shrink: 0; font-family: 'Montserrat', sans-serif; }
.client-name    { font-size: 13px; font-weight: 600; color: #1A1A1A; margin: 0 0 2px; }
.client-project { font-size: 11.5px; color: #9CA3AF; margin: 0; }

.badge { display: inline-flex; align-items: center; gap: 5px; padding: 4px 11px; border-radius: 20px; font-size: 12px; font-weight: 600; font-family: 'Montserrat', sans-serif; }
.badge::before { content: ''; width: 6px; height: 6px; border-radius: 50%; }
.badge--renovasi   { background: #F3F4F6; color: #6B7280; }
.badge--renovasi::before   { background: #9CA3AF; }
.badge--custom-furnitur { background: #EEF4FF; color: #315B9A; }
.badge--custom-furnitur::before { background: #4F7EC9; }
.badge--new-build { background: #F0FDF4; color: #1F7A45; }
.badge--new-build::before { background: #34A853; }
.badge--custom     { background: #FFFBEB; color: #B45309; }
.badge--custom::before     { background: #F59E0B; }

.td-biaya   { font-weight: 600; color: #1A1A1A; white-space: nowrap; }
.td-tanggal { color: #6B7280; white-space: nowrap; }
.td-actions { display: flex; align-items: center; gap: 8px; }

.action-btn {
  width: 30px; height: 30px; border-radius: 7px;
  border: 1px solid #E5E7EB; background: transparent;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer; color: #9CA3AF; transition: all 0.15s;
}
.action-btn:hover      { border-color: #1B7A6E; color: #1B7A6E; background: #F0FAF8; }
.action-btn--del:hover { border-color: #EF4444; color: #EF4444; background: #FEF2F2; }
</style>
