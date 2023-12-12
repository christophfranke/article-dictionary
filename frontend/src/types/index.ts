export interface PartialWord {
  id: string;
  index: number;
  original: string;
  translations: string[];
  status: string;
  frequency: number;
}

export interface Word extends PartialWord {
  index: number;
}

export interface ArticleData {  
  title: string;
  content: string;
}

export interface ArticleBase extends ArticleData {
  id: string;
  slug: string;
  status: string;
  owned: boolean;
}

export interface ArticlePreview extends ArticleBase {
  excerpt: string;
  lastRead: string;
  createdAt: string;
  statistics: {
    total: number;
    new: number;
    seen: number;
    known: number;
  }
}

export interface ArticleDetail extends ArticleBase {
  words: string[];
  dictionary: Word[];
}

export interface Progress {
    date: string;
    known_words: number;
    latest_timestamp: string;
    new_words: number;
    seen_words: number;
    total_words: number;
}

export interface UserPreview {
  isLoggedIn: boolean;
  name: string;
  email: string;
}

export interface User extends UserPreview {
  sourceLanguage: string;
  targetLanguage: string;
}

export type FetchFn = <T>(...args: Parameters<typeof fetch>) => Promise<T | null>;
