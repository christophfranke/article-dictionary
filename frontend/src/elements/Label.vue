<template>
	<label>
		<slot />
	</label>
</template>

<style scoped lang="scss">
@import "@/style/global.scss";

label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
  color: $label-color;
}
</style>	