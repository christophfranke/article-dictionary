import { ref, computed  } from 'vue';
import type { Ref, ComputedRef } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import type { FetchFn } from '@/types';

const SIMULATE_DELAY = 0;

export const redirectToLogin = (router: any, route: any) => {
  // Redirect to login with the current path as the 'next' parameter using Vue Router
  const currentPath = route?.fullPath;
  if (router) {    
    if (currentPath && !currentPath.startsWith('/login')) {
      router.push(`/login?next=${encodeURIComponent(currentPath)}`);
    }
  }
}

export const useFetchAuthorized = (): FetchFn => {  
  const router = useRouter();
  const route = useRoute();
  
  // this is the adjusted fetch function
  return async <T>(...args: Parameters<typeof fetch>): Promise<T | null> => {
    try {
      if (SIMULATE_DELAY) {
        await new Promise(resolve => setTimeout(resolve, SIMULATE_DELAY * Math.random()));
      }
      const response = await fetch(...args);

      if (response.status === 401) {
        redirectToLogin(router, route)
      }

      if (response.ok) {
        return response.json() as T;
      }

      console.error('Could not fetch', args[0], response.status);
    } catch (error) {
      console.error('Error while fetching:', args[0], error);
    }

    return null
  };
}

interface UseApi {
  fetchAuthorized: FetchFn;
  errorMessage: Ref<string | null>;
  isLoading: ComputedRef<boolean>;
}

const loadingCounter = ref<number>(0);
const isLoading = computed<boolean>(() => loadingCounter.value > 0);
export default (): UseApi => {
  const router = useRouter();
  const route = useRoute();

  const errorMessage = ref<string | null>(null);

  const fetchAuthorized = async <T>(...args: Parameters<typeof fetch>): Promise<T | null> => {
    try {
      loadingCounter.value += 1;
      errorMessage.value = null;

      if (SIMULATE_DELAY) {
        await new Promise(resolve => setTimeout(resolve, SIMULATE_DELAY * Math.random()));
      }
      const response = await fetch(...args);

      if (response.status === 401) {
        redirectToLogin(router, route);

        loadingCounter.value -= 1;
        return null;
      }

      if (response.ok) {
        const data = await response.json() as T;
        loadingCounter.value -= 1;
        return data;
      }

      const { error } = await response.json();
      if (error) {
        errorMessage.value = error;
      } else {
        errorMessage.value = `Could not connect to server: ${response.status}`;
      }
    } catch (error) {
      errorMessage.value = `Could not connect to server: ${error}`;
    }

    loadingCounter.value -= 1;
    return null;
  };


  return {
    fetchAuthorized,
    errorMessage,
    isLoading,
  }
}