import { useParams, useNavigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { toast } from 'react-hot-toast';

import type { Book } from '../types/book';
import type { Comment } from '../types/comment';
import type { Publisher } from '../types/publisher';

import {
  getBookById,
  getCommentsForBook,
  postCommentToBook,
  rateBook,
} from '../services/bookService';

import { modifyComment, deleteComment } from '../services/commentService';
import { getPublishersById } from '../services/publisherService';
import { useAuthStore } from '../store/authStore';
import {
  getFavorites,
  addFavorite,
  removeFavorite,
} from '../services/userService';

function BookDetail() {
  const { id } = useParams();
  const numId = Number(id);

  const navigate = useNavigate();

  const isLoggedIn = !!useAuthStore((state) => state.accessToken);
  const userId = useAuthStore((state) => state.id);

  const [book, setBook] = useState<Book | null>(null);
  const [comments, setComments] = useState<Comment[]>([]);
  const [publisher, setPublisher] = useState<Publisher | null>(null);

  const [isFavorite, setIsFavorite] = useState(false);
  const [input, setInput] = useState('');
  const [editInput, setEditInput] = useState('');
  const [hovered, setHovered] = useState(0);

  const [myComment, setMyComment] = useState<Comment | null>(null);
  const [editMode, setEditMode] = useState(false);

  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!numId) {
      setError('Invalid book id');
      setIsLoading(false);
      return;
    }

    setIsLoading(true);

    Promise.all([
      getBookById(numId),
      getCommentsForBook(numId),
      isLoggedIn ? getFavorites() : Promise.resolve(null),
    ])
      .then(([bookRes, commentsRes, favRes]) => {
        const bookData = bookRes?.data ?? bookRes;
        const commentsData = commentsRes?.data ?? commentsRes ?? [];

        setBook(bookData);
        setComments(commentsData);

        const mine = commentsData.find((c: Comment) => c.uid === userId);
        setMyComment(mine || null);
        if (mine) setEditInput(mine.message);

        if (favRes) {
          const favData = favRes.data ?? favRes;
          setIsFavorite(favData.some((b: Book) => b.id === numId));
        }

        if (!bookData) throw new Error('Book not found');
        return getPublishersById(bookData.eid);
      })
      .then((publisherData) => {
        setPublisher(publisherData);
      })
      .catch((err) => {
        console.error(err);
        setError('Failed to load book.');
      })
      .finally(() => {
        setIsLoading(false);
      });
  }, [numId, userId, isLoggedIn]);

  const handleRate = async (star: number) => {
    try {
      await rateBook(numId, star);
      toast.success(`Rated ${star} star(s)`);

      const updated = await getBookById(numId);
      setBook(updated.data ?? updated);
    } catch {
      toast.error('Failed to submit rating');
    }
  };

  const toggleFavorite = async () => {
    try {
      if (isFavorite) {
        await removeFavorite(numId);
        setIsFavorite(false);
        toast.success('Removed from favorites');
      } else {
        await addFavorite(numId);
        setIsFavorite(true);
        toast.success('Added to favorites');
      }

      const updated = await getBookById(numId);
      setBook(updated.data ?? updated);
    } catch {
      toast.error('Favorite action failed');
    }
  };

  const handleComment = async () => {
    if (!input.trim()) return;

    try {
      const res = await postCommentToBook(numId, input);
      setInput('');

      const updated = await getCommentsForBook(numId);
      const data = updated.data ?? updated;

      setComments(data);

      const mine = data.find((c: Comment) => c.uid === userId);
      setMyComment(mine || null);

      toast.success('Comment posted');
    } catch {
      toast.error('User has already commented');
    }
  };

  const handleUpdateComment = async () => {
    if (!myComment) return;

    try {
      await modifyComment(myComment.id, { message: editInput });

      const updated = await getCommentsForBook(numId);
      const data = updated.data ?? updated;

      setComments(data);

      const mine = data.find((c: Comment) => c.uid === userId);
      setMyComment(mine || null);

      setEditMode(false);

      toast.success('Comment updated');
    } catch {
      toast.error('Update failed');
    }
  };

  const handleDeleteComment = async () => {
    if (!myComment) return;

    try {
      await deleteComment(myComment.id);

      const updated = await getCommentsForBook(numId);
      const data = updated.data ?? updated;

      setComments(data);

      setMyComment(null);
      setEditInput('');
      setEditMode(false);

      toast.success('Comment deleted');
    } catch {
      toast.error('Delete failed');
    }
  };

  if (isLoading) {
    return <div className="text-center mt-20 text-gray-500">Loading...</div>;
  }

  if (error || !book) {
    return <div className="text-center mt-20 text-red-500">{error}</div>;
  }

  return (
    <div className="min-h-screen bg-gray-100 text-black">
      <div className="max-w-6xl mx-auto p-6 space-y-8">
        {/* HEADER CARD */}
        <div className="bg-white rounded-2xl shadow-md overflow-hidden flex flex-col md:flex-row">
          <div className="md:w-1/3 bg-gray-50 flex items-center justify-center p-6">
            <img
              src={book.cover_url}
              alt={book.title}
              className="w-full max-w-xs rounded-lg shadow object-cover"
            />
          </div>

          <div className="flex-1 p-6 space-y-4">
            <div className="flex justify-between items-start gap-4">
              <h1 className="text-2xl font-semibold leading-tight">
                {book.title}
              </h1>

              <div className="text-yellow-500 font-semibold whitespace-nowrap">
                ★ {book.rating ?? 'N/A'}
              </div>
            </div>

            <p className="text-gray-700 leading-relaxed">{book.description}</p>

            <hr className="border-gray-100" />

            {/* META */}
            <div className="text-sm text-gray-600 space-y-2">
              {book.authors?.length > 0 && (
                <div className="flex gap-2">
                  <span className="font-medium text-gray-700 shrink-0">
                    Authors:
                  </span>
                  <span>{book.authors.map((a) => a.nom).join(', ')}</span>
                </div>
              )}

              {book.genres?.length > 0 && (
                <div className="flex gap-2 items-start">
                  <span className="font-medium text-gray-700 shrink-0">
                    Genres:
                  </span>
                  <div className="flex flex-wrap gap-1.5">
                    {book.genres.map((g) => (
                      <span
                        key={g.id}
                        className="text-xs bg-gray-100 border px-2 py-0.5 rounded-full text-gray-600"
                      >
                        {g.nom}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              <div>
                <span className="font-medium text-gray-700">Publisher:</span>{' '}
                {publisher?.name}
              </div>

              <div>
                <span className="font-medium text-gray-700">Publication:</span>{' '}
                {book.pub_date}
              </div>

              <div>
                <span className="font-medium text-gray-700">ISBN:</span>{' '}
                {book.isbn}
              </div>
            </div>

            {isLoggedIn && (
              <div className="flex gap-3 pt-1">
                <button
                  onClick={toggleFavorite}
                  className={`px-4 py-2 rounded-md transition ${
                    isFavorite
                      ? 'bg-red-600 text-white hover:bg-red-700'
                      : 'bg-yellow-500 text-black hover:bg-yellow-600'
                  }`}
                >
                  {isFavorite ? 'Remove favorite' : 'Add to favorites'}
                </button>

                <button
                  onClick={() =>
                    navigate('/media-reader', {
                      state: { url: book.content_url },
                    })
                  }
                  className="bg-black text-white px-4 py-2 rounded-md hover:bg-gray-800 transition"
                >
                  Read book
                </button>
              </div>
            )}
          </div>
        </div>

        {/* RATING + COMMENT */}
        {isLoggedIn && (
          <div className="bg-white rounded-2xl shadow-md p-5 space-y-4">
            {/* RATING */}
            <div className="space-y-2">
              <div className="text-xs uppercase tracking-wide text-gray-400 font-medium">
                Rate this book
              </div>

              <div className="flex items-center gap-2">
                {[1, 2, 3, 4, 5].map((star) => (
                  <button
                    key={star}
                    onClick={() => setHovered(star)}
                    className={`text-2xl transition ${
                      star <= hovered ? 'text-yellow-400' : 'text-gray-300'
                    }`}
                  >
                    ★
                  </button>
                ))}

                <button
                  onClick={() => handleRate(hovered)}
                  disabled={hovered === 0}
                  className="ml-3 bg-blue-600 text-white px-3 py-1 rounded-md text-sm disabled:opacity-40"
                >
                  Submit rating
                </button>
              </div>
            </div>

            <hr className="border-gray-100" />

            {/* COMMENT */}
            <div className="space-y-2">
              <div className="text-xs uppercase tracking-wide text-gray-400 font-medium">
                {myComment ? 'Your comment' : 'Leave a comment'}
              </div>

              {myComment ? (
                editMode ? (
                  <div className="flex gap-2">
                    <input
                      value={editInput}
                      onChange={(e) => setEditInput(e.target.value)}
                      className="flex-1 border rounded-md px-3 py-2 text-sm"
                    />
                    <button
                      onClick={handleUpdateComment}
                      className="bg-green-600 text-white px-4 rounded-md"
                    >
                      Save
                    </button>
                  </div>
                ) : (
                  <div className="flex justify-between gap-3">
                    <p className="text-gray-800 flex-1 text-sm">
                      {myComment.message}
                    </p>

                    <div className="flex gap-3 text-sm">
                      <button
                        onClick={() => setEditMode(true)}
                        className="text-blue-600 hover:underline"
                      >
                        Edit
                      </button>
                      <button
                        onClick={handleDeleteComment}
                        className="text-red-600 hover:underline"
                      >
                        Delete
                      </button>
                    </div>
                  </div>
                )
              ) : (
                <div className="flex gap-2">
                  <input
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Write a comment..."
                    className="flex-1 border rounded-md px-3 py-2 text-sm"
                  />
                  <button
                    onClick={handleComment}
                    className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition"
                  >
                    Submit
                  </button>
                </div>
              )}
            </div>
          </div>
        )}

        {/* COMMENTS LIST */}
        <div className="bg-white rounded-2xl shadow-md overflow-hidden">
          <div className="px-5 py-3 border-b border-gray-100">
            <span className="text-xs uppercase tracking-wide text-gray-400 font-medium">
              Comments
            </span>
          </div>

          <div className="divide-y divide-gray-50">
            {comments.map((c) => (
              <div key={c.id} className="flex gap-4 px-5 py-4">
                <div className="w-36 shrink-0">
                  <div className="font-semibold text-sm">{c.user_name}</div>
                  <div className="text-xs text-gray-400 mt-0.5">
                    {c.date_publication}
                  </div>
                </div>

                <div className="text-gray-700 text-sm flex-1 leading-relaxed">
                  {c.message}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default BookDetail;
