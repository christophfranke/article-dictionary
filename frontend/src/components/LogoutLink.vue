<template>
	<a href="#" @click="logoutAndRedirect" v-if="user.isLoggedIn.value">Logout</a>
</template>

<script setup lang="ts">
import { useUser, useLogout } from '@/use/user';
import { useRouter } from 'vue-router';

const router = useRouter();
const user = useUser();
const logout = useLogout();

const logoutAndRedirect = async () => {
  if (await logout()) {
    router.push('/login');
  }
}
</script>