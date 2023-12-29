import type { PartialWord } from '@/types';
import type { DictionaryView } from '@/dictionary/view';


export const calculateIdealReviewInterval = (reviewLevel: number): number | null => {
	if (reviewLevel === 0) {
		return null;
	}

	if (reviewLevel === 1) {
		return 0
	}

	// level 3 -> 3.5 days, doubles with each level
	return 1.75 * Math.pow(2, reviewLevel - 2) * 1000 * 3600 * 24;
};

export const calculateNextDue = (word: PartialWord): Date | null => {
	const idealReviewInterval = calculateIdealReviewInterval(word.reviewLevel);
	if (idealReviewInterval === null) {
		return null;
	}

	const lastViewed = new Date(word.lastViewed);
	return new Date(lastViewed.getTime() + idealReviewInterval * 1000 * 3600 * 24);
}

const calculateDue = (word: PartialWord): number => {
  const now = new Date();
  const lastViewed = new Date(word.lastViewed);
  const timeSinceLastViewed = (now.getTime() - lastViewed.getTime()) / (1000 * 3600 * 24); // in days

  if (word.reviewLevel === 0) {
  	// it is always due if it has never been reviewed
    return 1;
  }

  if (word.reviewLevel === 1) {
  	// for first review level, score is 1 if last viewed today, 0 if last viewed more than a day ago
    return (1 - timeSinceLastViewed);
  }

  // Calculate ideal review time
  // level 3 -> 3.5 days, doubles with each level
  const idealReviewTime = 1.75 * Math.pow(2, word.reviewLevel - 2);

  // Calculate score based on how close we are to ideal review time
  return timeSinceLastViewed * (2 - timeSinceLastViewed) / idealReviewTime;
};

const calculateImportance = (word: PartialWord, maxFrequency: number): number => {
	const frequency = word.frequency
  if (frequency === 0) return 0;
  if (maxFrequency === 1) return 1; // Edge case to handle if maxFreq is 1

  // Logarithmic scale: importance goes from 1 (for freq 1) to 2 (for maxFreq)
  return 1 + Math.log(frequency) / Math.log(maxFrequency);
};

type BiasFunction = (score: number, word: PartialWord) => number;
export default (dictionary: DictionaryView, biasFn: BiasFunction = x => x) => {
	const findWordForReview = (): string | null => {
		const maxFreq = Math.max(...dictionary.all.value.map(word => word.frequency));

	  let highestScore = 0; // do not select words with 0 score or less
	  let wordToReview: PartialWord | null = null;

	  for (const word of dictionary.items.value) {
	  	const importance = calculateImportance(word, maxFreq);
	  	const due = calculateDue(word);
	    const score = biasFn(importance * due, word);
	    if (score > highestScore) {
	    	console.log(`Found new highest score for ${word.original}: ${score.toFixed(3)} (${importance.toFixed(2)}x${due.toFixed(2)})`);
	      highestScore = score;
	      wordToReview = word;
	    }
	  }

	  return wordToReview?.id || null
	};

	const pickSentence = (sentences: { text: string, words: string[] }[], word?: PartialWord): number => {
		const scores = sentences.map(sentence => {
			const words = sentence.words.map(word => dictionary.find(word));
			const score = words.reduce((acc, w) => acc + (w?.id === word?.id ? 6 : w?.reviewLevel || 0), 0);
			const random = 1 + Math.random();
			return random * score / words.length;
		});

		// find index with maximum score
		let maxIndex = 0;
		for (let i = 1; i < scores.length; i++) {
			if (scores[i] > scores[maxIndex]) {
				maxIndex = i;
			}
		}

		return maxIndex;
	};

	return {
		pickSentence,
		findWordForReview,
	}
}
