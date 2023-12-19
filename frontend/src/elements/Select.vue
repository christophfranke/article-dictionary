<script setup lang="ts">
import { ref, watch } from 'vue';
import type { PropType } from 'vue';

const props = defineProps({
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

const valueRef = ref(props.modelValue);
watch(valueRef, (newValue) => {
  emit('update:modelValue', newValue);
});

// Watch for external changes to modelValue and update valueRef accordingly
watch(() => props.modelValue, (newVal) => {
  valueRef.value = newVal;
});

</script>
<template>
	<select v-if="props.options" v-model="valueRef">
		<option v-for="(label, value) in props.options" :key="value" :value="value">{{ label }}</option>
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