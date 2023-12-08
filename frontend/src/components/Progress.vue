<template>
	<div>
		<Line :data="data" :options="options" />
	</div>
</template>

<script setup lang="ts">
import { Line } from 'vue-chartjs'

const data = {
  labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
  datasets: [
    {
      label: 'Data One',
      backgroundColor: '#f87979',
      data: [40, 39, 10, 40, 39, 80, 40]
    },
    {
      label: 'Data Two',
      backgroundColor: '#12aacc',
      data: [45, 3, 1, 20, 50, 88, 46]
    }
  ]
}

const options = {
  responsive: true,
  maintainAspectRatio: false,
	scales: {
	   x: {
	      grid: {
	         display: false
	      }
	   },
	   y: {
	      grid: {
	         display: false
	      }
	   }
	}
}
</script>