import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { URLs } from './router.constants';
import Browser from '../components/browser/Browser';
import Files from '../components/files/Files';
import MainLayout from '../components/layout/MainLayout';


type Props = {};

const Router = ({}: Props) => {
    return (
        <BrowserRouter>
            <Routes>
                <Route element={<MainLayout />}>
                    <Route path={URLs.BROWSER} element={<Browser />} />
                    <Route path={URLs.FILES} element={<Files />} />
                </Route>
            </Routes>
        </BrowserRouter>
    );
};

export default Router;