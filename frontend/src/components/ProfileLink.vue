<template>
	<RouterLink :to="isLoggedIn ? '/profile' : '/login'">
		{{ isLoggedIn ? name : 'Login' }}
	</RouterLink>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';

const loading = ref(true);
const isLoggedIn = ref(false);
const name = ref('');

const route = useRoute();

onMounted(async () => {
  try {
    const response = await fetch('/api/profile/preview');
    const data = await response.json();

    isLoggedIn.value = data.isLoggedIn;
    name.value = data.name;
  } catch (error) {
    console.error('Error fetching profile preview:', error);
  } finally {
    loading.value = false;
  }
});
</script>
