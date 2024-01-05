import styled from 'styled-components';
import FileInput from './FileInput';
import { useEffect, useState } from 'react';
import {
    FilePdfOutlined,
    FileUnknownOutlined,
    FileAddOutlined,
} from '@ant-design/icons';
import { getAllFilenames } from '../../API/repository/file-repository';
import Input from '../shared/Input';
import { BigIcon, NullText, PDFLink } from '../shared/design-system.styled';

const Files = () => {
    const [filenames, setFilenames] = useState<string[]>([]);
    const [searchQuery, setSearchQuery] = useState<string>('');
    const [refresh, setRefresh] = useState<number>(1);

    useEffect(() => {
        const fetchFiles = async () => {
            try {
                const files = await getAllFilenames();
                setFilenames(files);
            } catch (error) {}
        };

        fetchFiles();
    }, [refresh]);

    return (
        <Container>
            <Actions>
                <Input
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    placeholder="Search for files"
                    name="search"
                    label="Search all files"
                    containerStyle={{ width: '100%' }}
                />
                <FileInput onRefresh={() => setRefresh(refresh + 1)} />
            </Actions>
            <FileListContainer>
                <FileList>
                    {filenames.length === 0 && searchQuery.length === 0 && (
                        <NullText>
                            <BigIcon>
                                <FileAddOutlined />
                            </BigIcon>
                            <p>Upload some files</p>
                        </NullText>
                    )}
                    {filenames
                        .filter(
                            (filename) =>
                                searchQuery.length === 0 ||
                                filename
                                    .toLowerCase()
                                    .includes(searchQuery.toLowerCase()),
                        )
                        .map((filename) => (
                            <FileListItem
                                target="_blank"
                                href={`http://localhost:8000/get-pdf/${filename}`}
                                key={filename}
                            >
                                <BigIcon>
                                    <FilePdfOutlined />
                                </BigIcon>
                                <PDFLink>{filename}</PDFLink>
                            </FileListItem>
                        ))}
                    {searchQuery.length > 0 &&
                        filenames.filter((filename) =>
                            filename
                                .toLowerCase()
                                .includes(searchQuery.toLowerCase()),
                        ).length === 0 && (
                            <NullText>
                                <BigIcon>
                                    <FileUnknownOutlined />
                                </BigIcon>
                                <p>No files matching the query</p>
                            </NullText>
                        )}
                </FileList>
            </FileListContainer>
        </Container>
    );
};

export default Files;

const Actions = styled.div`
    display: flex;
    align-items: end;
    width: 100%;
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
