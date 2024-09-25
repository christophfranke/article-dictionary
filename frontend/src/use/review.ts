import type { PartialWord, Token } from '@/types';
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
  	// too soon to review
        return 0;
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

const calculateDueNeverTooLate = (word: PartialWord): number => {
    const now = new Date();

    if (word.reviewLevel === 0) {
        // too soon
        return 0;
    }
		
    if (word.reviewLevel === 1) {
        // the ideal time is now
        return 1;
    }

    const lastViewed = new Date(word.lastViewed);
    const timeSinceLastViewed = (now.getTime() - lastViewed.getTime()) / (1000 * 3600 * 24); // in days
    const idealReviewTime = 1.75 * Math.pow(2, word.reviewLevel - 2);

    // The ideal time has passed, so we are late
    if (timeSinceLastViewed > idealReviewTime) {
        return 1;
    }

    return timeSinceLastViewed * (2 - timeSinceLastViewed) / idealReviewTime;
}

const calculateDueNeverTooSoon = (word: PartialWord): number => {
    const now = new Date();

    if (word.reviewLevel === 0) {
        // cannot be too soon
        return 1;
    }

    const lastViewed = new Date(word.lastViewed);
    const timeSinceLastViewed = (now.getTime() - lastViewed.getTime()) / (1000 * 3600 * 24); // in days

    if (word.reviewLevel === 1) {
        return (1 - timeSinceLastViewed);
    }

    const idealReviewTime = 1.75 * Math.pow(2, word.reviewLevel - 2);

    // It is never too soon
    if (timeSinceLastViewed < idealReviewTime) {
        return 1;
    }

    return timeSinceLastViewed * (2 - timeSinceLastViewed) / idealReviewTime;
}

const calculateImportance = (word: PartialWord, maxFrequency: number): number => {
    const frequency = word.frequency
    if (frequency === 0) return 0;
    if (maxFrequency === 1) return 1; // Edge case to handle if maxFreq is 1

    // Logarithmic scale: importance goes from 1 (for freq 1) to 2 (for maxFreq)
    return 1 + Math.log(frequency) / Math.log(maxFrequency);
};

export type ScoreMap = {
	importance: number;
	due: number;
	dueNeverTooLate: number;
	dueNeverTooSoon: number;
}
export type ScoreFunction = (scores: ScoreMap, word: PartialWord) => number;
const plainScore: ScoreFunction = (score: ScoreMap) => score.importance * score.due;
export default (dictionary: DictionaryView, scoreFn: ScoreFunction = plainScore) => {
    const findWordForReview = (): string | null => {
        const maxFreq = Math.max(...dictionary.all.value.map(word => word.frequency));

	  let highestScore = 0; // do not select words with 0 score or less
	  let wordToReview: PartialWord | null = null;

	  for (const word of dictionary.items.value) {
	  	const importance = calculateImportance(word, maxFreq);
	  	const due = calculateDue(word);
	  	const dueNeverTooLate = calculateDueNeverTooLate(word);
	  	const dueNeverTooSoon = calculateDueNeverTooSoon(word);
	    const score = scoreFn({
	    	importance,
	    	due,
	    	dueNeverTooLate,
	    	dueNeverTooSoon,
	    }, word);
	    if (score > highestScore) {
	    	console.log(`Found new highest score for ${word.original}: ${score.toFixed(3)} (${importance.toFixed(2)}x${due.toFixed(2)})`);
	      highestScore = score;
	      wordToReview = word;
	    }
	  }

	  return wordToReview?.id || null
    };

    const pickSentence = (sentences: { text: string, tokens: Token[] }[], word?: PartialWord): number => {
        const scores = sentences.map(sentence => {
            const words = sentence.tokens.map(token => dictionary.find(token.word));
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
