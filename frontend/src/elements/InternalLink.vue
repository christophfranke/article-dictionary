<script setup lang="ts">
import { RouterLink } from 'vue-router';

const { to } = defineProps({
  to: {
    type: String,
    required: true,
  },
});

</script>

<template>
	<RouterLink :to="to">
		<slot />
	</RouterLink>
</template>

<style scoped lang="scss">
a {	
  display: block;
  color: #007bff;
  text-decoration: none;
  font-size: 14px;

  &:hover {
	  text-decoration: underline;
  }
}

</style>