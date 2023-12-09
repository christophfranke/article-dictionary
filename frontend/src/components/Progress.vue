<template>
  <div v-if="chartData">
    <Line :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { Line } from 'vue-chartjs';
import type { ChartData, Point } from 'chart.js';
import type { Progress } from '@/types';


const chartData = ref<ChartData<"line", (number | Point | null)[], unknown> | null>(null);
const chartOptions = ref({
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    x: {
      type: 'time',
      time: {
        unit: 'day',
        tooltipFormat: 'MMM D, YYYY',
        displayFormats: {
          day: 'MMM D',
        },
      },
      grid: {
        display: false
      },
    },
    y: {
      beginAtZero: true,
      grid: {
        display: false
      },
    },
  },
});

onMounted(async () => {
  try {
    const response = await fetch('/api/statistics/daily');
    const data = await response.json() as Progress[];

    // sort data by date
    data.sort((a: { date: string }, b: { date: string }) => new Date(a.date).getTime() - new Date(b.date).getTime());

    chartData.value = {
      labels: data.map(entry => entry.date),
      datasets: [
        // {
        //   label: 'New',
        //   backgroundColor: 'rgba(51, 153, 255)',
        //   borderColor: 'rgba(51, 153, 255)',
        //   data: data.map(entry => ({ x: Date.parse(entry.date), y: entry.new_words })),
        //   fill: false,
        // },
        {
          label: 'Seen',
          backgroundColor: 'rgba(255, 191, 128)',
          borderColor: 'rgba(255, 191, 128)',
          data: data.map(entry => ({ x: Date.parse(entry.date), y: entry.seen_words })),
          fill: false,
        },
        {
          label: 'Known',
          backgroundColor: 'rgb(51, 204, 51)',
          borderColor: 'rgb(51, 204, 51)',
          data: data.map(entry => ({ x: Date.parse(entry.date), y: entry.known_words })),
          fill: false,
        },
        // {
        //   label: 'Total Words',
        //   backgroundColor: '#a83252',
        //   borderColor: '#a83252',
        //   data: data.map(entry => ({ x: Date.parse(entry.date), y: entry.total_words })),
        //   fill: false,
        // },
      ],
    };
  } catch (error) {
    console.error('Error fetching data:', error);
  }
});
</script>
