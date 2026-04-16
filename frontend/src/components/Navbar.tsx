import { Link, useLocation } from 'react-router-dom';
import { useState } from 'react';
import { useAuthStore } from '../store/authStore';
import { useAuth } from '../hooks/useAuth';

function Navbar() {
  const { name, email, accessToken, is_admin } = useAuthStore(); // add is_admin if you store it
  const { logout } = useAuth();
  const location = useLocation();

  const [open, setOpen] = useState(false);

  const isLoggedIn = !!accessToken;

  const linkClass = (path: string) =>
    `font-semibold px-2 py-1 rounded transition ${
      location.pathname === path ? 'bg-white/20' : 'hover:opacity-80'
    }`;

  return (
    <nav className="sticky top-0 z-50 bg-blue-600 px-6 py-4 flex justify-between items-center text-white shadow-md">
      <div className="flex gap-8">
        <Link to="/" className={linkClass('/')}>
          Catalog
        </Link>
        <Link to="/author" className={linkClass('/author')}>
          Authors
        </Link>
        <Link to="/publisher" className={linkClass('/publisher')}>
          Publishers
        </Link>
      </div>

      <div className="flex items-center gap-4">
        {!isLoggedIn ? (
          <Link
            to="/auth"
            className="bg-white text-blue-600 px-4 py-1.5 rounded-md font-medium hover:bg-gray-100 transition"
          >
            Login
          </Link>
        ) : (
          <div className="relative">
            <button
              onClick={() => setOpen(!open)}
              className="px-3 py-1 rounded-md hover:bg-white/10 transition font-medium"
            >
              {name ? `Hi, ${name}` : email}
            </button>

            {open && (
              <div className="absolute right-0 mt-2 w-40 bg-white text-black rounded-md shadow-md overflow-hidden">
                <Link
                  to="/user/me"
                  onClick={() => setOpen(false)}
                  className="block px-4 py-2 hover:bg-gray-100"
                >
                  Profile
                </Link>

                {is_admin && (
                  <Link
                    to="/admin"
                    onClick={() => setOpen(false)}
                    className="block px-4 py-2 hover:bg-gray-100"
                  >
                    Admin
                  </Link>
                )}

                <button
                  onClick={() => {
                    setOpen(false);
                    logout();
                  }}
                  className="w-full text-left px-4 py-2 hover:bg-gray-100 text-red-600"
                >
                  Logout
                </button>
              </div>
            )}
          </div>
        )}
      </div>
    </nav>
  );
}

export default Navbar;
