import { useRouter } from 'vue-router';
import type { FetchFn } from '@/types';

export const useFetchAuthorized = (): FetchFn => {  
  const router = useRouter();
  
  // this is the adjusted fetch function
  return async <T>(...args: Parameters<typeof fetch>): Promise<T | null> => {

    try {
      const response = await fetch(...args);

      if (response.status === 401) {
        // Redirect to login with the current path as the 'next' parameter using Vue Router
        const currentPath = router.currentRoute.value.fullPath;
        if (!currentPath.startsWith('/login')) {
          router.push(`/login?next=${encodeURIComponent(currentPath)}`);
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
