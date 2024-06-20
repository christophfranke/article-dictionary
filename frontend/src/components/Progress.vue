<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue';
import { Line } from 'vue-chartjs';
import type { ChartData, Point, ChartOptions } from 'chart.js';
import type { Progress } from '@/types';
import useApi from '@/use/api';

import Button from '@/elements/Button.vue';
import Headline from '@/elements/Headline.vue';
import __ from '@/i18n'


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
const showClusterData = ref(true);
const toggleClusterData = () => showClusterData.value = !showClusterData.value;

const selectedData = ref<string>('week')
const selectedDataValues = ['week', 'month'];
const toggleSelectedData = () => {
  const currentIndex = selectedDataValues.indexOf(selectedData.value);
  const nextIndex = (currentIndex + 1) % selectedDataValues.length;
  selectedData.value = selectedDataValues[nextIndex];
}

const selectedDataDisplay = computed(() => ({
  week: __('This Week'),
  month: __('This Month'),
  year: __('This Year'),
}[selectedData.value]) ?? 'All');

let lastData: ChartData<"line", Point[], unknown> | null = null;
const processedChartData = computed<ChartData<"line", Point[], unknown> | null>(() => {
  if (!chartData.value)
    return lastData;

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

    lastData = result;
    return lastData;
  }

  lastData = {
    ...chartData.value,
    datasets: chartData.value.datasets.map(dataset => ({
      ...dataset,
      data: dataset.data.map((point: DataPoint) => ({
        x: point.x,
        y: showClusterData.value ? point.cluster : point.word
      })).filter((point: DataPoint, index: number) => index > 0)
    })),
  }
  return lastData;
});

const rawData = ref<{ [key: string]: ChartData<any> }>({});
const chartData = computed(() => rawData.value[selectedData.value]);
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
        color: 'rgba(127, 127, 127, 0.1)'
      },
    },
  },
}));

const hasEnoughData = computed(() => {
  if (!chartData.value?.labels)
    return false;

  return chartData.value.labels.length > 1;
});

const { fetchAuthorized } = useApi();
const isLoading = ref<boolean>(true)
const fetchData = async (dataType: string) => {
  isLoading.value = true
  const data = await fetchAuthorized<Progress[]>(`/api/statistics/${dataType}`);
  isLoading.value = false

  if (data && data.length > 1) {
    // sort data by date
    data.sort((a: { date: string }, b: { date: string }) => new Date(a.date).getTime() - new Date(b.date).getTime());

    return {
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
}

watch(selectedData, async (newValue: string) => {
  if (!rawData.value[newValue]) {
    const result = await fetchData(newValue);
    if (result) {
      rawData.value[newValue] = result;
    }
  }
}, { immediate: true });
</script>

<template>
  <div :class="{ 'chart-container': true, disabled: !hasEnoughData }" v-if="hasEnoughData || isLoading">
    <div class="chart-toggle">
      <Headline type="h2">{{ __('Progress') }}</Headline>
      <div class="buttons">
        <Button @click="toggleClusterData" role="view">
          {{ showClusterData ? __('Word cluster') : __('Words') }}
        </Button>
        <Button @click="toggleRelativeData" role="view">
          {{ showRelativeData ? __('New') : __('Total') }}
        </Button>
        <Button @click="toggleSelectedData" role="view">
          {{ selectedDataDisplay }}
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
  transition: opacity 0.3s ease-in-out;

  &.disabled {
    opacity: 0.5;
    pointer-events: none;
    cursor: default;
  }
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
