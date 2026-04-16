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
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-6">Publisher Catalog</h1>
      {isLoading ? (
        <div className="text-center text-gray-500 mt-20">Loading...</div>
      ) : error ? (
        <div className="text-center text-red-500 mt-20">{error}</div>
      ) : (
        <div className="flex flex-col">
          {publishers.map((publisher) => (
            <Link to={`/publisher/${publisher.id}`} key={publisher.id}>
              <div className="flex flex-row rounded-lg shadow hover:shadow-lg transition cursor-pointer items-center gap-4 p-3">
                <div className="font-semibold">{publisher.name}</div>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}

export default PublisherCatalog;
