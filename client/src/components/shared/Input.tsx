import {
    DesignComponentContainer,
    ErrorInputHelper,
    Label,
} from './design-system.styled';
import styled from 'styled-components';

import { Input as AntInput, InputRef } from 'antd';
import React from 'react';


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
    disabled?: boolean;
};

const Input = React.forwardRef<InputRef, Props>(({
    value,
    label,
    placeholder = '',
    onChange,
    name,
    type = 'text',
    prefix,
    error = '',
    containerStyle = {},
    disabled = false,
}, ref) => {
    return (
        <DesignComponentContainer style={containerStyle}>
            <Label>{label}</Label>
            <InputContainer>
                {type === 'password' && (
                    <AntInput.Password
                        ref={ref}
                        value={value}
                        prefix={prefix}
                        placeholder={placeholder}
                        onChange={onChange}
                        name={name}
                        type={type}
                        status={error ? 'error' : ''}
                        disabled={disabled}
                    />
                )}
                {type === 'text' && (
                    <AntInput
                        ref={ref}
                        value={value}
                        prefix={prefix}
                        placeholder={placeholder}
                        onChange={onChange}
                        name={name}
                        type={type}
                        status={error ? 'error' : ''}
                        disabled={disabled}
                    />
                )}
            </InputContainer>
            {error && <ErrorInputHelper>{error}</ErrorInputHelper>}
        </DesignComponentContainer>
    );
});

export default Input;

export const InputContainer = styled.div``;
