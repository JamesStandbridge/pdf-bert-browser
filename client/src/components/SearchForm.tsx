import { useRef, useEffect } from 'react';
import styled from 'styled-components';
import Input from './Input';
import Button from './Button';
import { InputRef } from 'antd';

type Props = {
    query: string;
    onSearch: (e: any) => void;
    onQueryChange: (query: string) => void;
};

const SearchForm = ({ query, onSearch, onQueryChange }: Props) => {
    const inputRef = useRef(null);

    useEffect(() => {
        const handleKeyDown = (e) => {
            if (e.ctrlKey && e.shiftKey && e.code === 'KeyF') {
                e.preventDefault();
                inputRef.current && (inputRef.current as InputRef).focus();
            }
        };

        window.addEventListener('keydown', handleKeyDown);

        return () => {
            window.removeEventListener('keydown', handleKeyDown);
        };
    }, []);

    return (
        <Container onSubmit={onSearch}>
            <InputContainer>
                <Input
                    ref={inputRef}
                    value={query}
                    onChange={(e) => onQueryChange(e.target.value)}
                    label={'Search query'}
                    name={'query'}
                    placeholder='Ctrl+Shift+F to search'
                    containerStyle={{ width: '100%' }}
                />
                <Button onClick={onSearch}>search</Button>
            </InputContainer>
        </Container>
    );
};

export default SearchForm;

const Container = styled.form``;

const InputContainer = styled.div`
    display: flex;
    justify-content: center;
    align-items: end;
    width: 100%;
`;
