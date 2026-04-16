import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getBooks } from '../services/bookService';
import type { Book } from '../types/book';

function Catalog() {
  const [books, setBooks] = useState<Book[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getBooks()
      .then((data) => {
        setBooks(data);
        setIsLoading(false);
      })
      .catch(() => {
        setError('Failed to load books.');
        setIsLoading(false);
      });
  }, []);

  return (
    <div className="p-8 max-w-7xl mx-auto text-black">
      <h1 className="text-3xl font-bold mb-6">Book Catalog</h1>

      {isLoading ? (
        <div className="text-center text-gray-500 mt-20">Loading...</div>
      ) : error ? (
        <div className="text-center text-red-500 mt-20">{error}</div>
      ) : (
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-6">
          {books.map((book) => (
            <Link to={`/book/${book.id}`} key={book.id}>
              <div className="bg-white rounded-xl shadow hover:shadow-lg transition overflow-hidden cursor-pointer h-full flex flex-col">
                <img
                  src={book.cover_url}
                  alt={book.title}
                  className="w-full h-64 object-cover"
                />

                <div className="p-3 flex flex-col gap-2 flex-1">
                  <div className="font-semibold text-sm line-clamp-2">
                    {book.title}
                  </div>

                  {/* To be implemented */}
                  {/* <div className="flex flex-wrap gap-1 text-xs text-gray-600">
                    {(book?.authors ?? []).map((author) => (
                      <span key={author.id}>{author.name}</span>
                    ))}
                  </div>

                  <div className="flex flex-wrap gap-1 text-xs text-gray-500">
                    {(book?.genres ?? []).map((genre) => (
                      <span key={genre.id}>{genre.name}</span>
                    ))}
                  </div> */}

                  <div className="text-yellow-500 text-sm font-medium mt-auto">
                    ★ {book.rating ?? 'N/A'}
                  </div>
                </div>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}

export default Catalog;
