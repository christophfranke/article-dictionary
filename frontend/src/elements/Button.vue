<script setup lang="ts">
import { computed } from 'vue';
const { role, size } = defineProps({
  role: {
    type: String,
    default: 'action',
  },
  size: {
    type: String,
    default: 'default',
  },
});

</script>

<template>
	<button :class="{ [role]: true, [size]: true }">
		<slot />
	</button>
</template>

<style scoped lang="scss">
button {
  color: #fff;
  padding: 10px 20px;
  font-size: 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;

  &.small {
    padding: 5px 5px;
    font-size: 16px;
  }

  &.view {
    background-color: #007bff;
    &:hover {
      background-color: #0056b3;
    }
  }

  &.action {
    background-color: #4caf50; /* Green background */
    &:hover {
      background-color: #45a049;
    }
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
}
</style>