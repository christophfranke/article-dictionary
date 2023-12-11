import { ref } from 'vue';
import type { Word } from '@/types';

export default (props: any) => {
	const editingTranslationId = ref<string>('');
	const editTranslationsValue = ref<string>('');
	const editTranslationsInput = ref<HTMLInputElement[] | null>(null);

	const editTranslations = async (id: string): Promise<void> => {
	  if (props.display.action.edit) {
	    editingTranslationId.value = id;
	    if (id) {
	      const word: Word | undefined = props.dictionary.words.value.find((word: Word) => word.id === id);

	      if (word) {
	        editTranslationsValue.value = word.translations.join(', ');

	        await new Promise((resolve) => setTimeout(resolve, 0));

	        // Focus the input field for editing translations
	        if (editTranslationsInput.value && editTranslationsInput.value.length > 0) {
	          editTranslationsInput.value[0].focus();
	          editTranslationsInput.value[0].select();
	        }
	      }
	    }
	  }
	};

	const stopEditTranslations = async (id: string): Promise<void> => {
	  await new Promise(resolve => setTimeout(resolve, 0));

	  if (editingTranslationId.value === id) {
	    editingTranslationId.value = '';
	  }
	};


	const isUpdating = ref(false)
	const updateTranslation = async (e: Event): Promise<void> => {
	  e.preventDefault();
	  if (isUpdating.value) {
	    return
	  }

	  isUpdating.value = true;
	  const word: Word | undefined = props.dictionary.words.value.find((word: Word) => word.id === editingTranslationId.value);

	  if (word) {
	    const translations: string[] = editTranslationsValue.value.split(',').map((t) => t.trim());
	    await props.dictionary.updateWord(word.original, { translations });
	    editingTranslationId.value = '';
	  }

	  isUpdating.value = false;
	};

	return {
		editingTranslationId,
		editTranslationsValue,
		editTranslationsInput,
		editTranslations,
		stopEditTranslations,
		updateTranslation
	}
}