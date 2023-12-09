<script setup lang="ts">
import ProfileLink from './ProfileLink.vue';
import LogoutLink from './LogoutLink.vue';
</script>

<template>
  <header>
    <div class="wrapper">
      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/articles">Articles</RouterLink>
        <RouterLink to="/dictionary">Dictionary</RouterLink>
        <ProfileLink class="profile-link" />
        <LogoutLink />
      </nav>
    </div>
  </header>
</template>

<style scoped>
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
  justify-content: flex-start;
}

nav a {  
  padding: 5px 10px;
  border-radius: 5px;
  transition: background-color 0.3s ease;
}

a:hover {
  background-color: #555;
}

.profile-link {
	margin-left: auto;
}
</style>
