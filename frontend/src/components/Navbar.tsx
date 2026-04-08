import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <nav className="bg-blue-600 px-6 py-4">
      <ul className="flex gap-6">
        <li>
          <Link className="text-white font-semibold hover:underline" to="/">
            Catalog
          </Link>
        </li>
        <li>
          <Link
            className="text-white font-semibold hover:underline"
            to="/login"
          >
            Login
          </Link>
        </li>
        <li>
          <Link
            className="text-white font-semibold hover:underline"
            to="/book/:id"
          >
            Book
          </Link>
        </li>
      </ul>
    </nav>
  );
}

export default Navbar;
