import type { StreamApi } from './api';


export default <T>(request: StreamApi<T>, key: string): StreamApi<T> => {
	return request
}