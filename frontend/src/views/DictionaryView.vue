<template>
  <div>
    <h1>Dictionary View</h1>
    <button @click="resetDictionary">Reset</button>
    <table>
      <thead>
        <tr>
          <th @click="sortTable('original')">Original</th>
          <th @click="sortTable('translated')">Translated</th>
          <th @click="sortTable('status')">Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(word, index) in sortedWords" :key="index">
          <td>{{ word.original }}</td>
          <td>{{ word.translated }}</td>
          <td>{{ word.status }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';

const words = ref([]);
const sortOrder = ref('asc');
const sortedBy = ref('');

const resetDictionary = async () => {
  await fetch('/api/dictionary/reset', { method: 'POST' });
  loadDictionary();
};

const sortTable = (column) => {
  if (column === sortedBy.value) {
    // Toggle the sorting order if clicking on the same column
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc';
  } else {
    // Sort the table by the selected column
    sortedBy.value = column;
    sortOrder.value = 'asc';
  }
};

const loadDictionary = async () => {
  const response = await fetch('/api/dictionary/');
  words.value = await response.json();
};

const sortedWords = computed(() => {
  const sorted = [...words.value];
  if (sortedBy.value) {
    sorted.sort((a, b) => {
      const order = sortOrder.value === 'asc' ? 1 : -1;
      return a[sortedBy.value] > b[sortedBy.value] ? order : -order;
    });
  }
  return sorted;
});

onMounted(() => {
  loadDictionary();
});
</script>
