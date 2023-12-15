<template>
	<form class="form">
		<slot />
	</form>
</template>

<style scoped lang="scss">
form {
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
}
</style>