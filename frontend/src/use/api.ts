import { ref, onMounted } from 'vue';
import type { Ref } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import type { FetchFn } from '@/types';

const redirectToLogin = (router: any, route: any) => {
  // Redirect to login with the current path as the 'next' parameter using Vue Router
  const currentPath = route?.fullPath;
  if (router) {          
    if (currentPath && !currentPath.startsWith('/login')) {
      router.push(`/login?next=${encodeURIComponent(currentPath)}`);
    } else {
      router.push('/login');
    }
  }
}

export const useFetchAuthorized = (): FetchFn => {  
  const router = useRouter();
  const route = useRoute();
  
  // this is the adjusted fetch function
  return async <T>(...args: Parameters<typeof fetch>): Promise<T | null> => {
    // await new Promise(resolve => setTimeout(resolve, 2000 * Math.random()));
    try {
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
  isLoading: Ref<boolean>;
}

export default (): UseApi => {
  const router = useRouter();
  const route = useRoute();

  const errorMessage = ref<string | null>(null);
  const isLoading = ref<boolean>(false);

  const fetchAuthorized = async <T>(...args: Parameters<typeof fetch>): Promise<T | null> => {
    try {
      isLoading.value = true;
      errorMessage.value = null;

      const response = await fetch(...args);

      if (response.status === 401) {
        isLoading.value = false;
        redirectToLogin(router, route);
        return null;
      }

      if (response.ok) {
        const data = await response.json() as T;
        isLoading.value = false;
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

    isLoading.value = false;
    return null;
  };


  return {
    fetchAuthorized,
    errorMessage,
    isLoading,
  }
}