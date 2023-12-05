// dictionary.ts
interface Word {
  index: number;
  original: string;
  translations: string[];
  status: string;
}

export const loadAll = async (): Promise<Word[]> => {
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

export const rebuild = async (): Promise<Word[]> => {
  try {
    const response = await fetch('/api/dictionary/reset', { method: 'POST' });
    if (response.ok) {
      return await response.json();
    } else {
      console.error('Failed to fetch dictionary:', response.status);
      return {};
    }
  } catch (error) {
    console.error('Error fetching dictionary:', error);
    return {};
  }
};


export const addWord = async (original: string): Promise<Word | null> => {
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

export const updateWord = async (original: string, data: Record<string, unknown>): Promise<Word | null> => {
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
