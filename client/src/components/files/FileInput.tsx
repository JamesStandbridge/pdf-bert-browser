import styled from 'styled-components';
import { Upload } from 'antd';
import { UploadOutlined, LoadingOutlined} from '@ant-design/icons';
import Button from '../shared/Button';
import { useEffect, useState } from 'react';

type Props = {
    onFileSelect: (file: File | null) => void;
    selectedFile: File | null;
};

const FileInput = ({ onFileSelect, selectedFile }: Props) => {
    const [loading, setLoading] = useState<boolean>(false);

    useEffect(() => { 
        if (selectedFile) {
            setLoading(false);
        }
    }, [selectedFile]);
    
    const beforeUpload = (file: File) => {
        setLoading(true);
        if (file.type !== 'application/pdf') {
            return Upload.LIST_IGNORE;
        }
        onFileSelect(file);
        return false; 
    };

    return (
        <Container>
            <Upload
                beforeUpload={beforeUpload}
                maxCount={1}
                accept="application/pdf"
                showUploadList={false}
                disabled={loading}
            >
                <Button disabled={loading}>
                    {loading ? (
                        <><LoadingOutlined /> Indexing Document...</>
                    ) : (
                       <><UploadOutlined /> Upload Document</> 
                    )}
                </Button>
            </Upload>
        </Container>
    );
};

export default FileInput;

const Container = styled.div`
`;
