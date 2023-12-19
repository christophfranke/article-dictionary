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
  <textarea v-bind="$attrs" v-model="valueRef" />
</template>

<style scoped lang="scss">
@import "@/style/global.scss";

textarea {
  color: inherit;
  background-color: inherit;
  width: 100%;
  padding: 10px;
  border: 1px solid $border-color;
  border-radius: 4px;
  box-sizing: border-box;
  resize: vertical;
  min-height: 300px;
}
</style>
