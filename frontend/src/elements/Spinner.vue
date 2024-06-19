<script setup lang="ts">
import useApi from '@/use/api'

const { isLoading } = useApi()
</script>

<template>
  <transition
    name="spinner-fade"
    mode="out-in"
    appear
  >
    <div v-if="isLoading" class="spinner-container">
      <svg
        class="spinner"
        width="37.5px"
        height="37.5px"
        viewBox="0 0 50 50"
        xmlns="http://www.w3.org/2000/svg"
      >
        <circle
          class="path"
          cx="25"
          cy="25"
          r="20"
          fill="none"
          stroke-width="5"
        ></circle>
      </svg>
    </div>
  </transition>
</template>

<style scoped lang="scss">
@import "@/style/global.scss";

.spinner-container {
  position: fixed;
  bottom: 10px;
  right: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.spinner {
  animation: rotate 2s linear infinite;
}

.path {
  stroke: $view-color;
  stroke-linecap: round;
  animation: dash 1.5s ease-in-out infinite;
}

@keyframes rotate {
  100% {
    transform: rotate(360deg);
  }
}

@keyframes dash {
  0% {
    stroke-dasharray: 1, 150;
    stroke-dashoffset: 0;
  }
  50% {
    stroke-dasharray: 90, 150;
    stroke-dashoffset: -35;
  }
  100% {
    stroke-dasharray: 90, 150;
    stroke-dashoffset: -124;
  }
}


.spinner-fade-enter-active {
  transition: opacity .3s;
  transition-delay: .3s;
}

.spinner-fade-leave-active {
  transition: opacity .3s; /* No delay for leaving */
}

.spinner-fade-enter-from,
.spinner-fade-leave-to /* .spinner-fade-leave-active in <2.1.8 */ {
  opacity: 0;
}
</style>
