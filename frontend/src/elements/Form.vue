<template>
	<form class="form">
		<slot />
	</form>
</template>

<style scoped lang="scss">
@import "@/style/global.scss";

form {
  background-color: $form-background-color;
  border: 1px solid $border-color;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
}
</style>