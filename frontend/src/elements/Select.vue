<script setup lang="ts">
import type { PropType } from 'vue';

const { options } = defineProps({
	options: {
		type: Object as PropType<{ [key: string]: string } | null>,
		default: {},
	},
})

</script>
<template>
	<select v-if="options">
		<option v-for="(label, value) in options" :key="value" :value="value">{{ label }}</option>
		<slot />
	</select>
</template>

<style scoped lang="scss">
select {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}
</style>