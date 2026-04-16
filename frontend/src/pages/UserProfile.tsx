import { useEffect, useState } from 'react';
import {
  getCurrentUser,
  getCurrentUserBookList,
  getFavorites,
  getCurrentUserComments,
} from '../services/userService';

import type { User } from '../types/user';
import type { Book } from '../types/book';
import type { Comment } from '../types/comment';

function UserProfile() {
  const [user, setUser] = useState<User | null>(null);
  const [books, setBooks] = useState<Book[]>([]);
  const [favorites, setFavorites] = useState<Book[]>([]);
  const [comments, setComments] = useState<Comment[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const [u, b, f, c] = await Promise.all([
          getCurrentUser(),
          getCurrentUserBookList(),
          getFavorites(),
          getCurrentUserComments(),
        ]);

        setUser(u);

        setBooks(Array.isArray(b) ? b : []);
        setFavorites(Array.isArray(f) ? f : []);
        setComments(Array.isArray(c) ? c : []);
      } catch (err) {
        console.error('UserProfile error:', err);
        setBooks([]);
        setFavorites([]);
        setComments([]);
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, []);

  if (loading) return <div className="text-white p-4">Loading...</div>;
  if (!user) return <div className="text-red-500 p-4">User not found</div>;

  return (
    <div className="min-h-screen bg-gray-100 text-black p-6">
      <div className="max-w-5xl mx-auto space-y-8">
        <div className="bg-gradient-to-r from-blue-600 to-blue-500 text-white rounded-2xl p-6 shadow-md">
          <h1 className="text-2xl font-bold">{user.name || user.email}</h1>
          <p className="text-sm opacity-80">{user.email}</p>

          {user.is_admin && (
            <span className="inline-block mt-3 text-xs bg-yellow-300 text-black px-2 py-1 rounded">
              Admin
            </span>
          )}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <section className="bg-white rounded-xl shadow p-5 border-l-4 border-pink-500">
            <h2 className="text-lg font-semibold mb-3">Favorites</h2>

            {(favorites?.length ?? 0) === 0 ? (
              <p className="text-gray-500">No favorites yet</p>
            ) : (
              <div className="space-y-2">
                {favorites.map((b) => (
                  <div
                    key={b.id}
                    className="p-2 rounded hover:bg-pink-50 transition"
                  >
                    {b.title}
                  </div>
                ))}
              </div>
            )}
          </section>

          <section className="bg-white rounded-xl shadow p-5 border-l-4 border-green-500">
            <h2 className="text-lg font-semibold mb-3">History</h2>

            {(books?.length ?? 0) === 0 ? (
              <p className="text-gray-500">No history yet</p>
            ) : (
              <div className="space-y-2">
                {books.map((b) => (
                  <div
                    key={b.id}
                    className="p-2 rounded hover:bg-green-50 transition"
                  >
                    {b.title}
                  </div>
                ))}
              </div>
            )}
          </section>
        </div>

        <section className="bg-white rounded-xl shadow-md p-5">
          <h2 className="text-lg font-semibold mb-4">Comments</h2>

          {(comments?.length ?? 0) === 0 ? (
            <p className="text-gray-500">No comments</p>
          ) : (
            <div className="space-y-4">
              {comments.map((c) => (
                <div key={c.id} className="border-b pb-3 last:border-none">
                  <div className="flex justify-between text-sm text-gray-600">
                    <span className="font-medium text-black">
                      {c.user_name}
                    </span>
                    <span>{c.date_publication}</span>
                  </div>

                  <p className="mt-1">{c.message}</p>
                </div>
              ))}
            </div>
          )}
        </section>
      </div>
    </div>
  );
}

export default UserProfile;
