import { computed, ref } from 'vue';
import type { Ref } from 'vue';

import type { Word, Article } from '../types';
import type { DictionaryCollection } from '../dictionary/collection';

interface StatisticsResult {
  newWordsPercentage: number;
  seenWordsPercentage: number;
  knownWordsPercentage: number;
  newWords: number;
  seenWords: number;
  knownWords: number;
  uniqueWords: number;
  totalWords: number;
}

interface UseStatisticsParams {
  dictionary: DictionaryCollection;
  article?: Ref<Article>;
}

const statisticsForArticle = (dictionary: DictionaryCollection, article: Ref<Article>): StatisticsResult => {
  let newWords = 0;
  let seenWords = 0;
  let knownWords = 0;

  article.value.words.forEach((original: string) => {
    const word = dictionary.find(original.toLowerCase());
    if (word) {
      if (word.status === 'new') {
        newWords++;
      } else if (word.status === 'seen') {
        seenWords++;
      } else if (word.status === 'known') {
        knownWords++;
      }
    }
  });

  const totalWords = newWords + seenWords + knownWords;
  const newWordsPercentage = Math.round((newWords / totalWords) * 100);
  const seenWordsPercentage = Math.round((seenWords / totalWords) * 100);
  const knownWordsPercentage = Math.round((knownWords / totalWords) * 100);

  return {
    newWordsPercentage,
    seenWordsPercentage,
    knownWordsPercentage,
    newWords,
    seenWords,
    knownWords,
    uniqueWords: dictionary.all().length,
    totalWords: article.value.words.length,
  };
}

const statisticsForDictionary = (dictionary: DictionaryCollection): StatisticsResult => {
  let newWords = 0;
  let seenWords = 0;
  let knownWords = 0;

  dictionary.all().forEach((word: Word) => {
    if (word.status === 'new') {
      newWords++;
    } else if (word.status === 'seen') {
      seenWords++;
    } else if (word.status === 'known') {
      knownWords++;
    }
  });

  const totalWords = newWords + seenWords + knownWords;
  const newWordsPercentage = Math.round((newWords / totalWords) * 100);
  const seenWordsPercentage = Math.round((seenWords / totalWords) * 100);
  const knownWordsPercentage = Math.round((knownWords / totalWords) * 100);

  return {
    newWordsPercentage,
    seenWordsPercentage,
    knownWordsPercentage,
    newWords,
    seenWords,
    knownWords,
    uniqueWords: totalWords,
    totalWords
  };
}

const useStatistics = ({ dictionary, article }: UseStatisticsParams): Ref<StatisticsResult> => !!article?.value
  ? computed<StatisticsResult>(() => statisticsForArticle(dictionary, article))
  : computed<StatisticsResult>(() => statisticsForDictionary(dictionary))

export default useStatistics;
