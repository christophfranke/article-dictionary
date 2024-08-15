export interface PartialWord {
  id: string;
  clusterId: string;
  original: string;
  translations: string[];
  status: string;
  frequency: number;
  lastViewed: string;
  reviewLevel: number;
  needsRetranslate: string;
}

export interface Word extends PartialWord {
  order: number;
}

export interface WordDetail extends Word {
  sentences: {
    text: string
    tokens: Token[]
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
  needsProcessing: boolean;
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

export type Token = {
  display: string;
  word: string;
  space: string;
  lemma?: string;
  pos?: string;
  ignore: boolean;
}

export type Highlight = {
  token: Token | null,
  index: number
}

export interface ArticleDetail extends ArticleBase {
  tokens: Token[];
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
  interfaceLanguage: string;
  theme: string;
}

export type FetchFn = <T>(...args: Parameters<typeof fetch>) => Promise<T | null>;
