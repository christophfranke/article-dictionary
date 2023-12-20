<template>
	<p>
		<slot />
	</p>
</template>

<style scoped lang="scss">
@import "@/style/global.scss";

p {
  color: $excerpt-color;
  line-height: 1.4;	
  font-weight: $font-weight;
}	
</style>