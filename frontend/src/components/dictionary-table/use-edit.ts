import { ref } from 'vue';
import type { Word } from '@/types';

const editingTranslationId = ref<string>('');
const editTranslationsValue = ref<string>('');

export default (props: any) => {
	const editTranslations = async (id: string): Promise<void> => {
	  if (props.display.action.edit) {
	    editingTranslationId.value = id;
	    if (id) {
	      const word: Word | undefined = props.dictionary.items.value.find((word: Word) => word.id === id);

	      if (word) {
	        editTranslationsValue.value = word.translations.join(', ');

	        await new Promise((resolve) => setTimeout(resolve, 0));

	        const input: any = document.getElementById('edit-translations');
	        if (input) {	        	
	          input.focus();
	          input.select();
	        }
	      }
	    }
	  }
	};

	const cancelEditTranslations = async (id: string): Promise<void> => {
	  await new Promise(resolve => setTimeout(resolve, 0));

	  if (editingTranslationId.value === id) {
	    editingTranslationId.value = '';
	  }
	};


	const isUpdating = ref(false)
	const updateTranslation = async (): Promise<void> => {
	  if (isUpdating.value) {
	    return
	  }

	  isUpdating.value = true;
	  const word: Word | undefined = props.dictionary.items.value.find((word: Word) => word.id === editingTranslationId.value);

	  if (word) {
	    const translations: string[] = editTranslationsValue.value.split(',').map((t) => t.trim());
	    await props.dictionary.updateOne(word.id, { translations });
	    editingTranslationId.value = '';
	  }

	  isUpdating.value = false;
	};

	return {
		editingTranslationId,
		editTranslationsValue,
		editTranslations,
		cancelEditTranslations,
		updateTranslation
	}
}