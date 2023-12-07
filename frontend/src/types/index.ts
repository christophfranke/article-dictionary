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
}

export interface ArticlePreview extends ArticleBase {
  excerpt: string;
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
