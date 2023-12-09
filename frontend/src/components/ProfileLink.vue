<template>
	<RouterLink :to="user.isLoggedIn.value ? '/profile' : '/login'">
		{{ user.isLoggedIn.value ? user.name.value : 'Login' }}
	</RouterLink>
</template>

<script setup lang="ts">
import { useUser } from '@/use/user';

const user = useUser();
</script>
