<template>
  <div>
    <router-link :to="data.url">
      <h2>{{ data.title }}</h2>
      <p>{{ data.excerpt }}...</p>
    </router-link>
  </div>
</template>

<script setup lang="ts">
const props = defineProps(['data']);
</script>
