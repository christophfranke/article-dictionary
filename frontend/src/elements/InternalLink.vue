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
@import "@/style/global.scss";

a {	
  display: block;
  color: $internal-link-color;
  text-decoration: none;
  font-size: 14px;
  font-weight: normal;

  &:hover {
	  text-decoration: underline;
  }
}

</style>