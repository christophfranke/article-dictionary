<script setup lang="ts">
import { RouterLink } from 'vue-router';

</script>

<template>
	<RouterLink to="/register">
		<slot />
	</RouterLink>
</template>

<style scoped lang="scss">
a {	
  color: #007bff;
  text-decoration: none;

  &:hover {
	  text-decoration: underline;
  }
}

</style>