import { createBrowserRouter } from 'react-router-dom';
import App from './App';

import Catalog from './pages/Catalog';
import Auth from './pages/Auth';
import BookDetail from './pages/BookDetail';
import BookReader from './pages/BookReader';
import UserSettings from './pages/UserSettings';
import UserProfile from './pages/UserProfile';
import AuthorCatalog from './pages/AuthorCatalog';
import AuthorDetail from './pages/AuthorDetail';
import PublisherCatalog from './pages/PublisherCatalog';
import PublisherDetail from './pages/PublisherDetail';
import Admin from './pages/Admin';
import NotFound from './pages/NotFound';

import { RequireAdmin, RequireAuth, RequireGuest } from './routes/guards';

export const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    children: [
      { index: true, element: <Catalog /> },

      // guest only
      {
        path: 'auth',
        element: (
          <RequireGuest>
            <Auth />
          </RequireGuest>
        ),
      },

      { path: 'book/:id', element: <BookDetail /> },
      { path: 'media-reader', element: <BookReader /> },

      // auth only
      {
        path: 'user/settings',
        element: (
          <RequireAuth>
            <UserSettings />
          </RequireAuth>
        ),
      },
      {
        path: 'user/me',
        element: (
          <RequireAuth>
            <UserProfile />
          </RequireAuth>
        ),
      },
      {
        path: 'user/me',
        element: (
          <RequireAuth>
            <UserProfile />
          </RequireAuth>
        ),
      },

      { path: 'author', element: <AuthorCatalog /> },
      { path: 'author/:id', element: <AuthorDetail /> },
      { path: 'publisher', element: <PublisherCatalog /> },
      { path: 'publisher/:id', element: <PublisherDetail /> },

      {
        path: 'admin',
        element: (
          <RequireAdmin>
            <Admin />
          </RequireAdmin>
        ),
      },

      // fallback
      { path: '*', element: <NotFound /> },
    ],
  },
]);
