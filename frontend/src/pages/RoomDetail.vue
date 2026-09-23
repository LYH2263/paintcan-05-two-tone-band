<script setup>
import { onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { getJSON, postJSON } from '../api'
const route = useRoute()
const detail = ref(null)
const est = ref(null)
const err = ref('')
const band = ref(false)
const waist_height = ref(1.0)
const lower_coverage = ref(6)
const lower_coats = ref(2)
const upper_coverage = ref(10)
const upper_coats = ref(2)
const load = async () => {
  detail.value = await getJSON(`/api/rooms/${route.params.id}`)
  await run()
}
const run = async () => {
  err.value = ''
  try {
    est.value = await postJSON('/api/estimate', {
      room_id: +route.params.id, persist: false,
      band: band.value, waist_height: waist_height.value,
      lower_coverage: lower_coverage.value, lower_coats: lower_coats.value,
      upper_coverage: upper_coverage.value, upper_coats: upper_coats.value,
    })
  } catch (e) { err.value = String(e); est.value = null }
}
onMounted(load); watch(() => route.params.id, load)
</script>
<template><div class="page" v-if="detail"><h1>{{ detail.room.name }}</h1>
<label><input type="checkbox" v-model="band" @change="run" /> 墙腰双色分带</label>
<fieldset v-if="band" class="band-box">
  <label>腰线离地(m) <input type="number" step="0.05" v-model.number="waist_height" @change="run" /></label>
  <label>下带涂布率 <input type="number" step="0.5" v-model.number="lower_coverage" @change="run" /></label>
  <label>下带遍数 <input type="number" step="1" v-model.number="lower_coats" @change="run" /></label>
  <label>上带涂布率 <input type="number" step="0.5" v-model.number="upper_coverage" @change="run" /></label>
  <label>上带遍数 <input type="number" step="1" v-model.number="upper_coats" @change="run" /></label>
</fieldset>
<p v-if="err" class="err">{{ err }}</p>
<template v-if="est && !est.band">
  <p>净面积 {{ est.net_m2 }} m² · 需漆 <span class="hero-num">{{ est.liters }} L</span></p>
</template>
<template v-if="est && est.band">
  <p>净面积 {{ est.net_m2 }} m² · 腰线 {{ est.waist_height }} m · 合计 <span class="hero-num">{{ est.liters }} L</span></p>
  <table>
    <tr><th>带</th><th>净面积 m²</th><th>涂布率</th><th>遍数</th><th>升数</th></tr>
    <tr><td>下带</td><td>{{ est.lower_band.net_m2 }}</td><td>{{ est.lower_band.coverage }}</td><td>{{ est.lower_band.coats }}</td><td>{{ est.lower_band.liters }}</td></tr>
    <tr><td>上带</td><td>{{ est.upper_band.net_m2 }}</td><td>{{ est.upper_band.coverage }}</td><td>{{ est.upper_band.coats }}</td><td>{{ est.upper_band.liters }}</td></tr>
  </table>
</template>
<ul><li v-for="o in detail.openings" :key="o.id">{{ o.kind }} {{ o.w }}×{{ o.h }}</li></ul>
</div></template>
