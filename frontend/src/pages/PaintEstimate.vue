<script setup>
import { ref } from 'vue'
import { postJSON } from '../api'
const room_id = ref(1)
const band = ref(false)
const waist_height = ref(1.0)
const lower_coverage = ref(6)
const lower_coats = ref(2)
const upper_coverage = ref(10)
const upper_coats = ref(2)
const out = ref(null)
const err = ref('')
const run = async () => {
  err.value = ''
  try {
    out.value = await postJSON('/api/estimate', {
      room_id: room_id.value, persist: true,
      band: band.value, waist_height: waist_height.value,
      lower_coverage: lower_coverage.value, lower_coats: lower_coats.value,
      upper_coverage: upper_coverage.value, upper_coats: upper_coats.value,
    })
  } catch (e) { err.value = String(e); out.value = null }
}
</script>
<template><div class="page"><h1>估漆工作台</h1>
<label>房间ID <input v-model.number="room_id" /></label>
<label><input type="checkbox" v-model="band" /> 墙腰双色分带</label>
<fieldset v-if="band" class="band-box">
  <label>腰线离地(m) <input type="number" step="0.05" v-model.number="waist_height" /></label>
  <label>下带涂布率 <input type="number" step="0.5" v-model.number="lower_coverage" /></label>
  <label>下带遍数 <input type="number" step="1" v-model.number="lower_coats" /></label>
  <label>上带涂布率 <input type="number" step="0.5" v-model.number="upper_coverage" /></label>
  <label>上带遍数 <input type="number" step="1" v-model.number="upper_coats" /></label>
</fieldset>
<button @click="run">估算</button>
<p v-if="err" class="err">{{ err }}</p>
<template v-if="out && !out.band">
  <p>净 {{ out.net_m2 }} m² · {{ out.liters }} 升 · {{ out.coats }} 遍</p>
</template>
<template v-if="out && out.band">
  <p>净 {{ out.net_m2 }} m² · 腰线 {{ out.waist_height }} m</p>
  <table>
    <tr><th>带</th><th>净面积 m²</th><th>涂布率</th><th>遍数</th><th>升数</th></tr>
    <tr><td>下带</td><td>{{ out.lower_band.net_m2 }}</td><td>{{ out.lower_band.coverage }}</td><td>{{ out.lower_band.coats }}</td><td>{{ out.lower_band.liters }}</td></tr>
    <tr><td>上带</td><td>{{ out.upper_band.net_m2 }}</td><td>{{ out.upper_band.coverage }}</td><td>{{ out.upper_band.coats }}</td><td>{{ out.upper_band.liters }}</td></tr>
    <tr><td>合计</td><td>{{ out.net_m2 }}</td><td>—</td><td>—</td><td><b>{{ out.liters }}</b></td></tr>
  </table>
</template>
</div></template>
