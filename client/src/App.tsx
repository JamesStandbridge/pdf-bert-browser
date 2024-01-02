import { useState } from 'react';
import './App.css';
import styled from 'styled-components';

import FileInput from './components/FileInput';

import { uploadFile } from './API/repository/file-repository';

import { searchQuery } from './API/repository/search-repository';
import { ResultItem } from './type';
import SearchResultDisplay from './components/SearchResultDisplay';
import Theme from './theme/Theme';
import SearchForm from './components/SearchForm';

function App() {
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [query, setQuery] = useState<string>('');
    const [submittedQuery, setSubmittedQuery] = useState<string>('');
    const [searchResult, setSarchResult] = useState<ResultItem[] | null>(null);
    const [loading, setLoading] = useState<boolean>(false);

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

    const handleSearch = async (e: any) => {
        e.preventDefault();
        setLoading(true);
        setSubmittedQuery(query);
        try {
            const response = await searchQuery(query.trim());
            setSarchResult(response);
        } catch (error) {
            console.error('Search error', error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <Theme>
            <Container>
                <Content>
                    <FileInput
                        selectedFile={selectedFile}
                        onFileSelect={(file) => {
                            handleFileUpload(file);
                        }}
                    />
                    <SearchForm
                        onSearch={handleSearch}
                        query={query}
                        onQueryChange={(query) => setQuery(query)}
                    />
                    <SearchResultDisplay
                        loading={loading}
                        searchResult={searchResult}
                        query={submittedQuery}
                    />
                </Content>
            </Container>
        </Theme>
    );
}

export default App;

const Content = styled.div`
    width: 80%;
    padding-top: 100px;
`;

const Container = styled.div`
    width: 100%;
    display: flex;
    min-height: 100vh;
    justify-content: center;
`;
