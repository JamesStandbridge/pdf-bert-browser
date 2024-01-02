import styled from 'styled-components';
import Input from './Input';
import Button from './Button';

type Props = {
    query: string;
    onSearch: (e: any) => void;
    onQueryChange: (query: string) => void;
};

const SearchForm = ({ query, onSearch, onQueryChange }: Props) => {
    return (
        <Container onSubmit={onSearch}>
            <InputContainer>
                <Input
                    value={query}
                    onChange={(e) => onQueryChange(e.target.value)}
                    label={'Search query'}
                    name={'query'}
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
