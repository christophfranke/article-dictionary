import { ref, onMounted } from 'vue';
import { useFetchAuthorized } from '@/use/api';

const name = ref('');
const isLoggedIn = ref(false);
const email = ref('');
const sourceLanguage = ref('');
const targetLanguage = ref('');
const fetchAuthorized = useFetchAuthorized();


const fetchPreview = async () => {
  const data = await fetchAuthorized('/api/profile/preview');

  isLoggedIn.value = data.isLoggedIn;
  name.value = data.name;
};

const fetchProfileSettings = async () => {
  const data = await fetchAuthorized('/api/profile/settings');

  if (data) {
    email.value = data.email;
    name.value = data.name;
    sourceLanguage.value = data.sourceLanguage;
    targetLanguage.value = data.targetLanguage;
  }
};

export const useUser = () => {
	onMounted(fetchPreview)
	return { name, isLoggedIn }
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
	return async (formData) => {
	  const data = await fetchAuthorized('/api/profile/update', {
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

	const login = async (): boolean => {
    data = await fetchAuthorized('/api/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email: localEmail.value, localPassword: password.value }),
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

export const useLogout = () => {
	return async (): boolean => {
    const data = await fetchAuthorized('/api/auth/logout');

    if (data) {
	    isLoggedIn.value = false
	    name.value = ''
	    email.value = ''
	    password.value = ''
	    return true
    }

	  return false
	};
}