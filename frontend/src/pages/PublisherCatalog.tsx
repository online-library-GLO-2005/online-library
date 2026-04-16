import { useEffect, useState } from 'react';
import type { Publisher } from '../types/publisher';
import { getPublishers } from '../services/publisherService';
import { Link } from 'react-router-dom';

function PublisherCatalog() {
  const [publishers, setPublishers] = useState<Publisher[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getPublishers()
      .then((data) => {
        setPublishers(data);
        setIsLoading(false);
      })
      .catch(() => {
        setError('Failed to load publishers.');
        setIsLoading(false);
      });
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 text-black p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">Publisher Catalog</h1>

        {isLoading ? (
          <div className="text-center text-gray-500 mt-20">Loading...</div>
        ) : error ? (
          <div className="text-center text-red-500 mt-20">{error}</div>
        ) : (
          <div className="space-y-3">
            {publishers.map((publisher) => (
              <Link
                to={`/publisher/${publisher.id}`}
                key={publisher.id}
                className="block"
              >
                <div className="flex items-center justify-between p-4 bg-white rounded-xl shadow-sm hover:shadow-md hover:scale-[1.01] transition">
                  <div className="font-semibold text-lg">{publisher.name}</div>

                  <div className="text-sm text-gray-500">View details →</div>
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default PublisherCatalog;
