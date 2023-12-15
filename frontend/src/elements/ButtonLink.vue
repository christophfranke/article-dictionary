<script setup lang="ts">
import { RouterLink } from 'vue-router';
import Button from '@/elements/Button.vue';

</script>

<template>
	<RouterLink>
		<Button class="button"><slot /></Button>
	</RouterLink>
</template>

<style scoped lang="scss">
.button {
  width: 100%;
}
</style>
