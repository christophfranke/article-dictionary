import type { PartialWord } from '@/types';
import type { DictionaryApi } from './request';

export default (request: DictionaryApi, key: string): DictionaryApi => {
	let collection: { [key: string]: PartialWord } = JSON.parse(localStorage.getItem(key) || '{}');

	const save = (newData: PartialWord[]) => {
			newData.forEach(word => {
				collection[word.id] = word;
			})

			localStorage.setItem(key, JSON.stringify(collection));
	}

	const list = async function* (): AsyncGenerator<PartialWord[], void, unknown> {
		yield Object.values(collection);
		for await (const newData of request.list()) {
			yield newData;
			save(newData);
		}
	}

	const add = async function* (data: Record<string, unknown>): AsyncGenerator<PartialWord | null, void, unknown> {
		for await (const newData of request.add(data)) {
			yield newData;
			if (newData) {				
				save([newData]);
			}
		}		
	}

	const updateOne = async function* (id: string, data: Record<string, unknown>): AsyncGenerator<PartialWord | null, void, unknown> {
		const oldItem = collection[id];
		if (oldItem) {
			const item = { ...oldItem, ...data } as PartialWord;
			yield item;
			save([item]);
		}

		for await (const newData of request.updateOne(id, data)) {
			yield newData;
			if (newData) {
				save([newData]);
			}
		}
	}

	return {
		...request,
		add,
		updateOne,
		list
	}
}