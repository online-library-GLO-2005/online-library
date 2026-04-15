import { createBrowserRouter } from "react-router-dom"
import App from "./App"
import Catalog from "./pages/Catalog"
import Login from "./pages/Login"
import BookDetail from "./pages/BookDetail"
import BookReader from "./pages/BookReader";
import UserSettings from "./pages/UserSettings";
import UserSavedBooks from "./pages/UserSavedBooks";
import UserProfile from "./pages/UserProfile";
import AuthorCatalog from "./pages/AuthorCatalog";
import AuthorDetail from "./pages/AuthorDetail";
import PublisherCatalog from "./pages/PublisherCatalog";
import PublisherDetail from "./pages/PublisherDetail";
import Admin from "./pages/Admin";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children: [
      { index: true, element: <Catalog /> },
      { path: "login", element: <Login /> },
      { path: "book/:id", element: <BookDetail /> },
      { path: "media-reader/:filename", element: <BookReader />},
      { path: "user/settings", element: <UserSettings />},
      { path: "user/booklist", element: <UserSavedBooks />},
      { path: "user/:id", element: <UserProfile />},
      { path: "author", element: <AuthorCatalog />},
      { path: "author/:id", element: <AuthorDetail />},
      { path: "publisher", element: <PublisherCatalog />},
      { path: "publisher/:id", element: <PublisherDetail />},
      { path: "admin", element: <Admin />}
    ],
  },
])