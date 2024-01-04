import { useState } from 'react';

import { searchQuery } from '../../API/repository/search-repository';
import { ResultItem } from '../../type';
import SearchResultDisplay from './SearchResultDisplay';
import SearchForm from './SearchForm';

function Browser() {
    const [query, setQuery] = useState<string>('');
    const [submittedQuery, setSubmittedQuery] = useState<string>('');
    const [searchResult, setSarchResult] = useState<ResultItem[] | null>(null);
    const [loading, setLoading] = useState<boolean>(false);


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
        <>
            <SearchForm
                onSearch={handleSearch}
                query={query}
                onQueryChange={(query) => setQuery(query)}
                loading={loading}
            />
            <SearchResultDisplay
                loading={loading}
                searchResult={searchResult}
                query={submittedQuery}
            />
        </>
    );
}

export default Browser;