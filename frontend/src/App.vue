<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import HeaderComponent from '@/components/HeaderComponent.vue'

</script>

<template>
  <div>
    <HeaderComponent />
    <RouterView />
  </div>
</template>

<style>
body {
  font-family: 'Helvetica Neue', 'Arial', sans-serif;
  font-size: 16px;
  margin: 0;
  padding: 0 0 50px 0;
  box-sizing: border-box;
}
a, a:visited {
  text-decoration: none;
}

p, h1, h2, h3, h4, h5, h6 {
  margin: 0;
}

</style>
