import styled from 'styled-components';
import FileInput from './FileInput';
import { useEffect, useState } from 'react';
import {
    FilePdfOutlined
} from '@ant-design/icons';
import { getAllFilenames, uploadFile } from '../../API/repository/file-repository';
import Input from '../shared/Input';

type Props = {
};

const Files = ({  }: Props) => {
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [filenames, setFilenames] = useState<string[]>([]);
    const [searchQuery, setSearchQuery] = useState<string>('');

    useEffect(() => {
        const fetchFiles = async () => {
            const files = await getAllFilenames();
            setFilenames(files);
        };
        fetchFiles();
    
    }, [selectedFile])

    const handleFileUpload = async (file: File | null) => {
        if (file) {
            try {
                console.log('yes');
                const response = await uploadFile(file);
                setSelectedFile(file);
                console.log('Upload success', response);
            } catch (error) {
                console.error('Upload failure', error);
            }
        }
    };
   

    return (
        <Container>
            <Actions>
        <Input 
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search for files"
            name="search"
            label="Search"
            containerStyle={{ width: '100%' }}
        />
        <FileInput
            selectedFile={selectedFile}
            onFileSelect={(file) => {
                handleFileUpload(file);
            }}
        />

            </Actions>
        <FileListContainer>
            <FileList>
                {filenames.filter(
                    filename => searchQuery.length === 0 
                    || filename.toLowerCase().includes(searchQuery.toLowerCase())).map((filename) => (
                    <FileListItem 
                        target="_blank"
                        href={`http://localhost:8000/get-pdf/${filename}`}
                        key={filename}
                    >
                        <BigIcon>
                            <FilePdfOutlined />
                        </BigIcon>

                        <PDFLink
                        >
                            {filename}
                        </PDFLink>
                    </FileListItem>
                ))}
            </FileList>
        </FileListContainer>
        </Container>
    );
};

export default Files;

const Actions = styled.div`
    display: flex; 
    align-items: end;
    width: 100%;`
;

const PDFLink = styled.p`
    color: ${(props) => props.theme.primaryColor};
    font-size: 12px;
    text-align: center;
`;

const BigIcon = styled.div`
    font-size: 50px;
    color: ${(props) => props.theme.primaryColor};
`;


const FileListContainer = styled.div`
    width: 100%;
`;

const FileList = styled.div`
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 20px 40px;
`;

const FileListItem = styled.a`
    padding: 20px;
    text-align: center;
    text-decoration: none;
`;



const Container = styled.div``;