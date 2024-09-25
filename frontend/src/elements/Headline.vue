<script setup lang="ts">
const { type } = defineProps({
    type: {
        type: String,
        default: 'h1',
    },
});

const allowedTypes = ['h1', 'h2', 'h3'];
</script>

<template>
    <component :is="type" v-if="allowedTypes.includes(type)">
        <slot />
    </component>
</template>

<style scoped lang="scss">
@import "@/style/global.scss";

h1, h2, h3 {
	margin: 0;
  color: $headline-font-color;
}

h1 {
  font-size: 32px;
}
h2 {
  font-size: 24px;
}
h3 {
  font-size: 18px;
}
</style>