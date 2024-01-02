import AxiosService from '../axios/AxiosService';
import { endpoints } from '../registry';
import { headerBuilder } from '../headerBuilder';

export const uploadFile = async (file: File): Promise<any> => {
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
