<script setup lang="ts">
import { RouterLink } from 'vue-router';
import Button from '@/elements/Button.vue';

const { to, role, size } = defineProps({
    to: {
        type: String,
        required: true,
    },
    role: {
        type: String,
        default: 'view',
    },
    size: {
        type: String,
        default: 'default',
    }
});
</script>

<template>
    <RouterLink :to="to">
        <Button class="button" :role="role" :size="size"><slot /></Button>
    </RouterLink>
</template>

<style scoped lang="scss">
.button {
  width: 100%;
}
</style>
