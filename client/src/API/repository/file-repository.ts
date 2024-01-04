import AxiosService from '../axios/AxiosService';
import { endpoints } from '../registry';
import { headerBuilder } from '../headerBuilder';

export const uploadFile = async (file: File): Promise<{filename: string}> => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await AxiosService.post(
        endpoints.POST_UPLOAD_PDF(),
        formData,
        {
            headers: {
                ...headerBuilder.POST_HEADER,
                'Content-Type': 'multipart/form-data',
            },
        },
    );

    return response.data;
};

export const getAllFilenames = async (): Promise<string[]> => {
    const response = await AxiosService.get(
        endpoints.GET_ALL_FILENAMES()
    );
    return response.data;
}

export const resetFiles = async (): Promise<any> => {
    const response = await AxiosService.delete(
        endpoints.RESET_FILES()
    );
    return response.data;
    
}