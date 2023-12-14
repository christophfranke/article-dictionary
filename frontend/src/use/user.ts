import { ref, onMounted } from 'vue';
import useApi from '@/use/api';
import type { User, UserPreview, FetchFn } from '@/types';

const name = ref('');
const isLoggedIn = ref(false);
const email = ref('');
const sourceLanguage = ref('');
const targetLanguage = ref('');


const fetchPreview = (fetchAuthorized: FetchFn) => async  () => {
  const data = await fetchAuthorized<UserPreview>('/api/profile/preview');

  if (data) {  	
	  isLoggedIn.value = data.isLoggedIn;
	  name.value = data.name;
	  email.value = data.email;
  }
};

const fetchProfileSettings = (fetchAuthorized: FetchFn) => async () => {
  const data = await fetchAuthorized<User>('/api/profile/settings');

  if (data) {
    email.value = data.email;
    name.value = data.name;
    sourceLanguage.value = data.sourceLanguage;
    targetLanguage.value = data.targetLanguage;
  }
};

export const useUser = () => {
	const { fetchAuthorized } = useApi();
	onMounted(fetchPreview(fetchAuthorized))
	return { name, email, isLoggedIn }
};

export const useProfile = () => {
	const { fetchAuthorized } = useApi();
	onMounted(fetchProfileSettings(fetchAuthorized))

	return {
		isLoggedIn,
		email,
		name,
		sourceLanguage,
		targetLanguage,
	}
}

export const useUpdateProfile = () => {
	const { fetchAuthorized, errorMessage, isLoading } = useApi();

	const updateProfile = async (formData: any) => {
	  const data = await fetchAuthorized<User>('/api/profile/update', {
	    method: 'POST',
	    headers: {
	      'Content-Type': 'application/json',
	    },
			// remove sourceLanguage and targetLanguage, because not yet supported
	    body: JSON.stringify(formData),
	  });

	  if (data) {
	    email.value = data.email;
	    name.value = data.name;
	    sourceLanguage.value = data.sourceLanguage;
	    targetLanguage.value = data.targetLanguage;

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
	const { fetchAuthorized, errorMessage, isLoading } = useApi();
	const localEmail = ref('')
	const localPassword = ref('')

	const login = async (): Promise<boolean> => {
    const data = await fetchAuthorized<UserPreview>('/api/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email: localEmail.value, password: localPassword.value }),
    });

    if (data) {
    	isLoggedIn.value = true;
    	email.value = localEmail.value;
    	fetchPreview(fetchAuthorized)();

    	return true;
    }

    return false;
	}

	return {
		login,
		email: localEmail,
		password: localPassword,
		errorMessage,
		isLoading,
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
    const data = await fetchAuthorized<UserPreview>('/api/auth/register', {
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
    	isLoggedIn.value = true;
    	email.value = localEmail.value;
    	name.value = localName.value;
    	fetchPreview(fetchAuthorized)();

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
	    isLoggedIn.value = false
	    name.value = ''
	    email.value = ''
	    sourceLanguage.value = '';
	    targetLanguage.value = '';
	    return true
    }

	  return false
	};
}
