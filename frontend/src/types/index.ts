export interface PartialWord {
  id: string;
  original: string;
  translations: string[];
  status: string;
  frequency: number;
}

export interface Word extends PartialWord {
  order: number;
}

export interface WordDetail extends Word {
  sentences: {
    text: string
    words: string[]
  }[];
  similar: string[];
}

export interface ArticleData {  
  title: string;
  content: string;
  privacy: string;
}

export interface ArticleBase extends ArticleData {
  id: string;
  slug: string;
  status: string;
  owned: boolean;
  readingIndex: number;
}

export interface ArticlePreview extends ArticleBase {
  excerpt: string;
  lastRead: string;
  createdAt: string;
  statistics: {
    total: number;
    new: {
      words: number;
      cluster: number;
    }
    seen: {
      words: number;
      cluster: number;
    }
    known: {
      words: number;
      cluster: number;
    }
  }
}

export interface ArticleDetail extends ArticleBase {
  words: string[];
}

export interface Progress {
    date: string;
    latest_timestamp: string;
    known_words: number;
    new_words: number;
    seen_words: number;
    total_words: number;
    known_cluster: number;
    new_cluster: number;
    seen_cluster: number;
    total_cluster: number;
}

export interface ProfilePreview {
  isLoggedIn: boolean;
  name: string;
  email: string;
}

export interface Profile extends ProfilePreview {
  sourceLanguage: string;
  targetLanguage: string;
}

export type FetchFn = <T>(...args: Parameters<typeof fetch>) => Promise<T | null>;
