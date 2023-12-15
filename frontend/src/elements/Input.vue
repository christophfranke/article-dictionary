<script setup lang="ts">
import { ref, watch } from 'vue';

const { modelValue } = defineProps(['modelValue']);
const emit = defineEmits(['update:modelValue']);

const valueRef = ref(modelValue);
watch(valueRef, (newValue) => {
  emit('update:modelValue', newValue);
});
</script>

<template>
  <input v-bind="$attrs" v-model="valueRef" />
</template>

<style scoped lang="scss">
input {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}
</style>
