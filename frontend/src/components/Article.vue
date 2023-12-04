<template>
  <div>
    <!-- Your article display logic goes here -->
    <p>{{ data.title }}</p>
    <p>{{ data.content }}</p>
    <!-- Add more details as needed -->
  </div>
</template>

<script setup lang="ts">
const props = defineProps(['data']);
</script>
