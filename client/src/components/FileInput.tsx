import { ChangeEvent } from 'react';
import styled from 'styled-components';

type Props = {
    onFileSelect: (file: File | null) => void;
    selectedFile: File | null;
};

const FileInput = ({ onFileSelect, selectedFile }: Props) => {
    const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files ? event.target.files[0] : null;
        if (file && file.type === 'application/pdf') {
            onFileSelect(file);
        } else {
            alert('Veuillez sélectionner un fichier PDF.');
            onFileSelect(null);
        }
    };

    return (
        <Container>
            <input
                type="file"
                accept="application/pdf"
                onChange={handleFileChange}
            />
            {selectedFile && <p>Fichier sélectionné : {selectedFile.name}</p>}
        </Container>
    );
};

export default FileInput;

const Container = styled.div``;
