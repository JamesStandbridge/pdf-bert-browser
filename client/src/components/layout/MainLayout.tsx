import { Outlet, useNavigate } from 'react-router-dom';
import styled from 'styled-components';

import { SearchOutlined, FilePdfOutlined } from '@ant-design/icons';
import Button from '../shared/Button';
import { resetFiles } from '../../API/repository/file-repository';

type Props = {};

const MainLayout = ({}: Props) => {
    const navigate = useNavigate();

    const reset = () => {
        resetFiles();
        navigate('/');
    }

    return (
        <>
            <MenuContainer>
                <Section>
                    <Logo>PDF Fast Search</Logo>
                    <MenuItem onClick={() => navigate("/")}>
                        <SearchOutlined />
                        Browser
                    </MenuItem>
                    <MenuItem onClick={() => navigate("/files")}>
                        <FilePdfOutlined />
                        Files
                    </MenuItem>
                </Section>
                <Section>
                    <Button margin="0" onClick={reset}>Reset</Button>
                </Section>
            </MenuContainer>
            <Container>
                <Content>
                    <Outlet />
                </Content>
            </Container>
        </>
    );
};

export default MainLayout;

const Section = styled.div`
    display: flex;
    align-items: center;
    gap: 20px;
`;



const Content = styled.div`
    width: 80%;
    padding-top: 20px;
`;

const Container = styled.div`
    width: 100%;
    display: flex;
    height: calc(100vh - 30px);
    justify-content: center;
`;

const MenuContainer = styled.div`
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 20px 40px;
    background-color: ${props => props.theme.primaryColor};
    color: white;
`;

const Logo = styled.div`
    font-weight: bolder;
    font-size: 20px;
`;

const MenuItem = styled.div`
    cursor: pointer; 
    display: flex; 
    align-items: center;
    gap: 10px;
    font-weight: 600;

    &:hover {
        color: ${props => props.theme.accentColor};
    }
`;