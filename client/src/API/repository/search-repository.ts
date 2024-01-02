import AxiosService from '../axios/AxiosService';
import { endpoints } from '../registry';

export const searchQuery = async (query: string): Promise<any> => {
    const response = await AxiosService.post(endpoints.POST_SEARCH(), {
        query,
    });

    return response.data;
};
