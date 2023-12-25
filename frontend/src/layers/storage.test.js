import { describe, it, expect, beforeEach, vi } from 'vitest';
import createStorage from './storage'; // Adjust the import path

describe('Enhanced StreamApi', () => {
  let mockApi;
  let enhancedApi;

  beforeEach(() => {
    // Reset localStorage and mockApi before each test
    localStorage.clear();

    mockApi = {
      list: vi.fn(() => []),
      add: vi.fn(() => []),
      get: vi.fn(() => []),
      updateOne: vi.fn(() => [])
    };
    enhancedApi = createStorage(mockApi, 'testKey');
  });

  it('should cache and return data from list', async () => {
    // Mock API response
    mockApi.list.mockImplementationOnce(async function* () {
      yield [{ id: '1', name: 'Test Item' }];
    });

    // Test initial load from localStorage
    const listGenerator = enhancedApi.list();
    expect(await listGenerator.next()).toEqual({ done: false, value: [] });

    // Test API response caching
    expect(await listGenerator.next()).toEqual({ done: false, value: [{ id: '1', name: 'Test Item' }] });

    await listGenerator.next()

    const storedData = JSON.parse(localStorage.getItem('testKey') || '{}');
    expect(storedData).toHaveProperty('1', { id: '1', name: 'Test Item' });
  });

  it('should add data and save to localStorage', async () => {
    const newItem = { id: '2', name: 'New Item' };
    mockApi.add.mockImplementationOnce(async function* () {
      yield newItem;
    });

    const addGenerator = enhancedApi.add(newItem);
    expect(await addGenerator.next()).toEqual({ done: false, value: newItem });

    await addGenerator.next();

    const storedData = JSON.parse(localStorage.getItem('testKey') || '{}');
    expect(storedData).toHaveProperty('2', newItem);
  });

  it('should retrieve a single item using get', async () => {
    const item3 = { id: '3', name: 'Existing Item' };
    const item4 = { id: '4', name: 'Another Item' };

    mockApi.add.mockImplementationOnce(async function* (item) {
      yield item;
    });

    // add item3 to localStorage
    for await(const _ of enhancedApi.add(item3));

    let hasResult = false;
    for await(const result of enhancedApi.get(item3.id)) {
      if (result) {
        hasResult = true
        expect(result).toEqual(item3);
      }
    }
    expect(hasResult).toBe(true);

    // Test retrieval from API if not in localStorage
    mockApi.get.mockImplementationOnce(async function* () {
      yield item4;
    });

    hasResult = false;
    for await(const result of enhancedApi.get(item4.id)) {
      if (result) {
        hasResult = true
        expect(result).toEqual(item4);
      }
    }

    expect(hasResult).toBe(true);
  });

  it('should update an item and save changes to localStorage', async () => {
    const originalItem = { id: '5', name: 'Old Item' };
    const updatedItem = { id: '5', name: 'Updated Item' };
    localStorage.setItem('testKey', JSON.stringify({ '5': originalItem }));

    mockApi.updateOne.mockImplementationOnce(async function* () {
      yield updatedItem;
    });

    const updateOneGenerator = enhancedApi.updateOne('5', { name: 'Updated Item' });
    expect(await updateOneGenerator.next()).toEqual({ done: false, value: updatedItem });
    for await (const _ of updateOneGenerator);

    const storedData = JSON.parse(localStorage.getItem('testKey') || '{}');
    expect(storedData).toHaveProperty(updatedItem.id, updatedItem);
  });
});
