import styled from 'styled-components';

export const highlightSearchTerms = (text: string, searchQuery: string) => {
    const isExactSearch =
        searchQuery.startsWith('"') && searchQuery.endsWith('"');
    let regex: any;

    if (isExactSearch) {
        const exactQuery = searchQuery.replace(/^"|"$/g, '');
        regex = new RegExp(`(${escapeRegExp(exactQuery)})`, 'gi');
    } else {
        const keywords = searchQuery.split(/\s+/).map(escapeRegExp);
        regex = new RegExp(`(${keywords.join('|')})`, 'gi');
    }

    const parts = text.split(regex);

    return (
        <>
            {parts.map((part, index) =>
                regex.test(part) ? (
                    <Highlight key={index}>{part}</Highlight>
                ) : (
                    part
                ),
            )}
        </>
    );
};

function escapeRegExp(text: string) {
    return text.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

const Highlight = styled.span`
    background-color: yellow;
`;
