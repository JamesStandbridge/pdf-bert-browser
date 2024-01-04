import { useEffect, useState } from 'react';
import styled from 'styled-components';
import { ResultItem } from '../type';
import {
    RightOutlined,
    DownOutlined,
    FilePdfOutlined,
    FileUnknownOutlined,
    LoadingOutlined,
    FileSearchOutlined,
} from '@ant-design/icons';
import { highlightSearchTerms } from '../utils/highlighSearchTerms';

type Props = {
    query: string;
    searchResult: ResultItem[] | null;
    loading: boolean;
};

const snippetLimit = 1000;

const SearchResultDisplay = ({ query, searchResult, loading }: Props) => {
    const [expanded, setExpanded] = useState<string[]>([]);
    const [showMore, setShowMore] = useState<string[]>([]);

    useEffect(() => {
        setExpanded([]);
        setShowMore([]);
    }, [query]);

    const expand = (key: string) => {
        if (expanded.includes(key)) {
            setExpanded(expanded.filter((item) => item !== key));
        } else {
            setExpanded([...expanded, key]);
        }
    };

    const toggleShowMore = (key: string) => {
        setShowMore((prevShowMore) =>
            prevShowMore.includes(key)
                ? prevShowMore.filter((k) => k !== key)
                : [...prevShowMore, key],
        );
    };

    return (
        <Container>
            {!loading && !searchResult && (
                <NullText>
                    <BigIcon>
                        <FileSearchOutlined />
                    </BigIcon>
                    <p>Query something ...</p>
                </NullText>
            )}
            {loading && (
                <NullText>
                    <BigIcon>
                        <LoadingOutlined />
                    </BigIcon>
                    <p>Scanning documents ...</p>
                </NullText>
            )}
            {!loading &&
                searchResult &&
                searchResult
                    .filter(
                        (result: ResultItem) =>
                            result.snippet !== 'Snippet not found.',
                    )
                    .map((result: ResultItem, index: number) => {
                        const showFullSnippet = showMore.includes(
                            result.document,
                        );
                        const snippetToShow = showFullSnippet
                            ? result.snippet
                            : result.snippet.substring(0, snippetLimit);
                        const remainingCharacters =
                            result.snippet.length - snippetLimit;

                        return (
                            <ResultContainer key={result.document}>
                                <ResultTitle>{`Result - ${
                                    index + 1
                                }`}</ResultTitle>
                                <SnippetContainer>
                                    {highlightSearchTerms(
                                        snippetToShow,
                                        query.trim(),
                                    )}
                                    {!showFullSnippet &&
                                        result.snippet.length > snippetLimit &&
                                        ' ... '}
                                    {result.snippet.length > snippetLimit && (
                                        <ShowMoreButton
                                            onClick={() =>
                                                toggleShowMore(result.document)
                                            }
                                        >
                                            {showFullSnippet
                                                ? 'Show less'
                                                : `Show ${remainingCharacters} more characters`}
                                        </ShowMoreButton>
                                    )}
                                </SnippetContainer>
                                <SourceActionContainer
                                    onClick={() => expand(result.document)}
                                >
                                    <ArrowIcon>
                                        {expanded.includes(result.document) ? (
                                            <DownOutlined />
                                        ) : (
                                            <RightOutlined />
                                        )}
                                    </ArrowIcon>
                                    {`Sources - ${
                                        result.occurrences
                                    } occurrence${
                                        result.occurrences > 1 ? 's' : ''
                                    } in total`}
                                    <HorizontalLine />
                                </SourceActionContainer>
                                {expanded.includes(result.document) ? (
                                    <SourceContainer>
                                        <BigIcon>
                                            <FilePdfOutlined />
                                        </BigIcon>

                                        <PDFLink
                                            href={`http://localhost:8000/get-pdf/${result.document}`}
                                            target="_blank"
                                        >
                                            {result.document}
                                        </PDFLink>
                                    </SourceContainer>
                                ) : null}
                            </ResultContainer>
                        );
                    })}
            {!loading &&
            searchResult &&
            searchResult.filter(
                (result: ResultItem) => result.snippet !== 'Snippet not found.',
            ).length === 0 ? (
                <NullText>
                    <BigIcon>
                        <FileUnknownOutlined />
                    </BigIcon>
                    <p>No results found</p>
                </NullText>
            ) : null}
        </Container>
    );
};

export default SearchResultDisplay;

const PDFLink = styled.a`
    text-decoration: none;
    color: ${(props) => props.theme.primaryColor};
`;

const ShowMoreButton = styled.button`
    color: ${(props) => props.theme.primaryColor};
    background: none;
    border: none;
    cursor: pointer;
    &:hover {
        text-decoration: underline;
    }
`;

const SnippetContainer = styled.div`
    position: relative;
`;

const NullText = styled.div`
    text-align: center;
    font-size: 20px;
    font-weight: 500;
    margin-top: 100px;
`;

const BigIcon = styled.div`
    font-size: 50px;
    color: ${(props) => props.theme.primaryColor};
`;

const SourceContainer = styled.div`
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 20px 40px;
`;

const ArrowIcon = styled.div``;

const SourceActionContainer = styled.div`
    display: flex;
    align-items: center;
    gap: 5px;
    cursor: pointer;
    color: ${(props) => props.theme.accentColor};
    font-size: 15px;
    margin-top: 20px;
`;

const HorizontalLine = styled.div`
    background-color: ${(props) => props.theme.accentColor};
    height: 1px;
    flex-grow: 1;
`;

const ResultTitle = styled.h3`
    color: ${(props) => props.theme.textColor};
`;

const ResultContainer = styled.div`
    box-shadow: rgba(0, 0, 0, 0.16) 0px 1px 4px;
    padding: 20px;
    margin: 30px 0;
    background-color: ${(props) => props.theme.backgroundColor};
    border-radius: 5px;
`;

const Container = styled.div``;
