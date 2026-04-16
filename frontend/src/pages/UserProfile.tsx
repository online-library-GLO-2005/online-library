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
    <div className="min-h-screen bg-white text-black p-6 space-y-6">
      {/* USER */}
      <div className="bg-white/10 p-4 rounded">
        <h1 className="text-xl font-semibold">{user.name || user.email}</h1>
        <p className="text-sm opacity-70">{user.email}</p>

        {user.is_admin && (
          <span className="text-xs bg-yellow-500 text-black px-2 py-1 rounded inline-block mt-2">
            Admin
          </span>
        )}
      </div>

      {/* FAVORITES */}
      <section>
        <h2 className="text-lg font-semibold mb-2">Favorites</h2>

        {(favorites?.length ?? 0) === 0 ? (
          <p className="opacity-70">No favorites</p>
        ) : (
          <ul className="space-y-2">
            {favorites.map((b) => (
              <li key={b.id} className="bg-white/5 p-2 rounded">
                {b.title}
              </li>
            ))}
          </ul>
        )}
      </section>

      {/* HISTORY */}
      <section>
        <h2 className="text-lg font-semibold mb-2">History</h2>

        {(books?.length ?? 0) === 0 ? (
          <p className="opacity-70">No history</p>
        ) : (
          <ul className="space-y-2">
            {books.map((b) => (
              <li key={b.id} className="bg-white/5 p-2 rounded">
                {b.title}
              </li>
            ))}
          </ul>
        )}
      </section>

      {/* COMMENTS */}
      <section>
        <h2 className="text-lg font-semibold mb-2">Comments</h2>

        {(comments?.length ?? 0) === 0 ? (
          <p className="opacity-70">No comments</p>
        ) : (
          <ul className="space-y-2">
            {comments.map((c) => (
              <li key={c.id} className="bg-white/5 p-2 rounded">
                {c.message}
              </li>
            ))}
          </ul>
        )}
      </section>
    </div>
  );
}

export default UserProfile;
