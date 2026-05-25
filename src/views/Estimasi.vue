<template>
  <div class="estimasi-page">

    <!-- ── Page Header ── -->
    <div class="page-header">
      <div class="container">
        <h1 class="page-header__title">Estimasi Biaya Proyek</h1>
        <div class="page-header__breadcrumb">
          <RouterLink to="/" class="breadcrumb__link">Home</RouterLink>
          <span class="breadcrumb__sep">›</span>
          <span class="breadcrumb__current">Estimasi</span>
        </div>
        <p class="page-header__desc">
          Lihat berbagai hasil karya <strong class="page-header__brand">SISI Interior</strong>
          yang dirancang untuk menghadirkan ruang yang estetik, nyaman, dan fungsional.
        </p>
      </div>
    </div>

    <!-- ── Main Content ── -->
    <section class="estimasi-section section">
      <div class="container estimasi-grid">
        <div class="estimasi-form">
          <div class="form-row">
            <div class="form-group">
              <label class="form-label">Nama Perusahaan</label>
              <input
                v-model="form.nama_perusahaan"
                type="text"
                class="form-input"
                placeholder=""
              />
            </div>
            <div class="form-group">
              <label class="form-label">Luas Area <span class="required-asterisk">*</span></label>
              <input
                v-model="form.luas_area"
                type="number"
                class="form-input"
                placeholder=""
                min="1"
              />
            </div>
          </div>

          <!-- Jenis Proyek -->
          <div class="field">
            <label class="field__label">Jenis Proyek <span class="required-asterisk">*</span></label>
            <div class="field__select-wrap">
              <select v-model="form.jenis_proyek" class="field__select">
                <option value="" disabled>Pilih jenis proyek</option>
                <option>Rumah</option>
                <option>Apartment</option>
                <option>Cafe</option>
                <option>Kantor</option>
                <option>Clinic</option>
                <option>Tenant</option>
                <option>Kost</option>
                <option>SPA</option>
                <option value="lainnya">Lainnya</option>
              </select>

              <input
                v-if="form.jenis_proyek === 'lainnya'"
                v-model="form.jenis_proyek_lainnya"
                type="text"
                class="field__input"
                placeholder="Masukkan jenis proyek lainnya"
              />
              <svg class="field__select-arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg>
            </div>
          </div>

          <div class="field">
            <label class="field__label">Jenis Pekerjaan <span class="required-asterisk">*</span></label>
            <select v-model="form.jenis_pekerjaan" class="field__select">
              <option value="" disabled>Pilih jenis pekerjaan</option>
              <option>Design</option>
              <option>Build / Fit Out</option>
              <option>Furniture</option>
              <option>MEP (Mechanical Electrical Plumbing)</option>
              <option>Maintenance</option>
              <option>Renovasi</option>
            </select>
          </div>

          <div class="field">
            <label class="field__label">Jenis Ruangan <span class="required-asterisk">*</span></label>

            <div class="multiselect" ref="multiRef">
              
              <!-- Trigger -->
              <div class="multiselect__trigger" @click.stop="toggleMultiSelect">
                <span v-if="form.jenis_ruangan.length === 0" class="multiselect__placeholder">
                  Silahkan pilih beberapa jenis
                </span>

                <span v-else class="multiselect__value">
                  {{ form.jenis_ruangan.join(', ') }}
                </span>

                <svg class="multiselect__arrow" width="16" height="16"
                  :style="{ transform: multiSelectOpen ? 'rotate(180deg)' : 'rotate(0deg)' }">
                  <polyline points="6 9 12 15 18 9"/>
                </svg>
              </div>

              <!-- Dropdown -->
              <div v-if="multiSelectOpen" class="multiselect__dropdown">
                <label 
                  v-for="item in daftarItemOptions" 
                  :key="item" 
                  class="multiselect__option"
                >
                  <input
                    type="checkbox"
                    :value="item"
                    v-model="form.jenis_ruangan"
                  />
                  <span>{{ item }}</span>
                </label>
              </div>

            </div>
          </div>

          
          <!-- Tingkat Kerumitan -->
          <div class="form-group">
            <label class="form-label">Tingkat Kerumitan <span class="required-asterisk">*</span></label>
            <div class="form-select-wrap">
              <select v-model="form.tingkat_kerumitan"class="form-select">
                <option value="">Pilih Tingkat Kerumitan</option>
                <option value="Mudah">Mudah</option>
                <option value="Sedang">Sedang</option>
                <option value="Sulit">Sulit</option>
              </select>
              <svg class="form-select-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg>
            </div>
          </div>

          <!-- Durasi Pengerjaan -->
          <div class="form-group">
            <label class="form-label">Durasi Pengerjaan (hari) <span class="required-asterisk">*</span></label>
            <input
              v-model="form.durasi_pengerjaan"
              type="number"
              class="form-input"
              placeholder=""
              min="1"
            />
          </div>

          <!-- Lokasi Proyek -->
          <div class="form-group">
            <label class="form-label">Lokasi Proyek <span class="required-asterisk">*</span></label>
            <input
              v-model="form.lokasi_proyek"
              type="text"
              class="form-input"
              placeholder=""
            />
          </div>

          <div class="field">
            <label class="field__label">Spesifikasi Design <span class="required-asterisk">*</span></label>
            <div class="field__select-wrap">
              <select v-model="form.spesifikasi_design" class="field__select">
                <option value="" disabled>Pilih spesifikasi design</option>
                <option>Japandi</option>
                <option>Industrial</option>
                <option>Scandinavian</option>
                <option>Modern</option>
                <option>Modern Minimalist</option>
                <option>Ekletik / Colorful</option>
                <option>Bohemian</option>
                <option>Klasik / Victorian</option>
                <option>Rustic</option>
                <option>Minimalis</option>
              </select>
              <svg class="field__select-arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg>
            </div>
          </div>

          <!-- Material Khusus -->
          <div class="field">
            <label class="form-label">Material Khusus</label>
            <div class="form-select-wrap">
              <select v-model="form.material_khusus" class="form-select">
                <option value="">Pilih Material</option>
                <option value="Kayu Jati">Kayu Jati</option>
                <option value="Kayu Mahoni">Kayu Mahoni</option>
                <option value="Kayu Jati Muda">Kayu Jati Muda</option>
                <option value="Multiplek">Multiplek</option>
                <option value="MDF">MDF</option>
                <option value="Besi">Besi</option>
                <option value="Kaca">Kaca</option>
                <option value="Marmer">Marmer</option>
                <option value="custom">Lainnya</option>
              </select>
              <svg class="form-select-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg>
            </div>
            <input
              v-if="form.material_khusus === 'custom'"
              v-model="form.material_custom"
              type="text"
              class="form-input form-input--stacked"
              placeholder="Masukkan material custom"
            />
          </div>

          <!-- Kebutuhan Tambahan -->
          <div class="form-group">
            <label class="form-label">Kebutuhan Tambahan</label>
            <textarea
              v-model="form.kebutuhan_tambahan"
              class="form-textarea"
              placeholder="Additional information"
              rows="4"
            ></textarea>
          </div>

          <!-- Tombol Reset + Simpan -->
          <div class="form-actions">
            <button
              type="button"
              class="btn-reset"
              @click="handleReset"
            >
              Reset
            </button>

            <button
              type="button"
              class="btn-simpan"
              @click="handleEstimasi"
              :disabled="isEstimating"
            >
              <span v-if="isEstimating" class="btn-spinner"></span>
              <span v-else>Proses</span>
            </button>
          </div>

        </div>

        <!-- ── Kanan: Ringkasan + Proses Estimasi ── -->
        <div class="estimasi-sidebar">

          <div class="ringkasan-card">
            <h2 class="ringkasan-card__title">Ringkasan Input</h2>

            <div class="ringkasan-card__rows">
              <div class="ringkasan-row">
                <span class="ringkasan-row__label">Luas Area </span>
                <span class="ringkasan-row__value">
                  <template v-if="form.luas_area">
                    {{ form.luas_area}} m² <span class="ringkasan-row__x">x</span> {{ form.luas_area}}
                  </template>
                  <template v-else>—</template>
                </span>
              </div>

              <div class="ringkasan-row">
                <span class="ringkasan-row__label">Kerumitan</span>
                <span class="ringkasan-row__value">{{ form.tingkat_kerumitan || '—' }}</span>
              </div>

              <div class="ringkasan-row">
                <span class="ringkasan-row__label">Durasi</span>
                <span class="ringkasan-row__value">
                  {{ form.durasi_pengerjaan ? form.durasi_pengerjaan + ' Hari' : '—' }}
                </span>
              </div>
            </div>

            <div class="ringkasan-divider"></div>

            <p class="ringkasan-card__disclaimer">
              Data yang Anda input hanya digunakan untuk proses estimasi
              biaya proyek interior. Hasil yang ditampilkan merupakan
              <strong>estimasi awal</strong> dan dapat berubah sesuai detail kebutuhan proyek.
              Halaman ini bukan halaman pembayaran atau transaksi.
            </p>

            <button
              class="btn-estimasi"
              @click="handleEstimasi"
              :disabled="isEstimating"
            >
              <span v-if="isEstimating" class="btn-spinner btn-spinner--dark"></span>
              <span v-else>Proses Estimasi</span>
            </button>

            <!-- Hasil Estimasi (muncul setelah proses) -->
            <div class="estimasi-result" v-if="estimasiResult">
              <div class="estimasi-result__divider"></div>
              <p class="estimasi-result__label">Estimasi Biaya</p>
              <div class="estimasi-result__rows">
                <div class="estimasi-result__row">
                  <span class="estimasi-result__sub-label">Minimum</span>
                  <span class="estimasi-result__sub-value">{{ formatRupiah(estimasiResult.minimum) }}</span>
                </div>
                <div class="estimasi-result__row">
                  <span class="estimasi-result__sub-label">Maksimum</span>
                  <span class="estimasi-result__sub-value">{{ formatRupiah(estimasiResult.maksimum) }}</span>
                </div>
                <div class="estimasi-result__row estimasi-result__row--highlight">
                  <span class="estimasi-result__sub-label">Rekomendasi</span>
                  <span class="estimasi-result__value">{{ formatRupiah(estimasiResult.rekomendasi) }}</span>
                </div>
              </div>
              <p class="estimasi-result__note">*Estimasi ini bersifat awal dan dapat berubah.</p>
            </div>

          </div>

        </div>

      </div>
    </section>

  </div>
</template>

<script setup>
import { ref, reactive,onMounted, onBeforeUnmount } from 'vue'
import { RouterLink } from 'vue-router'

const multiSelectOpen = ref(false)
const multiRef = ref(null)

const toggleMultiSelect = () => {
  multiSelectOpen.value = !multiSelectOpen.value
}

const daftarItemOptions = [
  //  Rumah
  "Living Room", "Master Room", "Bed Room", "Kitchen",
  "Dining Room", "Bath Room / Toilet", "Service Area",
  "Workspace", "Indoor Area", "Outdoor Area",
  "Backyard Garden", "Side Terrace",

  // Kantor
  "Lobby", "Director Room", "Manager Room", "Staff Room",
  "Office Room", "Meeting Room", "Waiting Room",
  "Consultation Room", "Treatment Room", "Training Room",
  "Cashier", "Canteen Area", "Mushalla",

  //  Bisnis
  "Pet Shop", "Pet Hotel", "Grooming Room", "Pet Clinic",

  //  Khusus
  "Understair Cabinet", "Kitchen Area", "Kitchen Set", "Kontainer Mart",

  //  Furniture
  "Bar Table", "Coffee Table", "Wooden Bench",
  "Wall Panel", "Pendant Lamp", "Backdrop Logo"
]

const handleClickOutside = (event) => {
  if (multiRef.value && !multiRef.value.contains(event.target)) {
    multiSelectOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})

const isSaving    = ref(false)
const isEstimating = ref(false)
const estimasiResult = ref(null)

const form = reactive({
  nama_perusahaan: '',
  luas_area: '',
  jenis_proyek: '',
  jenis_proyek_lainnya: '',
  jenis_pekerjaan: '',
  jenis_ruangan: [],

  tingkat_kerumitan: '',
  durasi_pengerjaan: '',

  lokasi_proyek: '',
  spesifikasi_design: '',
  material_khusus: '',
  material_custom: '',
  kebutuhan_tambahan: '',
})

const parseNumber = (value) => {
  const numericValue = Number(value)
  return Number.isFinite(numericValue) ? numericValue : 0
}

const formatRupiah = (angka) => {
  const numericValue = parseNumber(angka)
  return new Intl.NumberFormat('id-ID', {
    style: 'currency',
    currency: 'IDR',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  })
    .format(numericValue)
    .replace('Rp', 'Rp ')
}

const getJenisProyekPayload = () => (
  form.jenis_proyek === 'lainnya'
    ? (form.jenis_proyek_lainnya || '').trim()
    : form.jenis_proyek
)

const getMaterialPayload = () => (
  form.material_khusus === 'custom'
    ? (form.material_custom || '').trim()
    : form.material_khusus
)

const handleReset = () => {
  form.nama_perusahaan = ''
  form.luas_area = ''
  form.jenis_proyek = ''
  form.jenis_proyek_lainnya = ''
  form.jenis_pekerjaan = ''
  form.jenis_ruangan = [] 
  form.tingkat_kerumitan = ''
  form.durasi_pengerjaan = ''
  form.lokasi_proyek = ''
  form.spesifikasi_design = ''
  form.material_khusus = ''
  form.material_custom = ''
  form.kebutuhan_tambahan = ''

  estimasiResult.value = null
}

const handleSimpan = async () => {
  isSaving.value = true
  try {
    const token = localStorage.getItem('token')
    const res = await fetch('http://localhost:8081/api/users/estimasi',{
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
    body: JSON.stringify({
      nama_perusahaan: form.nama_perusahaan,
      luas_area: Number(form.luas_area),

      //  array → string (wajib disesuaikan ke backend ML)
      jenis_ruangan: form.jenis_ruangan[0] || '',

      jenis_proyek: getJenisProyekPayload(),
      jenis_pekerjaan: form.jenis_pekerjaan,
      tingkat_kerumitan: form.tingkat_kerumitan,
      durasi_pengerjaan: Number(form.durasi_pengerjaan),
      lokasi_proyek: form.lokasi_proyek,
      spesifikasi_design: form.spesifikasi_design,
      material_khusus: getMaterialPayload(),
      kebutuhan_tambahan: form.kebutuhan_tambahan,
    })
    })

    const data = await res.json()
    if (!res.ok) throw new Error(data.message || 'Gagal menyimpan.')
    alert('Data berhasil disimpan!')
  } catch (err) {
    alert(err.message || 'Tidak dapat terhubung ke server.')
  } finally {
    isSaving.value = false
  }
}

const handleEstimasi = async () => {
  if (
    !form.luas_area ||
    !form.jenis_proyek ||
    (form.jenis_proyek === 'lainnya' && !form.jenis_proyek_lainnya.trim()) ||
    !form.jenis_pekerjaan ||
    !form.tingkat_kerumitan ||
    !form.durasi_pengerjaan ||
    !form.lokasi_proyek ||
    !form.spesifikasi_design ||
    form.jenis_ruangan.length === 0 ||
    (form.material_khusus === 'custom' && !form.material_custom.trim())
  ) {
    alert('Lengkapi semua data wajib estimasi!')
    return
  }

  isEstimating.value = true
  estimasiResult.value = null

  try {
    const token = localStorage.getItem('token')
    const res = await fetch('http://localhost:8081/api/users/estimasi', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({
        nama_perusahaan: form.nama_perusahaan,
        luas_area: Number(form.luas_area),
        jenis_proyek: getJenisProyekPayload(),
        jenis_pekerjaan: form.jenis_pekerjaan,
        jenis_ruangan: form.jenis_ruangan.join(', '),
        tingkat_kerumitan: form.tingkat_kerumitan,
        durasi_pengerjaan: Number(form.durasi_pengerjaan || 0),
        lokasi_proyek: form.lokasi_proyek,
        spesifikasi_design: form.spesifikasi_design,
        material_khusus: getMaterialPayload(),
        kebutuhan_tambahan: form.kebutuhan_tambahan,
      }),
    })

    if (!res.ok) {
      throw new Error('Gagal mengambil estimasi dari server')
    }

    const data = await res.json()
    const rekomendasi = parseNumber(
      data.rekomendasi ?? data.estimasi_harga ?? data.data?.rekomendasi ?? data.data?.estimasi
    )
    const minimum = parseNumber(data.minimum ?? (rekomendasi * 0.8))
    const maksimum = parseNumber(data.maksimum ?? (rekomendasi * 1.2))

    estimasiResult.value = {
      minimum,
      maksimum,
      rekomendasi,
    }

  } catch (err) {
    console.error(err)
    alert('Gagal terhubung ke server estimasi')
  } finally {
    isEstimating.value = false
  }
}
</script>

<style scoped>
.estimasi-page {
  padding-top: 72px;
  font-family: 'Montserrat', sans-serif;
  background: #FFFFFF;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 40px;
}

.section {
  padding: 48px 0 80px;
}

/* ── Page Header ── */
.page-header {
  padding: 40px 0 0;
  background: #FFFFFF;
}

.page-header__title {
  font-size: 36px;
  font-weight: 800;
  color: #2C2C2C;
  margin: 0 0 10px;
}

.page-header__breadcrumb {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #888;
  margin-bottom: 16px;
}

.breadcrumb__link {
  color: #888;
  text-decoration: none;
  transition: color 0.2s;
}

.breadcrumb__link:hover { color: #1B7A6E; }
.breadcrumb__sep        { color: #aaa; }
.breadcrumb__current    { color: #555; }

.page-header__desc {
  font-size: 14px;
  line-height: 1.8;
  color: #444;
  margin: 0 0 8px;
}

.page-header__brand {
  color: #1B7A6E;
  font-weight: 700;
}

/* ── Layout Grid ── */
.estimasi-grid {
  display: grid;
  grid-template-columns: 1fr 380px;
  gap: 60px;
  align-items: start;
}

/* ── Form ── */
.estimasi-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-label {
  font-size: 13px;
  font-weight: 600;
  color: #2C2C2C;
}

.required-asterisk {
  color: #D64545;
  font-size: 11px;
  vertical-align: super;
}

.form-input {
  width: 100%;
  border: 1.5px solid #DDDDDD;
  border-radius: 6px;
  padding: 13px 16px;
  font-size: 13.5px;
  font-family: 'Montserrat', sans-serif;
  color: #333;
  background: #FFFFFF;
  outline: none;
  transition: border-color 0.2s;
  box-sizing: border-box;
}

.form-input:focus { border-color: #C8A135; }
.form-input::placeholder { color: #BBBBBB; }

.form-input--stacked {
  margin-top: 10px;
}

/* Remove number input arrows */
.form-input[type='number']::-webkit-inner-spin-button,
.form-input[type='number']::-webkit-outer-spin-button { -webkit-appearance: none; }
.form-input[type='number'] { -moz-appearance: textfield; }

/* Select */
.form-select-wrap {
  position: relative;
}

.form-select {
  width: 100%;
  border: 1.5px solid #DDDDDD;
  border-radius: 6px;
  padding: 13px 40px 13px 16px;
  font-size: 13.5px;
  font-family: 'Montserrat', sans-serif;
  color: #333;
  background: #FFFFFF;
  outline: none;
  appearance: none;
  cursor: pointer;
  transition: border-color 0.2s;
  box-sizing: border-box;
}

.form-select:focus { border-color: #C8A135; }

.form-select-icon {
  position: absolute;
  right: 14px;
  top: 50%;
  transform: translateY(-50%);
  color: #888;
  pointer-events: none;
}

/* Textarea */
.form-textarea {
  width: 100%;
  border: 1.5px solid #DDDDDD;
  border-radius: 6px;
  padding: 13px 16px;
  font-size: 13.5px;
  font-family: 'Montserrat', sans-serif;
  color: #333;
  background: #FFFFFF;
  outline: none;
  resize: vertical;
  min-height: 100px;
  transition: border-color 0.2s;
  box-sizing: border-box;
}

.form-textarea:focus { border-color: #C8A135; }
.form-textarea::placeholder { color: #BBBBBB; }

/* ── Form Actions ── */
.form-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-top: 4px;
}

.btn-reset {
  background: none;
  border: none;
  font-size: 13.5px;
  font-weight: 600;
  font-family: 'Montserrat', sans-serif;
  color: #888;
  cursor: pointer;
  padding: 4px 0;
  transition: color 0.2s;
  align-self: flex-end;
}

.btn-reset:hover { color: #444; }

.btn-simpan {
  flex: 1;
  background: #C8A135;
  color: #FFFFFF;
  font-size: 14px;
  font-weight: 700;
  font-family: 'Montserrat', sans-serif;
  padding: 16px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.2s ease, transform 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.btn-simpan:hover:not(:disabled) {
  background: #b08e2c;
  transform: translateY(-1px);
}

.btn-simpan:disabled { opacity: 0.7; cursor: not-allowed; }

/* ── Sidebar Ringkasan ── */
.estimasi-sidebar {
  position: sticky;
  top: 96px;
}

.ringkasan-card {
  border: 1.5px solid #E5E5E5;
  border-radius: 10px;
  padding: 28px 28px 32px;
  background: #FFFFFF;
}

.ringkasan-card__title {
  font-size: 18px;
  font-weight: 800;
  color: #2C2C2C;
  margin: 0 0 20px;
}

.ringkasan-card__rows {
  display: flex;
  flex-direction: column;
  gap: 14px;
  margin-bottom: 20px;
}

.ringkasan-row {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 12px;
}

.ringkasan-row__label {
  font-size: 12.5px;
  color: #888;
  flex-shrink: 0;
}

.ringkasan-row__value {
  font-size: 12.5px;
  font-weight: 700;
  color: #2C2C2C;
  text-align: right;
}

.ringkasan-row__x {
  font-size: 11px;
  color: #aaa;
  margin: 0 2px;
}

.ringkasan-divider {
  height: 1px;
  background: #EEEEEE;
  margin: 20px 0;
}

.ringkasan-card__disclaimer {
  font-size: 12px;
  line-height: 1.8;
  color: #666;
  text-align: justify;
  margin: 0 0 24px;
}

/* ── Proses Estimasi Button ── */
.btn-estimasi {
  width: 100%;
  background: #FFFFFF;
  color: #2C2C2C;
  font-size: 14px;
  font-weight: 600;
  font-family: 'Montserrat', sans-serif;
  padding: 15px;
  border: 1.5px solid #CCCCCC;
  border-radius: 6px;
  cursor: pointer;
  transition: border-color 0.2s, background 0.2s, transform 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.btn-estimasi:hover:not(:disabled) {
  border-color: #1B7A6E;
  color: #1B7A6E;
  transform: translateY(-1px);
}

.btn-estimasi:disabled { opacity: 0.6; cursor: not-allowed; }

/* ── Hasil Estimasi ── */
.estimasi-result {
  margin-top: 4px;
}

.estimasi-result__divider {
  height: 1px;
  background: #EEEEEE;
  margin: 20px 0;
}

.estimasi-result__label {
  font-size: 12px;
  color: #888;
  margin: 0 0 6px;
}

.estimasi-result__value {
  font-size: 20px;
  font-weight: 800;
  color: #1B7A6E;
  margin: 0 0 6px;
}

.estimasi-result__rows {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 8px;
}

.estimasi-result__row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.estimasi-result__row--highlight {
  padding-top: 4px;
}

.estimasi-result__sub-label {
  font-size: 12px;
  font-weight: 600;
  color: #666;
}

.estimasi-result__sub-value {
  font-size: 13px;
  font-weight: 700;
  color: #2C2C2C;
  text-align: right;
}

.estimasi-result__note {
  font-size: 11px;
  color: #aaa;
  margin: 0;
}

/* ── Field (SAMAKAN DENGAN form-group) ── */
.field {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.field__label {
  font-size: 13px;
  font-weight: 600;
  color: #2C2C2C;
}

/* wrapper select */
.field__select-wrap {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

/* select style disamakan */
.field__select {
  width: 100%;
  border: 1.5px solid #DDDDDD;
  border-radius: 6px;
  padding: 13px 40px 13px 16px;
  font-size: 13.5px;
  font-family: 'Montserrat', sans-serif;
  color: #333;
  background: #FFFFFF;
  outline: none;
  appearance: none;
  cursor: pointer;
  transition: border-color 0.2s;
  box-sizing: border-box;
}

.field__select:focus {
  border-color: #C8A135;
}

/* input tambahan (jenis proyek lainnya) */
.field__input {
  width: 100%;
  border: 1.5px solid #DDDDDD;
  border-radius: 6px;
  padding: 13px 16px;
  font-size: 13.5px;
  font-family: 'Montserrat', sans-serif;
  color: #333;
  background: #FFFFFF;
  outline: none;
  transition: border-color 0.2s;
  box-sizing: border-box;
}

.field__input:focus {
  border-color: #C8A135;
}

/* arrow */
.field__select-arrow {
  position: absolute;
  right: 14px;
  top: 16px;
  color: #888;
  pointer-events: none;
}

.multiselect__dropdown {
  z-index: 999; /* biar tidak ketutup */
}

/* ── Spinner ── */
.btn-spinner {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255,255,255,0.4);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
  display: inline-block;
}

.btn-spinner--dark {
  border-color: rgba(0,0,0,0.15);
  border-top-color: #2C2C2C;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* ── Responsive ── */
@media (max-width: 960px) {
  .estimasi-grid {
    grid-template-columns: 1fr;
    gap: 36px;
  }

  .estimasi-sidebar {
    position: static;
    order: -1;
  }
}

/* MULTISELECT WRAPPER */
.multiselect {
  position: relative;
  width: 100%;
}

/* TRIGGER = MIRIP SELECT */
.multiselect__trigger {
  width: 100%;
  border: 1.5px solid #DDDDDD;
  border-radius: 6px;
  padding: 13px 40px 13px 16px;
  font-size: 13.5px;
  font-family: 'Montserrat', sans-serif;
  background: #FFFFFF;
  color: #333;

  display: flex;
  align-items: center;
  justify-content: space-between;

  cursor: pointer;
  transition: all 0.2s ease;
}

/* HOVER */
.multiselect__trigger:hover {
  border-color: #C8A135;
}

/* FOCUS */
.multiselect__trigger:focus {
  border-color: #C8A135;
  box-shadow: 0 0 0 2px rgba(200,161,53,0.15);
}

/* TEXT */
.multiselect__placeholder {
  color: #BBBBBB;
}

.multiselect__value {
  color: #333;
}

/* ARROW */
.multiselect__arrow {
  position: absolute;
  right: 14px;
  top: 50%;
  transform: translateY(-50%);
  color: #888;
  pointer-events: none;
}

/* DROPDOWN */
.multiselect__dropdown {
  position: absolute;
  top: calc(100% + 6px);
  left: 0;
  width: 100%;
  background: #fff;
  border: 1.5px solid #DDDDDD;
  border-radius: 6px;
  box-shadow: 0 8px 20px rgba(0,0,0,0.08);
  z-index: 10;
  max-height: 200px;
  overflow-y: auto;
}

/* OPTION */
.multiselect__option {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  cursor: pointer;
}

.multiselect__option:hover {
  background: #F8F8F8;
}

.multiselect__option input {
  accent-color: #C8A135;
}

@media (max-width: 560px) {
  .container { padding: 0 20px; }
  .form-row  { grid-template-columns: 1fr; }
  .form-actions { flex-direction: column-reverse; align-items: stretch; }
  .btn-reset { text-align: center; }
}
</style>
