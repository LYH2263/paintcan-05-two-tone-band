<script setup>
import { computed, onMounted, ref } from 'vue'
import { getJSON, postJSON } from '../api'
const detail = ref(null)
const out = ref(null)
const err = ref('')
const bandOn = ref(false)
const waist = ref(1.2)
const lowerCov = ref(8)
const upperCov = ref(8)
onMounted(async () => { detail.value = await getJSON('/api/rooms/2') })
const OX = 20, OY = 20, BOX_W = 360, BOX_H = 200
const scale = computed(() => {
  if (!detail.value) return 1
  const r = detail.value.room
  return Math.min(BOX_W / r.length, BOX_H / r.height)
})
const wallW = computed(() => detail.value.room.length * scale.value)
const wallH = computed(() => detail.value.room.height * scale.value)
const waistOk = computed(() => detail.value && waist.value > 0 && waist.value < detail.value.room.height)
const waistPx = computed(() => (waistOk.value ? waist.value * scale.value : 0))
const run = async () => {
  err.value = ''; out.value = null
  const body = { room_id: detail.value.room.id, persist: false }
  if (bandOn.value) body.band = { enabled: true, waist_height: waist.value, lower_coverage: lowerCov.value, upper_coverage: upperCov.value }
  try { out.value = await postJSON('/api/estimate', body) } catch (e) { err.value = e.message }
}
</script>
<template><div class="page"><h1>洞口示意（种子房间）</h1>
<ul v-if="detail"><li v-for="o in detail.openings" :key="o.id">{{ o.kind }} 扣除 {{ (o.w*o.h).toFixed(2) }} m²</li></ul>
<template v-if="detail">
<label><input type="checkbox" v-model="bandOn" /> 墙腰双色分带</label>
<fieldset v-if="bandOn"><legend>分带参数</legend>
<label>腰线离地(m) <input type="number" step="0.05" min="0" v-model.number="waist" /></label>
<label>下带涂布率(m²/L) <input type="number" step="0.5" min="0" v-model.number="lowerCov" /></label>
<label>上带涂布率(m²/L) <input type="number" step="0.5" min="0" v-model.number="upperCov" /></label>
</fieldset>
<svg :viewBox="`0 0 400 260`" class="wall" role="img" aria-label="墙面分带示意">
<rect :x="OX" :y="OY" :width="wallW" :height="wallH" fill="#fff" stroke="#3a7ca5" stroke-width="2" />
<template v-if="bandOn && waistOk">
<rect :x="OX" :y="OY + wallH - waistPx" :width="wallW" :height="waistPx" fill="#bcd9ea" />
<line :x1="OX" :x2="OX + wallW" :y1="OY + wallH - waistPx" :y2="OY + wallH - waistPx" stroke="#c0392b" stroke-width="2" stroke-dasharray="6 4" />
<text :x="OX + 6" :y="OY + wallH - waistPx - 6" class="wall-label">上带 {{ (detail.room.height - waist).toFixed(2) }} m</text>
<text :x="OX + 6" :y="OY + wallH - 8" class="wall-label">下带 {{ waist.toFixed(2) }} m</text>
<text :x="OX + wallW + 6" :y="OY + wallH - waistPx + 4" class="wall-label">腰线 {{ waist.toFixed(2) }} m</text>
</template>
</svg>
<button @click="run">试算（不存档）</button>
<p v-if="err" class="err">已拒绝：{{ err }}</p>
<template v-if="out">
<p v-if="out.band">下带 {{ out.band.lower.net_m2 }} m² → {{ out.band.lower.liters }} 升 · 上带 {{ out.band.upper.net_m2 }} m² → {{ out.band.upper.liters }} 升 · 合计 <span class="hero-num">{{ out.band.total_liters }} L</span></p>
<p v-else>净 {{ out.net_m2 }} m² · {{ out.liters }} 升 · {{ out.coats }} 遍</p>
</template>
</template>
</div></template>
