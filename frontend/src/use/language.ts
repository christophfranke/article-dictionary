import { ref, onMounted } from 'vue';

export const useSupportedLanguages = () => {  
  const languages = ref<{ [key: string]: string } | null>(null);
  onMounted(async () => {
    const response = await fetch('/api/language/supported');
    if (response.ok) {
      languages.value = await response.json()
    }
  });

  return languages
}
