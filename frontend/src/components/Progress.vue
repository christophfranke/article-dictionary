<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { Line } from 'vue-chartjs';
import type { ChartData, Point } from 'chart.js';
import type { Progress } from '@/types';
import { useFetchAuthorized } from '@/use/api';


import 'chartjs-adapter-moment';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  TimeScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  TimeScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
)


const showRelativeData = ref(false);
const toggleRelativeData = () => showRelativeData.value = !showRelativeData.value;
const processedChartData = computed(() => {
  if (!chartData.value)
    return null

  if (showRelativeData.value) {
    return {
      ...chartData.value,
      datasets: chartData.value.datasets.map(dataset => ({
        ...dataset,
        data: dataset.data.map((point, index) => {
          if (index === 0)
            return {
              x: point.x,
              y: 0,
            };

          const previous = dataset.data[index - 1];
          if (previous === null || point === null)
            return null;

          return {
            x: point.x,
            y: point.y - previous.y,
          }
        })
      }))
    }
  }

  return chartData.value;
});


const chartData = ref<ChartData<"line", Point[], unknown> | null>(null);
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

const fetchAuthorized = useFetchAuthorized();
onMounted(async () => {
  const data = await fetchAuthorized<Progress[]>('/api/statistics/daily');

  if (data) {      
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
          backgroundColor: 'rgb(255, 191, 128)',
          borderColor: 'rgb(255, 191, 128)',
          data: data.map(entry => ({ x: Date.parse(entry.date), y: entry.seen_words })),
          fill: false,
        },
        {
          label: 'Known',
          backgroundColor: '#a83252',
          borderColor: '#a83252',
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
  }
});
</script>
<template>
  <div class="chart-container">
    <div class="chart-toggle">
      <button @click="toggleRelativeData" class="toggle-button">
        {{ showRelativeData ? 'New words' : 'Total words'}}
      </button>
    </div>
    <div v-if="processedChartData" class="chart">
      <Line :data="processedChartData" :options="chartOptions" />
    </div>
  </div>
</template>

<style scoped>
.chart-container {
  margin: 20px auto;
  max-width: 800px; /* Set a maximum width for the chart if needed */
}

.chart-toggle {
  margin-bottom: 10px; /* Add margin below the toggle button */
  text-align: right;
}

.toggle-button {
  background-color: #007bff;
  color: #fff;
  padding: 10px 20px;
  font-size: 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.toggle-button:hover {
  background-color: #0056b3;
}

.chart {
}
</style>
