<template>
    <RouterLink :to="profile.isLoggedIn ? '/profile' : '/login'">
        {{ profile.isLoggedIn ? (profile.name || profile.email) : __('Login') }}
    </RouterLink>
</template>


<script setup lang="ts">
import { useUser } from '@/use/user';
import __ from '@/i18n'

const { profile } = useUser();
</script>
