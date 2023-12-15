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
  display: block;
  color: #007bff;
  text-decoration: none;
  font-size: 14px;

  &:hover {
	  text-decoration: underline;
  }
}

</style>