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
  font-family: 'Helvetica Neue', Arial, sans-serif;
  font-size: 16px;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
a, a:visited {
  text-decoration: none;
}
</style>
