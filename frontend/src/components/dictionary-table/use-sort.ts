import { computed, ref } from 'vue';
import type { Word } from '@/types';

export default (props: any) => {
    const sortedBy = ref<string>(props.display.sortBy);
    const sortOrder = ref<string>(props.display.sortOrder);

    const sortTable = (column: string, defaultSortOrder: string = 'asc'): void => {
	    if (!props.display.action.sort) {
	    	return
	    }

	    if (column === sortedBy.value) {
	    	sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc';
	    } else {
	    	sortedBy.value = column;
	    	sortOrder.value = defaultSortOrder;
	    }
    };

    const sortedWords = computed<Array<Word>>(() => {
	    const sorted = props.dictionary.items.value;
	    if (sortedBy.value) {
	    	sorted.sort((a: any, b: any) => {
		        const order = sortOrder.value === 'desc' ? -1 : 1;

		        // Access property values
		        const propertyA = a[sortedBy.value];
		        const propertyB = b[sortedBy.value];

		        // Check if the property is a date string
		        if (sortedBy.value === 'lastViewed') {
			        const dateA = new Date(propertyA);
			        const dateB = new Date(propertyB);
			        return dateA > dateB ? order : -order;
		        }

		        // Use localeCompare for string comparison with locale awareness
		        if (typeof propertyA === 'string' && typeof propertyB === 'string') {
		        	return propertyA.localeCompare(propertyB) * order;
		        }

		        // For non-string properties, use regular comparison
		        return propertyA > propertyB ? order : -order;
		    });
	    }

	    if (props.display.limit > 0) {
	    	return sorted.slice(0, props.display.limit);
	    }

	    return sorted;
    });

    return { sortedWords, sortTable }
};