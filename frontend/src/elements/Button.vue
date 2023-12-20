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
@import "@/style/global.scss";

button {
  color: #fff;
  padding: 10px 20px;
  font-size: $button-font-size;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  font-weight: normal;

  &.small {
    padding: 5px 5px;
    font-size: $button-small-font-size;
  }

  &.view {
    background-color: $button-view-color;
    &:hover {
      background-color: $button-view-hover-color;
    }
  }

  &.action {
    background-color: $button-action-color;
    &:hover {
      background-color: $button-action-hover-color;
    }
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
}
</style>