import { useParams } from 'react-router-dom';
import { useState, useEffect } from 'react';
import type { Author } from '../types/author';
import { getAuthorsById } from '../services/authorService';

function AuthorDetail() {
  const { id } = useParams();
  const numId = Number(id);

  const [author, setAuthor] = useState<Author | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getAuthorsById(numId)
      .then((data) => {
        setAuthor(data);
        setIsLoading(false);
      })
      .catch(() => {
        setError('Failed to load author.');
        setIsLoading(false);
      });
  }, [numId]);

  return (
    <div className="min-h-screen bg-gray-100 text-black p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">Author Detail</h1>

        {isLoading ? (
          <div className="text-center text-gray-500 mt-20">Loading...</div>
        ) : error ? (
          <div className="text-center text-red-500 mt-20">{error}</div>
        ) : (
          <div className="bg-white rounded-2xl shadow p-6 flex flex-col md:flex-row gap-6">
            {author?.photo_url ? (
              <img
                src={author.photo_url}
                alt={author?.name}
                className="w-40 h-40 rounded-full object-cover border shadow-sm"
              />
            ) : (
              <div className="w-40 h-40 rounded-full bg-gray-200 flex items-center justify-center text-gray-500">
                No image
              </div>
            )}

            <div className="flex flex-col gap-3">
              <h2 className="text-2xl font-semibold">{author?.name}</h2>

              <p className="text-gray-700 leading-relaxed">
                {author?.description || 'No description available.'}
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default AuthorDetail;
