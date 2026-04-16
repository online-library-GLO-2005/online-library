import { Link } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import { useAuth } from '../hooks/useAuth';

function Navbar() {
  const { name, email, accessToken, id: userId } = useAuthStore();
  const { logout } = useAuth();

  const isLoggedIn = !!accessToken;

  return (
    <nav className="bg-blue-600 px-6 py-4 flex justify-between items-center">
      <ul className="flex gap-6">
        <li>
          <Link className="text-white font-semibold hover:underline" to="/">
            Catalog
          </Link>
        </li>

        <li>
          <Link
            className="text-white font-semibold hover:underline"
            to="/author"
          >
            Authors
          </Link>
        </li>

        <li>
          <Link
            className="text-white font-semibold hover:underline"
            to="/publisher"
          >
            Publishers
          </Link>
        </li>

        {isLoggedIn && (
          <li>
            <Link
              className="text-white font-semibold hover:underline"
              to="/user/booklist"
            >
              My Books
            </Link>
          </li>
        )}

        {!isLoggedIn && (
          <li>
            <Link
              className="text-white font-semibold hover:underline"
              to="/auth"
            >
              Login
            </Link>
          </li>
        )}
      </ul>

      <div className="flex items-center gap-4 text-white">
        {isLoggedIn && (
          <>
            <Link className="text-sm" to={`user/${userId}`}>
              {name ? `Hi, ${name}` : email}
            </Link>

            <button
              onClick={logout}
              className="bg-red-500 px-3 py-1 rounded hover:bg-red-600"
            >
              Logout
            </button>
          </>
        )}
      </div>
    </nav>
  );
}

export default Navbar;
