<script setup lang="ts">
const { message } = defineProps(['message']);
</script>
<template>
    <p v-if="message" class="error-message">{{ message }}</p>
</template>

<style scoped lang="scss">
@import "@/style/global.scss";

p {
  color: $error-font-color;
  background-color: $error-background-color;
  border: 1px solid $error-border-color;
  padding: 10px;
  border-radius: 4px;
}
</style>