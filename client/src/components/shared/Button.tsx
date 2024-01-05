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
    icon?: React.ReactNode;
    style?: React.CSSProperties;
};

const Button = ({
    children,
    onClick,
    type = 'primary',
    block = false,
    error = '',
    margin = '',
    disabled = false,
    icon = null,
    style = {},
}: Props) => {
    return (
        <DesignComponentContainer $margin={margin}>
            <AntButton
                onClick={onClick}
                type={type}
                block={block}
                disabled={disabled}
                icon={icon}
                style={{
                    ...style,
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
