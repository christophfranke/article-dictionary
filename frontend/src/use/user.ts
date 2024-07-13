import { ref, onMounted, reactive, watch, watchEffect } from 'vue';
import useApi from '@/use/api';
import type { Profile, ProfilePreview, FetchFn } from '@/types';
import { setTheme } from '@/themes';

const PROFILE_KEY = 'profile'

export const profile = reactive<Profile>(
	JSON.parse(localStorage.getItem(PROFILE_KEY) || '{}')
);

// Watch for changes in the profile and update localStorage
watch(profile, () => {
  localStorage.setItem(PROFILE_KEY, JSON.stringify(profile));
}, { deep: true });

watchEffect(() => {
	if (profile.isLoggedIn) {
		setTheme(profile.theme);
	} else {
		setTheme();
	} 
});

window.addEventListener('beforeunload', () => {
	try {
		localStorage.setItem(PROFILE_KEY, JSON.stringify(profile));
	} catch(e) {
		console.error('Could not store profile to local storage', e);
	}
});

const fetchPreview = (fetchAuthorized: FetchFn) => async  () => {
  const data = await fetchAuthorized<ProfilePreview>('/api/profile/preview');

  if (data) {
  	Object.assign(profile, data);
  }
};

const fetchProfileSettings = (fetchAuthorized: FetchFn) => async () => {
  const data = await fetchAuthorized<Profile>('/api/profile/settings');

  if (data) {
  	Object.assign(profile, data);
  }
};

export const useUser = () => {
	const { fetchAuthorized } = useApi();
	onMounted(fetchPreview(fetchAuthorized))
	return { 
		profile
	}
};

export const useProfile = () => {
	const { fetchAuthorized } = useApi();
	onMounted(fetchProfileSettings(fetchAuthorized))

	return {
		profile
	}
}

export const useUpdateProfile = () => {
	const { fetchAuthorized, errorMessage, isLoading } = useApi();

	const updateProfile = async (formData: any) => {
	  const data = await fetchAuthorized<Profile>('/api/profile/update', {
	    method: 'POST',
	    headers: {
	      'Content-Type': 'application/json',
	    },
			// remove sourceLanguage and targetLanguage, because not yet supported
	    body: JSON.stringify(formData),
	  });

	  if (data) {
	  	Object.assign(profile, data);

	    return true;
	  }

	  return false;
	}

	return {
		updateProfile,
		errorMessage,
		isLoading,
	}
}


export const useLogin = () => {
	const { fetchAuthorized, errorMessage } = useApi();
	const localEmail = ref('')
	const localPassword = ref('')
	const localIsLoading = ref(false);

	const login = async (): Promise<boolean> => {
		localIsLoading.value = true;
    const data = await fetchAuthorized<ProfilePreview>('/api/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email: localEmail.value, password: localPassword.value }),
    });

    if (data) {
	  	Object.assign(profile, data);
	    await fetchPreview(fetchAuthorized)();

    	localIsLoading.value = false;
    	return true;
    }

		localIsLoading.value = false;
    return false;
	}

	return {
		login,
		email: localEmail,
		password: localPassword,
		errorMessage,
		isLoading: localIsLoading,
	}
};

export const useRegister = () => {
	const { fetchAuthorized, errorMessage, isLoading } = useApi();
	const localEmail = ref('')
	const localName = ref('')
	const localPassword = ref('')
	const localSourceLanguage = ref('')
	const localTargetLanguage = ref('')

	const register = async (): Promise<boolean> => {
    const data = await fetchAuthorized<ProfilePreview>('/api/auth/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
      	email: localEmail.value,
      	name: localName.value,
      	password: localPassword.value,
      	sourceLanguage: localSourceLanguage.value,
      	targetLanguage: localTargetLanguage.value,
      }),
    });

    if (data) {
	  	Object.assign(profile, data);
    	await fetchPreview(fetchAuthorized)();

    	return true;
    }

    return false;
	}

	return {
		register,
		email: localEmail,
		name: localName,
		password: localPassword,
		sourceLanguage: localSourceLanguage,
		targetLanguage: localTargetLanguage,
		errorMessage,
		isLoading,
	}
};

export const useLogout = () => {
	const { fetchAuthorized } = useApi();
	return async (): Promise<boolean> => {
    const data = await fetchAuthorized('/api/auth/logout');

    if (data) {
      Object.assign(profile, {
        isLoggedIn: false,
        name: '',
        email: '',
        sourceLanguage: '',
        targetLanguage: '',
      });

	    return true
    }

	  return false
	};
}
