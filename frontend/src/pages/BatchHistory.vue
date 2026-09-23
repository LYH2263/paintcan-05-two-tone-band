<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
const items = ref([])
onMounted(async () => { items.value = (await getJSON('/api/history')).items })
</script>
<template><div class="page"><h1>估算记录</h1>
<table>
  <tr><th>#</th><th>时间</th><th>房间</th><th>分带</th><th>钉选参数</th><th>升数</th></tr>
  <tr v-for="h in items" :key="h.id">
    <td>#{{ h.id }}</td><td>{{ h.created_at }}</td><td>{{ h.room_id }}</td>
    <template v-if="h.result && h.result.band">
      <td>腰线 {{ h.result.waist_height }} m</td>
      <td>
        下带 {{ h.input.lower_band.coverage }} m²/L × {{ h.input.lower_band.coats }} 遍 → {{ h.result.lower_band.liters }} L<br/>
        上带 {{ h.input.upper_band.coverage }} m²/L × {{ h.input.upper_band.coats }} 遍 → {{ h.result.upper_band.liters }} L
      </td>
      <td><b>{{ h.result.liters }} L</b></td>
    </template>
    <template v-else-if="h.result">
      <td>关</td>
      <td>{{ h.input && h.input.coverage != null ? h.input.coverage + ' m²/L × ' + h.input.coats + ' 遍' : '—' }}</td>
      <td><b>{{ h.result.liters }} L</b></td>
    </template>
    <template v-else><td colspan="3">—</td></template>
  </tr>
</table>
</div></template>
