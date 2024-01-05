import styled from 'styled-components';
import { uploadFiles } from '../../API/repository/file-repository';
import { useRef, useState } from 'react';
import Button from '../shared/Button';

type Props = {
    onRefresh: () => void;
};

const FileInput = ({ onRefresh }: Props) => {
    const [loading, setLoading] = useState<boolean>(false);
    const fileInputRef = useRef<HTMLInputElement>(null);

    const handleFileSelect = async (
        event: React.ChangeEvent<HTMLInputElement>,
    ) => {
        if (event.target.files) {
            const files = Array.from(event.target.files).filter(
                (file) => file.type === 'application/pdf',
            );

            if (files.length > 0) {
                setLoading(true);
                try {
                    await uploadFiles(files);
                    onRefresh();
                } catch (error) {
                    console.error('Upload failure', error);
                }
                setLoading(false);
                if (fileInputRef.current) {
                    fileInputRef.current.value = '';
                }
            }
        }
    };

    const handleButtonClick = () => {
        fileInputRef.current?.click();
    };

    return (
        <Container>
            <HiddenInput
                type="file"
                ref={fileInputRef}
                onChange={handleFileSelect}
                multiple
                accept="application/pdf"
                disabled={loading}
            />
            <Button onClick={handleButtonClick} disabled={loading}>
                {loading ? 'Indexing Files...' : 'Upload Files'}
            </Button>
        </Container>
    );
};

export default FileInput;

const Container = styled.div`
    display: flex;
    flex-direction: column;
    align-items: start;
`;

const HiddenInput = styled.input`
    display: none; // Masquer l'input
`;
