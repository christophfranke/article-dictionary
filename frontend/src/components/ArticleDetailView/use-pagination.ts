import { ref, computed, watchEffect } from 'vue';
import type { Ref } from 'vue';
import type { ArticleDetail } from '@/types';

const splitChars = ['\n\n', '.\n','\n', '. ', '.', ' '];
export const splitContentIntoPages = (content: string, pageLength: number, errorMargin: number): number[] => {
  const splitChars = ['\n\n', '\n', '.', ' '];
  let splitIndices = [0]; // Start with the first index as 0
  let currentIndex = 0;

  while (currentIndex < content.length) {
    let minPageLength = pageLength - (pageLength * errorMargin / 100);
    let maxPageLength = pageLength + (pageLength * errorMargin / 100);
    let foundBreak = false;

    // Determine the range within which a break is acceptable
    let acceptableRangeStart = Math.max(currentIndex + minPageLength, 0);
    let acceptableRangeEnd = Math.min(currentIndex + maxPageLength, content.length);

    for (let char of splitChars) {
      let breakIndex = -1;
      let searchStartIndex = acceptableRangeStart;

      // Search for a break within the acceptable range
      while (searchStartIndex <= acceptableRangeEnd && breakIndex === -1) {
        breakIndex = content.indexOf(char, searchStartIndex);
        if (breakIndex === -1 || breakIndex > acceptableRangeEnd) {
          // No valid break found with this character within the range
          breakIndex = -1;
          searchStartIndex = acceptableRangeEnd + 1; // Move past the range end
        } else {
          // Valid break found
          splitIndices.push(breakIndex + char.length);
          currentIndex = breakIndex + char.length;
          foundBreak = true;
          break;
        }
      }

      if (foundBreak) {
        break; // Break out of the loop as a suitable break point is found
      }
    }

    // If no suitable break is found with any split characters, forcefully break at maxPageLength
    if (!foundBreak) {
      let forceBreakIndex = acceptableRangeEnd;
      splitIndices.push(forceBreakIndex);
      currentIndex = forceBreakIndex;
    }
  }

  if (content.length - splitIndices[splitIndices.length - 1] < (pageLength * errorMargin / 100)) {
    // If the last page is too short, merge it with the previous page
    splitIndices.pop();
  }

  return splitIndices;
};


export const getPageContents = (content: string, splitIndices: number[]): string[] => {
  return splitIndices.map((pageStart, i) => {
    const pageEnd = splitIndices[i + 1] || content.length;
    return content.slice(pageStart, pageEnd);
  });
}

export const calculateWordSplits = (content: string, words: string[], splitIndices: number[]): number[] => {
  const result: number[] = []; // Start with the first index as 0
  let index = 0;

  splitIndices.forEach((pageStart, i) => {
    const pageEnd = splitIndices[i + 1] || content.length;
    const pageContent = content.slice(pageStart, pageEnd);

    // push the first word that starts after the page start
    result.push(index);

    // consume pageContent word by word
    let pageIndex = 0;
    while(index < words.length) {
      const word = words[index];
      const wordStart = pageContent.indexOf(word, pageIndex);

      // if word is not found, break
      if (wordStart === -1) {
        break;
      }

      pageIndex = wordStart + word.length;

      // if word is found, move index to the next word
      index++;
    }
  });

  return result;
}

export const getPageWords = (words: string[], wordSplits: number[]): string[][] => {
  return wordSplits.map((pageStart, i) => {
    const pageEnd = wordSplits[i + 1] || words.length;
    return words.slice(pageStart, pageEnd);
  });
}

export default (article: Ref<ArticleDetail | undefined>) => {
  // Constants and Refs
  const pageLength = ref(2000); // Example page length
  const errorPercentage = ref(10); // Error percentage

  let splitDetails = ref<{
    splitIndices: number[];
    pageContent: string[];
    wordSplits: number[];
    pageWords: string[][];
  }>({
    splitIndices: [],
    pageContent: [],
    wordSplits: [],
    pageWords: [],
  });
  watchEffect(() => {
    if (article.value) {      
      const splitIndices = splitContentIntoPages(article.value.content, pageLength.value, errorPercentage.value);
      const pageContent = getPageContents(article.value.content, splitIndices);
      const wordSplits = calculateWordSplits(article.value.content, article.value.words, splitIndices);
      const pageWords = getPageWords(article.value.words, wordSplits);
      splitDetails.value = {
        splitIndices,
        pageContent,
        wordSplits,
        pageWords,
      };
    }
  });

  const currentPage = ref(1);

  const paginatedContent = computed(() => {
    return splitDetails.value.pageContent[currentPage.value - 1];
  });

  const paginatedWords = computed(() => {
    return splitDetails.value.pageWords[currentPage.value - 1];
  });


  // Update dictionary filter function for current page
  const numberOfPages = computed(() => {
    return splitDetails.value.pageContent.length;
  });


  // Compute relativeIndex
  const relativeIndex = computed(() => {
    if (!article.value || article.value.readingIndex === undefined) {
      return { page: -1, index: -1 };
    }

    const readingIndex = article.value.readingIndex;
    const wordSplits = splitDetails.value.wordSplits;

    // Find the page number for the readingIndex
    const pageIndex = wordSplits.findIndex((splitIndex, index) => {
      const nextPageSplitIndex = wordSplits[index + 1] || article.value!.words.length;
      return readingIndex >= splitIndex && readingIndex < nextPageSplitIndex;
    });

    if (pageIndex === -1) {
      return { page: -1, index: -1 }; // ReadingIndex is out of range
    }

    // Calculate the relative index of the word on the found page
    const relativeWordIndex = readingIndex - wordSplits[pageIndex];

    return { page: pageIndex + 1, index: relativeWordIndex };
  });

  const getAbsoluteIndex = (index: number): number => {
    const wordSplits = splitDetails.value.wordSplits;
    const pageIndex = currentPage.value - 1;

    return wordSplits[pageIndex] + index;
  }

  return {
    currentPage,
    paginatedContent,
    paginatedWords,
    numberOfPages,
    relativeIndex,
    getAbsoluteIndex,
  }
}
