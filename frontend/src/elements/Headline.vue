<script setup lang="ts">
const { type } = defineProps({
	type: {
		type: String,
		default: 'h1',
	},
});
</script>

<template>
	<h1 v-if="type === 'h1'">
		<slot />
	</h1>
	<h2 v-else>
		<slot />
	</h2>
</template>

<style scoped lang="scss">
h1 {
	margin: 0;
  color: #333;
  font-size: 32px;
}
h2 {
	margin: 0;
  color: #333;
  font-size: 24px;
}
</style>