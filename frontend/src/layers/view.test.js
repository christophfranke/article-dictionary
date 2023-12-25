import { describe, it, expect, beforeEach, vi } from 'vitest';
import { ref } from 'vue';
import createView from './view';

describe('View Utility', () => {
  let mockCollection;
  let view;

  const testData = [
    { id: '1', name: 'Item 1', category: 'A' },
    { id: '2', name: 'Item 2', category: 'B' },
    // Add more items as needed
  ];

  beforeEach(() => {
    mockCollection = {
      find: vi.fn((keyValue) => testData.find(item => item.id === keyValue)),
      all: ref(testData),
      // Mock other methods of Collection if needed
    };

    view = createView(mockCollection);
  });

  it('checks if an item is visible based on filter', () => {
    const filterFn = (x) => x.category === 'A';
    view.setFilter(filterFn);
    expect(view.isVisible('1')).toBe(true);
    expect(view.isVisible('2')).toBe(false);
  });

  it('computes `all` with default ordering', () => {
    expect(view.all.value).toEqual([
      { ...testData[0], order: 0 },
      { ...testData[1], order: 1 },
      // Add assertions for other items if needed
    ]);
  });

  it('computes `items` based on the filter', () => {
    const filterFn = (x) => x.category === 'A';
    view.setFilter(filterFn);
    expect(view.items.value).toEqual([
      { ...testData[0], order: 0 },
      // Include only items that match the filter
    ]);
  });

  it('sets a new filter and updates `items` accordingly', () => {
    const newFilterFn = (x) => x.category === 'B';
    view.setFilter(newFilterFn);
    expect(view.items.value).toEqual([
      { ...testData[1], order: 1 },
      // Include only items that match the new filter
    ]);
  });

  it('sets a new order and updates `all` accordingly', () => {
    const newOrderFn = (x) => x.name === 'Item 1' ? 1 : 0;
    view.setOrder(newOrderFn);
    expect(view.all.value).toEqual([
      { ...testData[0], order: 1 },
      { ...testData[1], order: 0 },
    ]);
  });
});

