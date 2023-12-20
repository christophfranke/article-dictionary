import type { PartialWord, FetchFn } from '@/types';
import type { Api } from '@/layers/api';

export interface DictionaryApi extends Api<PartialWord> {
  rebuild: () => Promise<{ message: string } | null>;
  retranslate: (id: string) => Promise<PartialWord | null>;
}

export default (apiRequest: FetchFn): DictionaryApi => {
  const list = async (): Promise<PartialWord[]> => {
    return await apiRequest<PartialWord[]>('/api/dictionary/') || [];
  };

  const rebuild = async (): Promise<{ message: string } | null> => {
    return await apiRequest('/api/dictionary/reset', { method: 'POST' });
  };

  const retranslate = async (id: string): Promise<PartialWord | null> => {
    return await apiRequest(`/api/dictionary/retranslate/${id}`, { method: 'POST' });
  };

  const add = async (data: Record<string, unknown>): Promise<PartialWord | null> => {
    return await apiRequest('/api/dictionary/add', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
  };

  // make sure only one request per id is active
  const updateRequestMap: { [key: string]: Promise<PartialWord | null> | undefined } = {}
  const updateOne = async (id: string, data: Record<string, unknown>): Promise<PartialWord | null> => {
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

  const get = async (id: string): Promise<PartialWord | null> => {
    throw new Error('Not implemented');

    return null as unknown as Promise<PartialWord>;
  }

  return {
    list,
    get,
    add,
    updateOne,
    updateMany,
    rebuild,
    retranslate,
  }
}

