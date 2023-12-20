import type { PartialWord } from '@/types';
import type { DictionaryApi } from './request';

export default (request: DictionaryApi, key: string): DictionaryApi => {
	let data: { [key: string]: PartialWord } = JSON.parse(localStorage.getItem(key) || '{}');

	const save = (newData: PartialWord[]) => {
			newData.forEach(word => {
				data[word.id] = word;
			})

			localStorage.setItem(key, JSON.stringify(data));
	}

	const list = async function* (): AsyncGenerator<PartialWord[], void, unknown> {
		yield Object.values(data);
		for await (const newData of request.list()) {
			yield newData;
			save(newData);
		}
	}

	return {
		...request,
		list
	}
}