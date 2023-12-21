<template>
	<RouterLink :to="profile.isLoggedIn ? '/profile' : '/login'">
		{{ profile.isLoggedIn ? (profile.name || profile.email) : 'Login' }}
	</RouterLink>
</template>

<script setup lang="ts">
import { useUser } from '@/use/user';

const { profile } = useUser();
</script>
