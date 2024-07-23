import { computed } from 'vue';
import type { Ref } from 'vue';

import type { Word, Token, ArticleDetail } from '../types';
import type { DictionaryView } from '../dictionary/view';

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
  dictionary: DictionaryView;
  article?: Ref<ArticleDetail>;
}

const statisticsForArticle = (dictionary: DictionaryView, article: Ref<ArticleDetail>): StatisticsResult => {
  let newWords = 0;
  let seenWords = 0;
  let knownWords = 0;

  article.value.tokens.forEach((token: Token) => {
    const word = dictionary.find(token.word);
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
    uniqueWords: dictionary.items.value.length,
    totalWords: article.value.tokens.length,
  };
}

const statisticsForDictionary = (dictionary: DictionaryView): StatisticsResult => {
  let newWords = 0;
  let seenWords = 0;
  let knownWords = 0;

  dictionary.all.value.forEach((word: Word) => {
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
