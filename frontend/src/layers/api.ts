export interface Api<T> {
  list: () => Promise<T[]>;
  get: (id: string) => Promise<T | null>;
  add: (data: Record<string, unknown>) => Promise<T | null>;
  updateOne: (id: string, data: Record<string, unknown>) => Promise<T | null>;
  updateMany: (ids: string[], update: Record<string, unknown>) => Promise<T[] | null>;
}


export interface StreamApi<T> {
  list: () => AsyncGenerator<T[], void, unknown>;
  get: (id: string) => AsyncGenerator<T | null, void, unknown>;
  add: (data: Record<string, unknown>) => AsyncGenerator<T | null, void, unknown>;
  updateOne: (id: string, data: Record<string, unknown>) => AsyncGenerator<T | null, void, unknown>;
  updateMany: (ids: string[], update: Record<string, unknown>) => AsyncGenerator<T[] | null, void, unknown>;
}


type PromiseFunction<A extends any[], T> = (...args: A) => Promise<T>;
type AsyncGeneratorFunction<A extends any[], T> = (...args: A) => AsyncGenerator<T, void, unknown>;

export function makeAsyncGenerator<A extends any[], T>(fn: PromiseFunction<A, T>): AsyncGeneratorFunction<A, T> {
    return async function* (...args: A): AsyncGenerator<T, void, unknown> {
        yield await fn(...args);
    };
}
