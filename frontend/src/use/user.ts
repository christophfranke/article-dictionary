import { ref, onMounted } from 'vue';
import { useFetchAuthorized } from '@/use/api';
import type { User, UserPreview } from '@/types';

const name = ref('');
const isLoggedIn = ref(false);
const email = ref('');
const sourceLanguage = ref('');
const targetLanguage = ref('');
const fetchAuthorized = useFetchAuthorized();


const fetchPreview = async () => {
  const data = await fetchAuthorized<UserPreview>('/api/profile/preview');

  if (data) {  	
	  isLoggedIn.value = data.isLoggedIn;
	  name.value = data.name;
	  email.value = data.email;
  }
};

const fetchProfileSettings = async () => {
  const data = await fetchAuthorized<User>('/api/profile/settings');

  if (data) {
    email.value = data.email;
    name.value = data.name;
    sourceLanguage.value = data.sourceLanguage;
    targetLanguage.value = data.targetLanguage;
  }
};

export const useUser = () => {
	onMounted(fetchPreview)
	return { name, email, isLoggedIn }
};

export const useProfile = () => {
	onMounted(fetchProfileSettings)

	return {
		email,
		name,
		sourceLanguage,
		targetLanguage,
	}
}

export const useUpdateProfile = () => {
	return async (formData: {}) => {
	  const data = await fetchAuthorized<User>('/api/profile/update', {
	    method: 'POST',
	    headers: {
	      'Content-Type': 'application/json',
	    },
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
}


export const useLogin = () => {
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
    	fetchPreview();

    	return true;
    }

    return false;
	}

	return { login, email: localEmail, password: localPassword }
};

export const useRegister = () => {
	const localEmail = ref('')
	const localName = ref('')
	const localPassword = ref('')

	const register = async (): Promise<boolean> => {
    const data = await fetchAuthorized<UserPreview>('/api/auth/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
      	email: localEmail.value,
      	name: localName.value,
      	password: localPassword.value
      }),
    });

    if (data) {
    	isLoggedIn.value = true;
    	email.value = localEmail.value;
    	name.value = localName.value;
    	fetchPreview();

    	return true;
    }

    return false;
	}

	return { register, email: localEmail, name: localName, password: localPassword }
};

export const useLogout = () => {
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