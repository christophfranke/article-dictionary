import { describe, it, expect, beforeEach, vi } from 'vitest';
import createCollection from './collection';

// Mock StreamApi for testing purposes
const mockStreamApi = {
  add: vi.fn(() => []),
  list: vi.fn(() => []),
  updateOne: vi.fn(() => []),
  updateMany: vi.fn(() => []),
  get: vi.fn(() => []),
};

describe('Collection', () => {
  let collection;

  beforeEach(() => {
    // Reset the collection before each test
    collection = createCollection(mockStreamApi, 'searchField', 'requestField');
  });

  it('should add an item', async () => {
    const data = { id: '1', name: 'Item 1' };
    mockStreamApi.add.mockImplementationOnce(async function* () {
      yield data;
    });

    const result = await collection.add(data);

    expect(result).toEqual(data);
    expect(collection.all.value).toContain(data);
  });

  it('should load items', async () => {
    const data = [{ id: '1', name: 'Item 1' }, { id: '2', name: 'Item 2' }];
    mockStreamApi.list.mockImplementationOnce(async function* () {
      yield data;
    });

    const result = await collection.load();

    expect(result).toEqual(data);
    expect(collection.all.value).toEqual(data);
  });

  it('should find an item by key', () => {
    const data = { id: '1', name: 'Item 1', searchField: 'key' };
    collection.set([data]);

    const result = collection.find('key');

    expect(result).toEqual(data);
  });

  it('should find an item by id', () => {
    const data = { id: '1', name: 'Item 1' };
    collection.set([data]);

    const result = collection.findById('1');

    expect(result).toEqual(data);
  });

  it('should update an item', async () => {
    const data = { id: '1', name: 'Item 1' };
    const updatedData = { id: '1', name: 'Updated Item 1' };
    collection.set([data]);
    mockStreamApi.updateOne.mockImplementationOnce(async function* () {
      yield updatedData;
    });

    const result = await collection.updateOne('1', updatedData);

    expect(result).toEqual(updatedData);
    expect(collection.all.value).toContainEqual(updatedData);
  });

  it('should update multiple items', async () => {
    const data = [{ id: '1', name: 'Item 1' }, { id: '2', name: 'Item 2' }];
    const updatedData = [{ id: '1', name: 'Updated Item 1' }, { id: '2', name: 'Updated Item 2' }];
    collection.set(data);
    mockStreamApi.updateMany.mockImplementationOnce(async function* () {
      yield updatedData;
    });

    const result = await collection.updateMany(['1', '2'], {});

    expect(result).toEqual(updatedData);
    expect(collection.all.value).toEqual(updatedData);
  });

  it('should get an item', async () => {
    const data = { id: '1', name: 'Item 1' };
    mockStreamApi.get.mockImplementationOnce(async function* () {
      yield data;
    });

    const result = await collection.get('1');

    expect(result).toEqual(data);
    expect(collection.all.value.find(item => item.id === '1' && item.name === 'Item 1')).toBeTruthy()
  });

  it('should discard all items', () => {
    const data = [{ id: '1', name: 'Item 1' }, { id: '2', name: 'Item 2' }];
    collection.set(data);

    collection.discard();

    expect(collection.all.value).toEqual([]);
  });
});
