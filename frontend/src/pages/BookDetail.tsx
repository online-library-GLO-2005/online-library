import { useParams, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import type {Book} from "../types/book";
import type {Comment} from "../types/comment";
import {getBookById, getCommentsForBook, postCommentToBook} from "../services/bookService";
import type {Publisher} from "../types/publisher";
import {getPublishersById} from "../services/publisherService";
import {useAuthStore} from "../store/authStore";

function BookDetail() {
  const { id } = useParams();
  const numId = Number(id);

  const accessToken = useAuthStore(state => state.accessToken);
  const navigate = useNavigate();

  const [book, setBook] = useState<Book | null>(null);
  const [comments, setComments] = useState<Comment[]>([]);
  const [publisher, setPublisher] = useState<Publisher | null>(null);
  const [input, setInput] = useState<string>('');
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
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-6">Book Detail</h1>
      {isLoading ? (
        <div className="text-center text-gray-500 mt-20">Loading...</div>
      ) : error ? (
        <div className="text-center text-red-500 mt-20">{error}</div>
      ) : (
        <div>
          <div className="flex flex-row">
              <img src={book?.cover_url} alt={book?.title} />
                <div className="flex flex-col">
                  <div className="flex flex-row">
                    <h2>{book?.title}</h2>
                    <div>★ {book?.rating ?? "N/A"}</div>
                  </div>
                  <div>Description: {book?.description}</div>
                  <div>Genre(s):</div>
                    {book?.genres.map(genre => (
                        <span key={genre.id}>{genre.name}</span>
                    ))}
                  <div>Author(s):</div>
                    {book?.authors.map(author => (
                        <span key={author.id}>{author.name}</span>
                    ))}
                  <div>Publisher: {publisher?.name}</div>
                  <div>Publication Date: {book?.pub_date}</div>
                  <div>ISBN: {book?.isbn}</div>
                  {accessToken && <button onClick={() => navigate("/media-reader", {state: {url: book?.content_url}})}>Read {book?.title}</button>}
                </div>
          </div>
          <div>
            {accessToken && (
              <div>
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Write a comment..."
                />
                <button
                  onClick={() => {
                    postCommentToBook(numId, input).then(() => {
                      setInput('');
                      getCommentsForBook(numId).then((data) =>
                        setComments(data),
                      );
                    });
                  }}
                >
                  Submit
                </button>
              </div>
            )}
            <div className="flex flex-col">
              {comments.map((comment) => (
                <div
                  className="flex flex-row rounded-lg shadow hover:shadow-lg transition cursor-pointer items-center gap-4 p-3"
                  key={comment.id}
                >
                  <div>
                    <div className="font-semibold">{comment.user_name}</div>
                    <div>{comment.date_publication}</div>
                  </div>
                  <div>{comment.message}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default BookDetail;
