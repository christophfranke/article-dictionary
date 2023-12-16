<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { Line } from 'vue-chartjs';
import type { ChartData, Point, ChartOptions } from 'chart.js';
import type { Progress } from '@/types';
import { useFetchAuthorized } from '@/use/api';

import Button from '@/elements/Button.vue';
import Headline from '@/elements/Headline.vue';


import 'chartjs-adapter-moment';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  LogarithmicScale,
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
  LogarithmicScale,
  TimeScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
)

type DataPoint = {
  x: string;
  word: number;
  cluster: number;
}


const showRelativeData = ref(false);
const toggleRelativeData = () => showRelativeData.value = !showRelativeData.value;
const showClusterData = ref(false);
const toggleClusterData = () => showClusterData.value = !showClusterData.value;
const processedChartData = computed<ChartData<"line", Point[], unknown> | null>(() => {
  if (!chartData.value)
    return null

  if (showRelativeData.value) {
    const result = {
      ...chartData.value,
      datasets: chartData.value.datasets.map(dataset => ({
        ...dataset,
        data: dataset.data
          .map((point: DataPoint) => ({
            x: point.x,
            y: showClusterData.value ? point.cluster : point.word
          })).map((point: Point, index: number, array: Point[]) => {
            if (index === 0)
              return {
                x: point.x,
                y: 0,
              };

            const previous = array[index - 1];
            if (previous === null || point === null)
              return null;

            return {
              x: point.x,
              y: Math.max(0, point.y - previous.y),
            }
          }).filter((point: Point, index: number) => index > 0)
      }))
    }

    return result
  }

  return {
    ...chartData.value,
    datasets: chartData.value.datasets.map(dataset => ({
      ...dataset,
      data: dataset.data.map((point: DataPoint) => ({
        x: point.x,
        y: showClusterData.value ? point.cluster : point.word
      })).filter((point: DataPoint, index: number) => index > 0)
    })),
  }
});


const chartData = ref<ChartData<any> | null>(null);
// It would have been nice to put ChartOptions here, but it errors like crazy
const chartOptions = computed<any>(() => ({
  responsive: true,
  maintainAspectRatio: false,
  aspectRatio: 1.5,
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
        display: false,
      },
    },
    y: {
      beginAtZero: true,
      type: showRelativeData.value ? 'linear': 'logarithmic',
      grid: {
        display: true,
        drawOnChartArea: true,
        color: '#f3f3f3'
      },
    },
  },
}));

const hasEnoughData = computed(() => {
  if (!chartData.value?.labels)
    return false;

  return chartData.value.labels.length > 1;
});



const fetchAuthorized = useFetchAuthorized();
onMounted(async () => {
  const data = await fetchAuthorized<Progress[]>('/api/statistics/daily');

  if (data) {      
    // sort data by date
    data.sort((a: { date: string }, b: { date: string }) => new Date(a.date).getTime() - new Date(b.date).getTime());

    chartData.value = {
      labels: data.map(entry => entry.date).filter((date, index) => index > 0),
      datasets: [
        {
          label: 'Known',
          backgroundColor: '#a83252',
          borderColor: '#a83252',
          data: data.map(entry => ({
            x: Date.parse(entry.date),
            word: entry.known_words,
            cluster: entry.known_cluster || 0,
          })),
          fill: false,
        },
        {
          label: 'Seen',
          backgroundColor: 'rgb(255, 191, 128)',
          borderColor: 'rgb(255, 191, 128)',
          data: data.map(entry => ({
            x: Date.parse(entry.date),
            word: entry.known_words + entry.seen_words,
            cluster: (entry.known_cluster || 0) + (entry.seen_cluster || 0),
          })),
          fill: false,
        },
        {
          label: 'All',
          backgroundColor: 'rgb(51, 153, 255)',
          borderColor: 'rgb(51, 153, 255)',
          data: data.map(entry => ({
            x: Date.parse(entry.date),
            word: entry.new_words + entry.known_words + entry.seen_words,
            cluster: (entry.new_cluster || 0) + (entry.known_cluster || 0) + (entry.seen_cluster || 0),
          })),
          fill: false,
        },
      ],
    };
  }
});
</script>
<template>
  <div class="chart-container" v-if="hasEnoughData">
    <div class="chart-toggle">
      <Headline type="h2">Progress</Headline>
      <div class="buttons">
        <Button @click="toggleClusterData" role="view">
          {{ showClusterData ? 'Word groups' : 'Words'}}
        </Button>
        <Button @click="toggleRelativeData" role="view">
          {{ showRelativeData ? 'Per Day' : 'Overall'}}
        </Button>
      </div>
    </div>
    <div v-if="processedChartData" class="chart">
      <Line :data="processedChartData" :options="chartOptions" />
    </div>
  </div>
</template>

<style scoped lang="scss">
.chart-container {
  margin: 0 auto;
  margin-bottom: 50px;
  max-width: 800px; /* Set a maximum width for the chart if needed */
}

.chart-toggle {
  margin-bottom: 10px; /* Add margin below the toggle button */
  display: flex;
  justify-content: space-between;
  align-items: baseline;
}

.buttons {
  margin-left: auto;
  button {
    margin-left: 10px;
  }
}

</style>
