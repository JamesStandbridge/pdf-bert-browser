import {
    DesignComponentContainer,
    ErrorInputHelper,
    Label,
} from './design-system.styled';
import styled from 'styled-components';

type Props = {
    value: string;
    label: string;
    placeholder?: string;
    onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
    name: string;
    type?: 'text' | 'password' | 'number';
    prefix?: React.ReactNode;
    error?: string;
    containerStyle?: React.CSSProperties;
};

import { Input as AntInput } from 'antd';

const Input = ({
    value,
    label,
    placeholder = '',
    onChange,
    name,
    type = 'text',
    prefix,
    error = '',
    containerStyle = {},
}: Props) => {
    return (
        <DesignComponentContainer style={containerStyle}>
            <Label>{label}</Label>
            <InputContainer>
                {type === 'password' && (
                    <AntInput.Password
                        value={value}
                        prefix={prefix}
                        placeholder={placeholder}
                        onChange={onChange}
                        name={name}
                        type={type}
                        status={error ? 'error' : ''}
                    />
                )}
                {type === 'text' && (
                    <AntInput
                        value={value}
                        prefix={prefix}
                        placeholder={placeholder}
                        onChange={onChange}
                        name={name}
                        type={type}
                        status={error ? 'error' : ''}
                    />
                )}
            </InputContainer>
            {error && <ErrorInputHelper>{error}</ErrorInputHelper>}
        </DesignComponentContainer>
    );
};

export default Input;

export const InputContainer = styled.div``;
