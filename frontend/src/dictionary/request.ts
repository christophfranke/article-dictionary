import type { PartialWord, FetchFn } from '@/types';

export interface DictionaryApi {
  loadAll: () => Promise<PartialWord[]>;
  rebuild: () => Promise<{ message: string } | null>;
  retranslate: (id: string) => Promise<PartialWord | null>;
  addWord: (original: string) => Promise<PartialWord | null>;
  updateWord: (id: string, data: Record<string, unknown>) => Promise<PartialWord | null>;
  updateMany: (ids: string[], update: Record<string, unknown>) => Promise<PartialWord[] | null>;
}

export default (apiRequest: FetchFn): DictionaryApi => {
  const loadAll = async (): Promise<PartialWord[]> => {
    return await apiRequest<PartialWord[]>('/api/dictionary/') || [];
  };

  const rebuild = async (): Promise<{ message: string } | null> => {
    return await apiRequest('/api/dictionary/reset', { method: 'POST' });
  };

  const retranslate = async (id: string): Promise<PartialWord | null> => {
    return await apiRequest(`/api/dictionary/retranslate/${id}`, { method: 'POST' });
  };


  const addWord = async (original: string): Promise<PartialWord | null> => {
    return await apiRequest('/api/dictionary/add', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ original }),
    });
  };

  // make sure only one request per id is active
  const updateRequestMap: { [key: string]: Promise<PartialWord | null> | undefined } = {}
  const updateWord = async (id: string, data: Record<string, unknown>): Promise<PartialWord | null> => {
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

    return await updateRequestMap[id]!;
  };

  const updateMany = async (ids: string[], update: Record<string, unknown>): Promise<PartialWord[] | null> => {
    return await apiRequest('/api/dictionary/update/', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ ids, update }),
    });
  }

  return {
    loadAll,
    rebuild,
    retranslate,
    addWord,
    updateWord,
    updateMany,
  }
}

