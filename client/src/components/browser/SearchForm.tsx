import { useRef, useEffect } from 'react';
import styled from 'styled-components';
import Input from '../shared/Input';
import Button from '../shared/Button';
import { InputRef } from 'antd';
import { SearchOutlined } from '@ant-design/icons';

type Props = {
    query: string;
    onSearch: (e: any) => void;
    onQueryChange: (query: string) => void;
    loading: boolean;
};

const SearchForm = ({ query, onSearch, onQueryChange, loading }: Props) => {
    const inputRef = useRef(null);

    useEffect(() => {
        const handleKeyDown = (e: { ctrlKey: any; shiftKey: any; code: string; preventDefault: () => void; }) => {
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

    useEffect(() => {
        if(!loading) {
            inputRef.current && (inputRef.current as InputRef).focus();
        }
    }, [loading]);

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
                    disabled={loading}
                />
                <Button 
                    disabled={loading}
                    onClick={onSearch}>
                    <SearchOutlined /> search
                </Button>
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
