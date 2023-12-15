<script setup lang="ts">
import Headline from '@/elements/Headline.vue';
import InternalLink from '@/elements/InternalLink.vue';


</script>

<template>
  <div class="container">
    <Headline>404 - Not Found</Headline>
    <p>The page you are looking for does not exist.</p>
    <InternalLink to="/" class="link">Back to home page</InternalLink>
  </div>
</template>

<style scoped lang="scss">
.container {
  margin: 100px auto 0;
  max-width: 400px;
  text-align: center;
}

p {
  margin: 20px 0;
}

.link {
  margin-top: 50px;
  font-size: 20px;
}
</style>