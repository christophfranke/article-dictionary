import { useRouter, useRoute } from 'vue-router';
import type { FetchFn } from '@/types';

export const useFetchAuthorized = (): FetchFn => {  
  const router = useRouter();
  const route = useRoute();
  
  // this is the adjusted fetch function
  return async <T>(...args: Parameters<typeof fetch>): Promise<T | null> => {
    // await new Promise(resolve => setTimeout(resolve, 2000 * Math.random()));
    try {
      const response = await fetch(...args);

      if (response.status === 401) {
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
