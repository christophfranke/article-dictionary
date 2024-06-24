import type { PartialWord, FetchFn } from '@/types';
import type { StreamApi } from '@/layers/api';


export interface DictionaryApi extends StreamApi<PartialWord> {
  rebuild: () => AsyncGenerator<{ message: string } | null, void, unknown>;
  retranslate: (id: string) => AsyncGenerator<PartialWord | null, void, unknown>;
  markSeen: (id: string) => AsyncGenerator<PartialWord | null, void, unknown>;
  getWord: (id: string) => AsyncGenerator<PartialWord | null, void, unknown>;
}

export default (apiRequest: FetchFn): DictionaryApi => {
  const list = async function* (): AsyncGenerator<PartialWord[], void, unknown> {
    yield await apiRequest<PartialWord[]>('/api/dictionary/') || [];
  };

  const rebuild = async function* (): AsyncGenerator<{ message: string } | null, void, unknown> {
    yield await apiRequest('/api/dictionary/reset', { method: 'POST' });
  };

  const retranslate = async function* (id: string): AsyncGenerator<PartialWord | null, void, unknown> {
    yield await apiRequest(`/api/dictionary/retranslate/${id}`, { method: 'POST' });
  };

  const markSeen = async function* (id: string): AsyncGenerator<PartialWord | null, void, unknown> {
    yield await apiRequest(`/api/dictionary/seen/${id}`, { method: 'POST' });
  };

  const getWord = async function* (id: string): AsyncGenerator<PartialWord | null, void, unknown> {
    yield await apiRequest(`/api/dictionary/get/${id}`, { method: 'GET' });
  };

  const add = async function* (data: Record<string, unknown>): AsyncGenerator<PartialWord | null, void, unknown> {
    yield await apiRequest('/api/dictionary/add', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
  };

  // make sure only one request per id is active
  const updateRequestMap: { [key: string]: Promise<PartialWord | null> | undefined } = {}
  const updateOne = async function* (id: string, data: Record<string, unknown>): AsyncGenerator<PartialWord | null, void, unknown> {
    if (updateRequestMap[id]) {
      await updateRequestMap[id];
    }

    updateRequestMap[id] = apiRequest(`/api/dictionary/update/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    yield await updateRequestMap[id]!;
  };

  const updateMany = async function* (ids: string[], update: Record<string, unknown>): AsyncGenerator<PartialWord[] | null, void, unknown> {
    yield await apiRequest('/api/dictionary/update/', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ ids, update }),
    });
  }

  const get = async function* (original: string): AsyncGenerator<PartialWord | null, void, unknown> {
    yield await apiRequest(`/api/dictionary/${original}`);
  }

  return {
    list,
    get,
    add,
    updateOne,
    updateMany,
    rebuild,
    retranslate,
    markSeen,
    getWord,
  }
}
