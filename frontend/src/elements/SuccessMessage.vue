<script setup lang="ts">
const { message } = defineProps(['message']);
</script>
<template>
    <p v-if="message" class="success-message">{{ message }}</p>
</template>

<style scoped lang="scss">
@import "@/style/global.scss";

p {
  color: $success-font-color;
  background-color: $success-background-color;
  border: 1px solid $success-border-color;
  padding: 10px;
  border-radius: 4px;
}
</style>