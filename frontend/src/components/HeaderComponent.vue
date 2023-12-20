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

<style scoped lang="scss">
@import '@/style/global.scss';

header {
  background-color: $header-background-color;
  color: $header-font-color;
  padding: 10px 0;
  font-weight: normal;
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

a, a:visited {
  padding: 5px 10px;
  border-radius: 5px;
  transition: background-color 0.3s ease;
  color: $header-font-color;
  text-decoration: none;
}

a:hover {
  background-color: $header-hover-color;
}

.profile-link {
	margin-left: auto;
}
</style>
