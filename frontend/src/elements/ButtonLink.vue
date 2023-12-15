<script setup lang="ts">
import { RouterLink } from 'vue-router';
import Button from '@/elements/Button.vue';

const { to } = defineProps({
  to: {
    type: String,
    required: true,
  },
});
</script>

<template>
	<RouterLink :to="to">
		<Button class="button"><slot /></Button>
	</RouterLink>
</template>

<style scoped lang="scss">
.button {
  width: 100%;
}
</style>
