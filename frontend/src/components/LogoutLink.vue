<template>
    <a href="#" @click="logoutAndRedirect" v-if="profile.isLoggedIn">{{ __('Logout') }}</a>
</template>


<script setup lang="ts">
import { useUser, useLogout } from '@/use/user';
import { useRouter } from 'vue-router';
import __ from '@/i18n'

const router = useRouter();
const { profile } = useUser();
const logout = useLogout();

const logoutAndRedirect = async () => {
  if (await logout()) {
    router.push('/login');
  }
}
</script>