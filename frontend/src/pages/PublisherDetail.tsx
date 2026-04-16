import { useParams } from 'react-router-dom';
import { useState, useEffect } from 'react';
import type { Publisher } from '../types/publisher';
import { getPublishersById } from '../services/publisherService';

function PublisherDetail() {
  const { id } = useParams();
  const numId = Number(id);

  const [publisher, setPublisher] = useState<Publisher | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getPublishersById(numId)
      .then((data) => {
        setPublisher(data);
        setIsLoading(false);
      })
      .catch(() => {
        setError('Failed to load publisher.');
        setIsLoading(false);
      });
  }, [numId]);

  return (
    <div className="min-h-screen bg-gray-100 text-black p-8">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">Publisher Detail</h1>

        {isLoading ? (
          <div className="text-center text-gray-500 mt-20">Loading...</div>
        ) : error ? (
          <div className="text-center text-red-500 mt-20">{error}</div>
        ) : (
          <div className="bg-white rounded-2xl shadow p-6 space-y-4">
            <h2 className="text-2xl font-semibold">{publisher?.name}</h2>

            <p className="text-gray-700 leading-relaxed">
              {publisher?.description || 'No description available.'}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default PublisherDetail;
