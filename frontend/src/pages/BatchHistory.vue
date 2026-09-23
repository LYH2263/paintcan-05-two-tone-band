<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
const items = ref([])
const parse = (h) => {
  let inp = {}, res = {}
  try { inp = JSON.parse(h.input_json || '{}') } catch { /* keep {} */ }
  try { res = JSON.parse(h.result_json || '{}') } catch { /* keep {} */ }
  return { ...h, inp, res }
}
onMounted(async () => { items.value = (await getJSON('/api/history')).items.map(parse) })
</script>
<template><div class="page"><h1>估算记录</h1>
<table>
<tr><th>#</th><th>时间</th><th>房间</th><th>净面积</th><th>合计升数</th><th>分带钉选</th></tr>
<tr v-for="h in items" :key="h.id">
<td>#{{ h.id }}</td><td>{{ h.created_at }}</td><td>{{ h.room_id }}</td>
<td>{{ h.res.net_m2 }} m²</td><td>{{ h.res.liters }} L</td>
<td v-if="h.res.band">腰线 {{ h.res.band.waist_height }} m ·
下带 {{ h.res.band.lower.liters }} L @{{ h.res.band.lower.coverage }} m²/L ·
上带 {{ h.res.band.upper.liters }} L @{{ h.res.band.upper.coverage }} m²/L ·
合计 {{ h.res.band.total_liters }} L</td>
<td v-else>未分带 · @{{ h.inp.coverage ?? h.res.coverage }} m²/L · {{ h.res.coats }} 遍</td>
</tr>
</table></div></template>
