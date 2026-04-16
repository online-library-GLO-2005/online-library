import { Link } from 'react-router-dom';

export default function NotFound() {
  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center text-black p-6">
      <div className="text-center bg-white p-10 rounded-2xl shadow-md">
        <h1 className="text-6xl font-bold mb-4">404</h1>

        <p className="text-gray-600 mb-6">Page not found</p>

        <Link
          to="/"
          className="inline-block bg-blue-600 text-white px-5 py-2 rounded-md hover:bg-blue-700 transition"
        >
          Return to catalog
        </Link>
      </div>
    </div>
  );
}
