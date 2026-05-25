<template>
  <div class="analitik-page">

    <!-- â”€â”€ HEADER â”€â”€ -->
    <div class="page-header">
      <h1 class="page-title">Dashboard Analitik</h1>
      <div class="header-right">
        <div class="search-box">
          <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
          </svg>
          <input type="text" v-model="searchQuery" placeholder="Search" class="search-input" />
        </div>
        <button class="notif-btn">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>
            <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
          </svg>
          <span class="notif-dot"></span>
        </button>
        <AdminAccountMenu />
      </div>
    </div>

    <!-- â”€â”€ ROW 1: STAT CARDS â”€â”€ -->
    <div class="stats-row">
      <div class="stat-card" v-for="stat in stats" :key="stat.key">
        <p class="stat-label">{{ stat.label }}</p>
        <p class="stat-value" :class="{ 'stat-value--gold': stat.gold }">{{ stat.value }}</p>
        <p class="stat-sub" :class="{ 'stat-sub--link': stat.linkSub }">{{ stat.sub }}</p>
      </div>
    </div>

    <!-- â”€â”€ ROW 2: GRAFIK + KATEGORI â”€â”€ -->
    <div class="chart-row">

      <!-- Grafik Tren -->
      <div class="chart-card">
        <div class="chart-card__header">
          <h2 class="section-title">Grafik Tren Biaya Proyek</h2>
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
            <path :d="chartSvg.areaPath" fill="url(#areaGradAnalitik)" />
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
              <linearGradient id="areaGradAnalitik" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="#1B7A6E" stop-opacity="0.35" />
                <stop offset="100%" stop-color="#1B7A6E" stop-opacity="0" />
              </linearGradient>
            </defs>
          </svg>
          <div v-else class="chart-empty">Belum ada data estimasi untuk periode ini.</div>
        </div>
      </div>
    </div>

    <!-- â”€â”€ ROW 3: PERFORMA + TINGKAT KERUMITAN â”€â”€ -->
    <div class="content-row">

      <!-- Performa / Ringkasan Proyek -->
      <div class="chart-card">
        <div class="chart-card__header">
          <h2 class="section-title">Performa / Ringkasan Proyek</h2>
          <button class="btn-see-all" @click="goToDataProyek">
            See All
          </button>
        </div>
        <table class="performa-table">
          <thead>
            <tr>
              <th>Jenis Proyek</th>
              <th>Jenis Pekerjaan</th>
              <th>Harga Proyek</th>
              <th>Durasi</th>
              <th>Tanggal</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(p, index) in performaProyek" :key="`${p.nama}-${index}`">
              <td class="td-nama">{{ p.nama }}</td>
              <td class="td-jenis">{{ p.jenis }}</td>
              <td class="td-biaya">{{ p.biaya }}</td>
              <td class="td-durasi">{{ p.durasi }}</td>
              <td class="td-tanggal">{{ p.tanggal }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Tingkat Kerumitan -->
      <div class="side-stack">
        <div class="side-card">
          <h2 class="section-title">Kategori Proyek</h2>
          <div class="kategori-list">
            <div class="kategori-row" v-for="k in kategoriProyek" :key="k.nama">
              <span class="kategori-nama">{{ k.nama }}</span>
              <span class="kategori-pct">{{ k.pct }}%</span>
            </div>
          </div>
        </div>

        <div class="side-card">
          <h2 class="section-title">Tingkat Kerumitan</h2>
          <div class="kerumitan-list">
            <div class="kerumitan-row" v-for="k in tingkatKerumitan" :key="k.label">
              <span class="kerumitan-dot" :style="{ background: k.color }"></span>
              <span class="kerumitan-label">{{ k.label }}</span>
              <span class="kerumitan-pct">{{ k.pct }}%</span>
            </div>
          </div>
        </div>
      </div>

    </div>

  </div>
</template>

<script setup>
import { computed, ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import AdminAccountMenu from '@/components/AdminAccountMenu.vue'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://rent-installation-utc-remedy.trycloudflare.com/api'

const searchQuery = ref('')
const chartPeriod = ref('this_month')
const avatarImg = ref(null)
const avatarFallback = ref(null)

const token = localStorage.getItem('token')
const router = useRouter()

const performaProyek = ref([])
const kategoriProyek = ref([])
const tingkatKerumitan = ref([])
const trendData = ref({
  labels: [],
  values: [],
  peak: { index: 0, label: '', value: 0 },
})

const stats = ref([
  { key: 'total', label: 'Total Proyek', value: '0', sub: 'Proyek', gold: true, linkSub: true },
  { key: 'rata', label: 'Rata-rata Biaya Proyek', value: 'Rp 0', sub: 'Dalam 1 Bulan terakhir', gold: true, linkSub: false },
  { key: 'tinggi', label: 'Biaya Tertinggi', value: 'Rp 0', sub: 'Per proyek', gold: true, linkSub: false },
  { key: 'rendah', label: 'Biaya Terendah', value: 'Rp 0', sub: 'Per proyek', gold: true, linkSub: false },
])

const formatRupiah = (angka) =>
  new Intl.NumberFormat('id-ID', {
    style: 'currency',
    currency: 'IDR',
    minimumFractionDigits: 0,
  }).format(Number(angka || 0))

const formatCompactCurrency = (value) => {
  const amount = Number(value || 0)
  if (amount >= 1000000000) return `${(amount / 1000000000).toFixed(1).replace('.0', '')}M`
  if (amount >= 1000000) return `${(amount / 1000000).toFixed(1).replace('.0', '')}Jt`
  if (amount >= 1000) return `${(amount / 1000).toFixed(0)}K`
  return `${amount}`
}

const goToDataProyek = () => {
  router.push('/admin/estimasi')
}

const getDashboardStats = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/admin/dashboard/stats`, {
      headers: { Authorization: `Bearer ${token}` },
    })

    const dashboard = response.data.data || {}
    stats.value[0].value = dashboard.total_proyek || 0
    stats.value[1].value = formatRupiah(dashboard.rata_rata_biaya || 0)
    stats.value[2].value = formatRupiah(dashboard.biaya_tertinggi || 0)
    stats.value[3].value = formatRupiah(dashboard.biaya_terendah || 0)
  } catch (error) {
    console.error('Gagal mengambil dashboard stats:', error)
  }
}

const chartSvg = computed(() => {
  const labels = trendData.value.labels || []
  const values = (trendData.value.values || []).map((value) => Number(value || 0))
  const peakIndex = Number(trendData.value.peak?.index ?? 0)

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

const loadTren = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/admin/dashboard/trend?period=${chartPeriod.value}`, {
      headers: { Authorization: `Bearer ${token}` },
    })

    if (!response.ok) {
      throw new Error('Gagal mengambil tren biaya proyek')
    }

    const result = await response.json()
    const data = result.data || {}
    trendData.value = {
      labels: Array.isArray(data.labels) ? data.labels : [],
      values: Array.isArray(data.values) ? data.values.map(Number) : [],
      peak: {
        index: Number(data.peak?.index ?? 0),
        label: data.peak?.label ?? '',
        value: Number(data.peak?.value ?? 0),
      },
    }

  } catch (error) {
    console.error('Gagal mengambil tren biaya proyek:', error)
    trendData.value = { labels: [], values: [], peak: { index: 0, label: '', value: 0 } }
  }
}

const getPerformaProyek = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/admin/dashboard/performa-proyek`, {
      headers: { Authorization: `Bearer ${token}` },
    })

    if (!response.ok) {
      throw new Error('Gagal mengambil performa proyek')
    }

    const result = await response.json()
    performaProyek.value = (result.data || []).map((item) => ({
      nama: item.jenis_proyek,
      jenis: item.jenis_pekerjaan,
      biaya: formatRupiah(item.harga_proyek),
      durasi: item.durasi_pengerjaan,
      tanggal: new Date(item.created_at).toLocaleDateString('id-ID'),
    }))
  } catch (error) {
    console.error('Gagal mengambil performa proyek:', error)
  }
}

const getKategoriProyek = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/admin/dashboard/kategori-proyek`, {
      headers: { Authorization: `Bearer ${token}` },
    })

    if (!response.ok) {
      throw new Error('Gagal mengambil kategori proyek')
    }

    const result = await response.json()
    kategoriProyek.value = result.data || []
  } catch (error) {
    console.error('Gagal mengambil kategori proyek:', error)
  }
}

const getTingkatKerumitan = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/admin/dashboard/tingkat-kerumitan`, {
      headers: { Authorization: `Bearer ${token}` },
    })

    if (!response.ok) {
      throw new Error('Gagal mengambil tingkat kerumitan')
    }

    const result = await response.json()
    tingkatKerumitan.value = (result.data || []).map((item) => ({
      label: item.label,
      pct: item.pct,
      color: item.label === 'Mudah'
        ? '#6DD69A'
        : item.label === 'Sedang'
        ? '#E8C96A'
        : '#E85C5C',
    }))
  } catch (error) {
    console.error('Gagal mengambil tingkat kerumitan:', error)
  }
}

const loadData = async () => {
  await loadTren()
}

onMounted(() => {
  getDashboardStats()
  getPerformaProyek()
  getKategoriProyek()
  getTingkatKerumitan()

  loadData()
})

watch(chartPeriod, loadTren)

const onAvatarError = () => {
  if (avatarImg.value) avatarImg.value.style.display = 'none'
  if (avatarFallback.value) avatarFallback.value.style.display = 'flex'
}
</script>

<style scoped>
.analitik-page {
  padding: 24px 28px;
  min-height: 100vh;
  background: #F4F5F7;
  font-family: 'Montserrat', sans-serif;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* â”€â”€ Header â”€â”€ */
.page-header {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 4px;
}
.page-title { font-size: 22px; font-weight: 700; color: #1A1A2E; }
.header-right { display: flex; align-items: center; gap: 10px; }

.search-box {
  display: flex; align-items: center; gap: 8px;
  background: #FFFFFF; border: 1.5px solid #E8E8E8;
  border-radius: 24px; padding: 8px 16px; width: 220px;
}
.search-icon { color: #C8A135; flex-shrink: 0; }
.search-input {
  border: none; outline: none;
  font-family: 'Montserrat', sans-serif; font-size: 12px;
  color: #333; background: transparent; width: 100%;
}
.search-input::placeholder { color: #AAAAAA; }

.notif-btn {
  position: relative; background: #FFFFFF; border: 1.5px solid #E8E8E8;
  border-radius: 50%; width: 38px; height: 38px;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer; color: #555;
}
.notif-dot {
  position: absolute; top: 7px; right: 7px;
  width: 6px; height: 6px; background: #C8A135;
  border-radius: 50%; border: 1.5px solid #fff;
}
.avatar {
  width: 38px; height: 38px; border-radius: 50%; overflow: hidden;
  background: #1B7A6E; display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}
.avatar img { width: 100%; height: 100%; object-fit: cover; }
.avatar-fallback { display: none; align-items: center; justify-content: center; font-size: 13px; font-weight: 700; color: #fff; }

/* â”€â”€ Stat Cards Row â”€â”€ */
.stats-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}
.stat-card {
  background: #FFFFFF;
  border-radius: 14px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
  padding: 20px 22px 18px;
}
.stat-label {
  font-size: 12px; font-weight: 500; color: #999;
  margin-bottom: 8px;
}
.stat-value {
  font-size: 22px; font-weight: 700; color: #1A1A2E;
  margin-bottom: 4px; line-height: 1.2;
}
.stat-value--gold { color: #C8A135; }
.stat-sub {
  font-size: 11px; color: #999;
}
.stat-sub--link { color: #C8A135; font-weight: 600; cursor: pointer; }
.stat-sub--link:hover { text-decoration: underline; }

/* â”€â”€ Row layout (chart + side) â”€â”€ */
.chart-row {
  display: block;
}

.content-row {
  display: grid;
  grid-template-columns: 1fr 260px;
  gap: 16px;
  align-items: start;
}

/* â”€â”€ Chart Card â”€â”€ */
.chart-card {
  background: #FFFFFF;
  border-radius: 14px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
  padding: 22px 22px 18px;
}
.chart-card__header {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 20px;
}
.section-title {
  font-size: 15px; font-weight: 700; color: #1A1A2E;
}
.chart-wrap {
  position: relative; height: 280px;
}
.chart-svg {
  width: 100%;
  height: 100%;
  display: block;
}
.chart-empty {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #9CA3AF;
  font-size: 12px;
}

.select-wrap { position: relative; }
.period-select {
  appearance: none; -webkit-appearance: none;
  padding: 7px 28px 7px 12px;
  background: #F0FAF8; border: 1.5px solid #C8E8E4; border-radius: 8px;
  font-family: 'Montserrat', sans-serif; font-size: 11px; font-weight: 600;
  color: #1B7A6E; outline: none; cursor: pointer;
}
.select-arrow {
  position: absolute; right: 8px; top: 50%;
  transform: translateY(-50%); color: #1B7A6E; pointer-events: none;
}

/* â”€â”€ Side Card â”€â”€ */
.side-card {
  background: #FFFFFF;
  border-radius: 14px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
  padding: 22px 20px;
}
.side-stack {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* Kategori Proyek */
.kategori-list { display: flex; flex-direction: column; gap: 20px; margin-top: 18px; }
.kategori-row { display: flex; align-items: center; justify-content: space-between; }
.kategori-nama { font-size: 13px; color: #444; }
.kategori-pct  { font-size: 14px; font-weight: 700; color: #1B7A6E; }

/* Performa table */
.performa-table { width: 100%; border-collapse: collapse; }
.performa-table th {
  padding: 8px 0; font-size: 11px; font-weight: 500;
  color: #AAAAAA; text-align: left; border-bottom: 1px solid #F0F0F0;
}
.performa-table td {
  padding: 14px 0; font-size: 12px; color: #444;
  border-bottom: 1px solid #F6F6F6; vertical-align: middle;
}
.performa-table tbody tr:last-child td { border-bottom: none; }
.td-nama   { font-weight: 700; color: #1A1A2E; }
.td-jenis  { font-weight: 600; color: #444; }
.td-biaya  { font-weight: 600; }
.td-durasi { text-align: center; }
.td-tanggal { color: #888; font-size: 11px; white-space: nowrap; }

.btn-see-all {
  padding: 7px 16px;
  background: #F4F5F7; border: 1px solid #E8E8E8; border-radius: 8px;
  font-family: 'Montserrat', sans-serif; font-size: 11px; font-weight: 600;
  color: #555; cursor: pointer; transition: background 0.2s;
}
.btn-see-all:hover { background: #EAEAEA; }

/* Tingkat Kerumitan */
.kerumitan-list { display: flex; flex-direction: column; gap: 20px; margin-top: 18px; }
.kerumitan-row { display: flex; align-items: center; gap: 12px; }
.kerumitan-dot { width: 20px; height: 20px; border-radius: 50%; flex-shrink: 0; }
.kerumitan-label { flex: 1; font-size: 13px; color: #444; }
.kerumitan-pct { font-size: 14px; font-weight: 700; color: #1B7A6E; }
</style>
