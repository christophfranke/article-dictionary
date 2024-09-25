<script setup lang="ts">
import { ref } from 'vue'
import { profile } from '@/use/user';
import ProfileLink from './ProfileLink.vue';
import LogoutLink from './LogoutLink.vue';
import Select from '@/elements/Select.vue';
import { default as __, supportedLanguages } from '@/i18n'

const lang = ref<string>('en')
</script>

<template>
    <header>
        <div class="wrapper">
            <nav v-if="profile.isLoggedIn">
                <RouterLink to="/home">{{ __('Home') }}</RouterLink>
                <RouterLink to="/articles">{{ __('Articles') }}</RouterLink>
                <RouterLink to="/dictionary">{{ __('Dictionary') }}</RouterLink>
                <RouterLink to="/dictionary/review">{{ __('Review') }}</RouterLink>
                <RouterLink to="/">{{ __('Introduction') }}</RouterLink>
                <ProfileLink class="profile-link" />
                <LogoutLink />
            </nav>
            <nav v-else>
                <RouterLink to="/">{{ __('Introduction') }}</RouterLink>
                <ProfileLink class="profile-link" />
                <RouterLink to="/register">{{ __('Register') }}</RouterLink>
                <Select class="interface" type="inline" :options="supportedLanguages" v-model="profile.interfaceLanguage" />
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

.interface {
  max-width: 80px;
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
