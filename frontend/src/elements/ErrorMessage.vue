<script setup lang="ts">
const { message } = defineProps(['message']);
</script>
<template>
	<p v-if="message" class="error-message">{{ message }}</p>
</template>

<style scoped lang="scss">
p {
  color: #721c24;
  background-color: #f8d7da;
  border: 1px solid #f5c6cb;
  padding: 10px;
  border-radius: 4px;
}
</style>