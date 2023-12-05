// dictionary.ts
interface PartialWord {
  id: string;
  original: string;
  translations: string[];
  status: string;
}

export const loadAll = async (): Promise<PartialWord[]> => {
  try {
    const response = await fetch('/api/dictionary/');
    if (response.ok) {
      return await response.json();
    } else {
      console.error('Failed to fetch dictionary:', response.status);
      return [];
    }
  } catch (error) {
    console.error('Error fetching dictionary:', error);
    return [];
  }
};

export const rebuild = async (): Promise<{ message: string } | null> => {
  try {
    const response = await fetch('/api/dictionary/reset', { method: 'POST' });
    if (response.ok) {
      return await response.json();
    } else {
      console.error('Failed to fetch dictionary:', response.status);
      return null;
    }
  } catch (error) {
    console.error('Error fetching dictionary:', error);
    return null;
  }
};

export const retranslate = async (original: string): Promise<{ message: string } | null> => {
  try {
    const response = await fetch(`/api/dictionary/retranslate/${original}`, { method: 'POST' });
    if (response.ok) {
      return await response.json();
    } else {
      console.error('Failed to retranslate:', response.status);
      return null;
    }
  } catch (error) {
    console.error('Error retranslating:', error);
    return null;
  }
};


export const addWord = async (original: string): Promise<PartialWord | null> => {
  try {
    const result = await fetch('/api/dictionary/add', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ original }),
    });

    if (result.ok) {
      return await result.json();
    } else {
      console.error('Error adding word to dictionary:', result.status);
      return null;
    }
  } catch (error) {
    console.error('Error adding word to dictionary:', error);
    return null;
  }
};

export const updateWord = async (original: string, data: Record<string, unknown>): Promise<PartialWord | null> => {
  try {
    const result = await fetch(`/api/dictionary/update/${original}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (result.ok) {
      return await result.json();
    } else {
      console.error('Error updating word in dictionary:', result.status);
      return null;
    }
  } catch (error) {
    console.error('Error updating word in dictionary:', error);
    return null;
  }
};

export const updateMany = async (originals: string[], update: Record<string, unknown>): Promise<PartialWord[] | null> => {
  try {
    const result = await fetch('/api/dictionary/update/', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ originals, update }),
    });

    if (result.ok) {
      return await result.json();
    } else {
      console.error('Error updating words in dictionary:', result.status);
      return null;
    }
  } catch (error) {
    console.error('Error updating words in dictionary:', error);
    return null;
  }
}
