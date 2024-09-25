<script setup lang="ts">
import { ref, watch } from 'vue';

const props = defineProps({
    modelValue: [String, Boolean]
});

const emit = defineEmits(['update:modelValue', 'change']);

// Reactive reference for the input value
const valueRef = ref(props.modelValue);

// Watch for external changes to modelValue and update valueRef accordingly
watch(() => props.modelValue, (newVal) => {
    valueRef.value = newVal;
});

// Watch for changes in valueRef and emit update event
watch(valueRef, (newValue) => {
    emit('update:modelValue', newValue);
    emit('change', newValue)
});
</script>

<template>
    <input v-bind="$attrs" v-model="valueRef" />
</template>

<style scoped lang="scss">
@import "@/style/global.scss";

input {
  color: inherit;
  background-color: inherit;
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: 1px solid $border-color;
  border-radius: 4px;
  box-sizing: border-box;

  &:disabled {
    opacity: 0.5;
  }
}
</style>
