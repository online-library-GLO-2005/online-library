import { useParams, useNavigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import type { Book } from '../types/book';
import type { Comment } from '../types/comment';
import {
  getBookById,
  getCommentsForBook,
  postCommentToBook,
  rateBook
} from '../services/bookService';
import type { Publisher } from '../types/publisher';
import { getPublishersById } from '../services/publisherService';
import { useAuthStore } from '../store/authStore';

function BookDetail() {
  const { id } = useParams();
  const numId = Number(id);

  const accessToken = useAuthStore((state) => state.accessToken);
  const navigate = useNavigate();

  const [book, setBook] = useState<Book | null>(null);
  const [comments, setComments] = useState<Comment[]>([]);
  const [publisher, setPublisher] = useState<Publisher | null>(null);
  const [input, setInput] = useState<string>('');
  const [hovered, setHovered] = useState<number>(0);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([getBookById(numId), getCommentsForBook(numId)])
      .then(([book, comments]) => {
        setBook(book);
        setComments(comments);
        getPublishersById(book.eid).then((data) => {
          setPublisher(data);
          setIsLoading(false);
        });
      })
      .catch(() => {
        setError('Failed to load book.');
        setIsLoading(false);
      });
  }, [numId]);

  return (
    <div className="p-8 max-w-6xl mx-auto text-black">
      <h1 className="text-3xl font-bold mb-6">Book Detail</h1>

      {isLoading ? (
        <div className="text-center text-gray-500 mt-20">Loading...</div>
      ) : error ? (
        <div className="text-center text-red-500 mt-20">{error}</div>
      ) : (
        <div className="space-y-10">
          <div className="flex flex-col md:flex-row gap-8 bg-white rounded-xl shadow p-6">
            <img
              src={book?.cover_url}
              alt={book?.title}
              className="w-64 h-auto rounded-lg shadow object-cover"
            />
            <div className="flex flex-col gap-3 flex-1">
              <div className="flex items-start justify-between">
                <h2 className="text-2xl font-semibold">{book?.title}</h2>

                <div className="text-yellow-500 font-semibold">
                  ★ {book?.rating ?? 'N/A'}
                </div>
              </div>

              <p className="text-gray-700">{book?.description}</p>

              <div>
                <h3 className="font-semibold">Genres</h3>
                <div className="flex flex-wrap gap-2 mt-1">
                  {book?.genres.map((genre) => (
                    <span
                      key={genre.id}
                      className="bg-gray-200 px-2 py-1 rounded text-sm"
                    >
                      {genre.nom}
                    </span>
                  ))}
                </div>
              </div>

              <div>
                <h3 className="font-semibold">Authors</h3>
                <div className="flex flex-wrap gap-2 mt-1">
                  {book?.authors.map((author) => (
                    <span key={author.id} className="text-sm text-gray-700">
                      {author.nom}
                    </span>
                  ))}
                </div>
              </div>

              <div className="text-sm text-gray-600 space-y-1">
                <div>
                  <span className="font-medium">Publisher:</span>{' '}
                  {publisher?.name}
                </div>
                <div>
                  <span className="font-medium">Publication:</span>{' '}
                  {book?.pub_date}
                </div>
                <div>
                  <span className="font-medium">ISBN:</span> {book?.isbn}
                </div>
              </div>

              {accessToken && (
                <button
                  onClick={() =>
                    navigate('/media-reader', {
                      state: { url: book?.content_url },
                    })
                  }
                  className="mt-4 bg-black text-white px-4 py-2 rounded hover:bg-gray-800 transition w-fit"
                >
                  Read book
                </button>
              )}
            </div>
          </div>
          {accessToken && (
            <div className="bg-white rounded-xl shadow p-4 flex gap-2">
              <div className="flex flex-row">
                {[1, 2, 3, 4, 5].map(star => (
                    <span
                        key={star}
                        className={`text-sxl cursor-pointer ${star <= hovered? "text-yellow-400" : "text-gray-300"}`}
                        onMouseEnter={() => setHovered(star)}
                        onMouseLeave={() => setHovered(0)}
                        onClick={() => {
                          rateBook(numId, star);
                        }}
                    >
                      ★
                    </span>
                ))}
              </div>
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Write a comment..."
                className="flex-1 border rounded px-3 py-2"
              />

              <button
                onClick={() => {
                  postCommentToBook(numId, input).then(() => {
                    setInput('');
                    getCommentsForBook(numId).then(setComments);
                  });
                }}
                className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
              >
                Submit
              </button>
            </div>
          )}
          <div className="space-y-3">
            {comments.map((comment) => (
              <div
                key={comment.id}
                className="bg-white rounded-lg shadow p-4 flex justify-between items-start gap-4 hover:shadow-md transition"
              >
                <div className="min-w-32">
                  <div className="font-semibold">{comment.user_name}</div>
                  <div className="text-xs text-gray-500">
                    {comment.date_publication}
                  </div>
                </div>

                <div className="flex-1 text-gray-800">{comment.message}</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default BookDetail;
