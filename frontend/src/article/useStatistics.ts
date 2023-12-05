import { computed, ref } from 'vue';

interface Word {
  status: string;
}

interface Dictionary {
  find(original: string): Word | undefined;
}

interface StatisticsResult {
  newWordsPercentage: number;
  seenWordsPercentage: number;
  knownWordsPercentage: number;
  newWords: number;
  seenWords: number;
  knownWords: number;
  totalWords: number;
}

interface Article {
  words: string[]
}

interface UseStatisticsParams {
  dictionary: Dictionary;
  article: Ref<Article>;
}

const useStatistics = ({ dictionary, article }: UseStatisticsParams): Ref<StatisticsResult> => {
  const statistics = computed<StatisticsResult>(() => {
    let newWords = 0;
    let seenWords = 0;
    let knownWords = 0;
    let totalWords = 0;

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
        totalWords++;
      }
    });

    const newWordsPercentage = Math.round((newWords / totalWords) * 100);
    const seenWordsPercentage = Math.round((seenWords / totalWords) * 100);
    const knownWordsPercentage = Math.round((knownWords / totalWords) * 100);

    return {
      newWordsPercentage,
      seenWordsPercentage,
      knownWordsPercentage,
      uniqueWords: dictionary.all().length,
      totalWords: article.value.words.length,
    };
  });

  return statistics;
};

export default useStatistics;
