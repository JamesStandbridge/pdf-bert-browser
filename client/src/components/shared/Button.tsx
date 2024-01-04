import { Button as AntButton } from 'antd';
import {
    DesignComponentContainer,
    ErrorInputHelper,
} from './design-system.styled';

type Props = {
    children?: React.ReactNode;
    onClick?: (e: React.MouseEvent<HTMLElement>) => void;
    type?: 'link' | 'text' | 'default' | 'primary' | 'dashed' | undefined;
    block?: boolean;
    error?: string;
    margin?: string;
    disabled?: boolean;
};

const Button = ({
    children,
    onClick,
    type = 'primary',
    block = false,
    error = '',
    margin = '',
    disabled = false,
}: Props) => {
    return (
        <DesignComponentContainer $margin={margin}>
            <AntButton
                onClick={onClick}
                type={type}
                block={block}
                disabled={disabled}
                style={{
                    textTransform: 'uppercase',
                    fontWeight: 'bold',
                }}
            >
                {children}
            </AntButton>
            {error && <ErrorInputHelper>{error}</ErrorInputHelper>}
        </DesignComponentContainer>
    );
};

export default Button;
