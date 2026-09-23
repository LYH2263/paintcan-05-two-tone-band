<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, postJSON } from '../api'
const rooms = ref([])
const room_id = ref(1)
const out = ref(null)
const err = ref('')
const bandOn = ref(false)
const waist = ref(1.2)
const lowerCov = ref(8)
const upperCov = ref(8)
onMounted(async () => { rooms.value = (await getJSON('/api/rooms')).items })
const run = async () => {
  err.value = ''; out.value = null
  const body = { room_id: room_id.value, persist: true }
  if (bandOn.value) body.band = { enabled: true, waist_height: waist.value, lower_coverage: lowerCov.value, upper_coverage: upperCov.value }
  try { out.value = await postJSON('/api/estimate', body) } catch (e) { err.value = e.message }
}
</script>
<template><div class="page"><h1>估漆工作台</h1>
<label>房间 <select v-model.number="room_id"><option v-for="r in rooms" :key="r.id" :value="r.id">{{ r.name }}</option></select></label>
<label><input type="checkbox" v-model="bandOn" /> 墙腰双色分带</label>
<fieldset v-if="bandOn"><legend>分带参数</legend>
<label>腰线离地(m) <input type="number" step="0.05" min="0" v-model.number="waist" /></label>
<label>下带涂布率(m²/L) <input type="number" step="0.5" min="0" v-model.number="lowerCov" /></label>
<label>上带涂布率(m²/L) <input type="number" step="0.5" min="0" v-model.number="upperCov" /></label>
</fieldset>
<button @click="run">估算</button>
<p v-if="err" class="err">已拒绝：{{ err }}</p>
<template v-if="out">
<p v-if="out.band">净 {{ out.net_m2 }} m² · 下带 {{ out.band.lower.liters }} 升 · 上带 {{ out.band.upper.liters }} 升 · 合计 <span class="hero-num">{{ out.band.total_liters }} L</span></p>
<p v-else>净 {{ out.net_m2 }} m² · {{ out.liters }} 升 · {{ out.coats }} 遍</p>
</template></div></template>
