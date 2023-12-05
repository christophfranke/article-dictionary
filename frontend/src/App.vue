<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div>
    <header>
      <div class="wrapper">
        <nav>
          <RouterLink to="/">Home</RouterLink>
          <RouterLink to="/dictionary">Dictionary</RouterLink>
        </nav>
      </div>
    </header>

    <RouterView />
  </div>
</template>

<style>
body {
  font-family: 'Helvetica Neue', Arial, sans-serif;
  font-size: 16px;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

header {
  background-color: #333;
  color: #fff;
  padding: 10px 0;
}

.wrapper {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

nav {
  display: flex;
  justify-content: space-between;
}

a, a:visited {
  color: #fff;
  text-decoration: none;
  padding: 5px 10px;
  border-radius: 5px;
  transition: background-color 0.3s ease;
}

a:hover {
  background-color: #555;
}
</style>
