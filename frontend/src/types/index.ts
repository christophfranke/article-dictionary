export interface PartialWord {
  id: string;
  index: number;
  original: string;
  translations: string[];
  status: string;
}

export interface Word extends PartialWord {
  index: number;
}

export interface PartialArticle {
  title: string;
  content: string;
}

export interface Article extends PartialArticle {
  words: string[];
  dictionary: Word[];
}
