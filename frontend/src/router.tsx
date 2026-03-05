import { createBrowserRouter } from "react-router-dom"
import App from "./App"
import Catalog from "./pages/Catalog"
import Login from "./pages/Login"
import BookDetail from "./pages/BookDetail"

export const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children: [
      { index: true, element: <Catalog /> },
      { path: "login", element: <Login /> },
      { path: "book/:id", element: <BookDetail /> },
    ],
  },
])