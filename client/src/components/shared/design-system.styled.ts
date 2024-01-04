import styled from 'styled-components';
import { DesignComponentContainerProps } from './design-system.type';

export const Label = styled.p`
    margin: 0;
    font-size: 15px;
    margin-bottom: 5px;
    color: #464646;
`;

export const DesignComponentContainer = styled.div<DesignComponentContainerProps>`
    margin: ${(props) => (props.$margin ? props.$margin : '25px 0')};
`;

export const WordSeparator = styled.div`
    display: flex;
    align-items: center;
    text-align: center;
    color: ${(props) => props.theme.lightPrimaryColor};
    margin: 20px 0;
    font-weight: bold;

    &::before,
    &::after {
        content: '';
        flex: 1;
        border-bottom: 1px solid ${(props) => props.theme.lightPrimaryColor};
    }

    &::before {
        margin: 0 10px 0 0;
    }

    &::after {
        margin: 0 0 0 10px;
    }
`;

export const TextLink = styled.a`
    cursor: pointer;
    color: ${(props) => props.theme.primaryColor};
    &:hover {
        text-decoration: underline;
    }
`;

export const ErrorInputHelper = styled.p`
    color: #ff4d4f;
    margin: 0;
    font-size: 12px;
    margin-top: 5px;
    margin-bottom: -18px;
`;

export const FlexLine = styled.div`
    display: flex;
    align-items: center;
    justify-content: space-between;
`;

export const FlexCenter = styled.div`
    display: flex;
    align-items: center;
    justify-content: center;
`;
