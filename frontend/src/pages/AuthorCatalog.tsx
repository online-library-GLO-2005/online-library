import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getAuthors } from '../services/authorService';
import type { Author } from '../types/author';

function AuthorCatalog() {
  const [authors, setAuthors] = useState<Author[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getAuthors()
      .then((data) => {
        setAuthors(data);
        setIsLoading(false);
      })
      .catch(() => {
        setError('Failed to load authors.');
        setIsLoading(false);
      });
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 text-black p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">Author Catalog</h1>

        {isLoading ? (
          <div className="text-center text-gray-500 mt-20">Loading...</div>
        ) : error ? (
          <div className="text-center text-red-500 mt-20">{error}</div>
        ) : (
          <div className="space-y-4">
            {authors.map((author) => (
              <Link
                to={`/author/${author.id}`}
                key={author.id}
                className="block"
              >
                <div className="flex items-center gap-4 p-4 bg-white rounded-xl shadow-sm hover:shadow-md hover:scale-[1.01] transition">
                  {author.photo_url ? (
                    <img
                      src={author.photo_url}
                      alt={author.name}
                      className="w-14 h-14 rounded-full object-cover border"
                    />
                  ) : (
                    <div className="w-14 h-14 rounded-full bg-gray-200 flex items-center justify-center text-gray-500 text-sm">
                      ?
                    </div>
                  )}

                  <div className="flex flex-col">
                    <span className="font-semibold text-lg">{author.name}</span>
                    <span className="text-sm text-gray-500">View profile</span>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default AuthorCatalog;
