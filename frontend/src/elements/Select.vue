<script setup lang="ts">
import { ref, watch } from 'vue';
import type { PropType } from 'vue';

const { options, modelValue } = defineProps({
	options: {
		type: Object as PropType<{ [key: string]: string } | null>,
		default: {},
	},
	modelValue: {
		type: String,
		default: '',
	},
})

const emit = defineEmits(['update:modelValue']);

const valueRef = ref(modelValue);
watch(valueRef, (newValue) => {
  emit('update:modelValue', newValue);
});

</script>
<template>
	<select v-if="options" v-model="valueRef">
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