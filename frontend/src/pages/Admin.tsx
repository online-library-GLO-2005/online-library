import { useState, useEffect } from 'react';
import { getGenres, createGenre, deleteGenre } from "../services/genreService";
import { getBooks, postBook, updateBook, deleteBook, linkAuthorToBook, linkGenreToBook } from "../services/bookService";
import { getAuthors, createAuthor, updateAuthor, deleteAuthor } from "../services/authorService";
import { getPublishers, createPublisher, updatePublisher, deletePublisher } from "../services/publisherService";
import { uploadCover, uploadBook } from "../services/mediaService"
import type { Genre } from "../types/genre";
import type { Author } from "../types/author";
import type { Publisher } from "../types/publisher";
import type { Book } from "../types/book";


function Admin() {
  const [tab, setTab] = useState("books");
  const [genres, setGenres] = useState<Genre[]>([]);
  const [newGenre, setNewGenre] = useState({name: ""});
  const [authors, setAuthors] = useState<Author[]>([]);
  const [newAuthor, setNewAuthor] = useState({ nom: "", description: "" });
  const [publishers, setPublishers] = useState<Publisher[]>([]);
  const [newPublisher, setNewPublisher] = useState({ nom: "", description: "" });
  const [books, setBooks] = useState<Book[]>([]);
  const [newBook, setNewBook] = useState({ title: "", isbn: "", description: "", pub_date: "", eid: 0 });
  const [selectedAuthors, setSelectedAuthors] = useState<number[]>([]);
  const [selectedGenres, setSelectedGenres] = useState<number[]>([]);
  const [coverFile, setCoverFile] = useState<File | null>(null);
  const [bookFile, setBookFile] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([getGenres(), getAuthors(), getPublishers(), getBooks()])
        .then(([genresData, authorsData, publishersData, booksData]) => {
          setGenres(genresData);
          setAuthors(authorsData);
          setPublishers(publishersData);
          setBooks(booksData);
          setIsLoading(false);
        })
        .catch(() => {
          setError("Failed to load admin options.");
          setIsLoading(false);
        })
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 text-black p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">Author Catalog</h1>

        {isLoading ? (
          <div className="text-center text-gray-500 mt-20">Loading...</div>
        ) : error ? (
          <div className="text-center text-red-500 mt-20">{error}</div>
        ) : (
            <div>
              <div className="flex flex-row gap-4">
                <button onClick={() => setTab("books")}>Books</button>
                <button onClick={() => setTab("authors")}>Authors</button>
                <button onClick={() => setTab("genres")}>Genres</button>
                <button onClick={() => setTab("publishers")}>Publishers</button>
              </div>

              {tab === "books" && (
                  <div>
                      <div className="flex flex-col gap-2 mb-4">
                          <input type="text" placeholder="Title" value={newBook.title}
                            onChange={(e) => setNewBook({ ...newBook, title: e.target.value })}
                            className="border rounded p-2" />
                          <input type="text" placeholder="ISBN" value={newBook.isbn}
                            onChange={(e) => setNewBook({ ...newBook, isbn: e.target.value })}
                            className="border rounded p-2" />
                          <input type="text" placeholder="Description" value={newBook.description}
                            onChange={(e) => setNewBook({ ...newBook, description: e.target.value })}
                            className="border rounded p-2" />
                          <input type="date" placeholder="Publication date" value={newBook.pub_date}
                            onChange={(e) => setNewBook({ ...newBook, pub_date: e.target.value })}
                            className="border rounded p-2" />
                          <div>
                              <select
                                  onChange={(e) => {
                                      const id = Number(e.target.value);
                                      if (id && !selectedGenres.includes(id)) {
                                          setSelectedGenres([...selectedGenres, id]);
                                      }
                                      e.target.value = "0";
                                  }}
                                  className="border rounded p-2"
                              >
                                  <option value={0}>Add a genre</option>
                                  {genres
                                      .filter(g => !selectedGenres.includes(g.id))
                                      .map(genre => (
                                          <option key={genre.id} value={genre.id}>{genre.name}</option>
                                      ))}
                              </select>
                              <div className="flex flex-row flex-wrap gap-2 mt-2">
                                  {selectedGenres.map(id => {
                                      const genre = genres.find(g => g.id === id);
                                      return (
                                          <span key={id}
                                                className="flex items-center gap-1 bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-sm">
                                      {genre?.name}
                                              <button
                                                  onClick={() => setSelectedGenres(selectedGenres.filter(g => g !== id))}>✕</button>
                                    </span>
                                      );
                                  })}
                              </div>
                          </div>
                          <div>
                              <select
                                  onChange={(e) => {
                                      const id = Number(e.target.value);
                                      if (id && !selectedAuthors.includes(id)) {
                                          setSelectedAuthors([...selectedAuthors, id]);
                                      }
                                      e.target.value = "0";
                                  }}
                                  className="border rounded p-2"
                              >
                                  <option value={0}>Add an author</option>
                                  {authors
                                      .filter(a => !selectedAuthors.includes(a.id))
                                      .map(author => (
                                          <option key={author.id} value={author.id}>{author.name}</option>
                                      ))}
                              </select>
                              <div className="flex flex-row flex-wrap gap-2 mt-2">
                                  {selectedAuthors.map(id => {
                                      const author = authors.find(a => a.id === id);
                                      return (
                                          <span key={id}
                                                className="flex items-center gap-1 bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-sm">
                                      {author?.name}
                                              <button
                                                  onClick={() => setSelectedAuthors(selectedAuthors.filter(a => a !== id))}>✕</button>
                                    </span>
                                      );
                                  })}
                              </div>
                          </div>
                          <select
                              value={newBook.eid}
                              onChange={(e) => setNewBook({...newBook, eid: Number(e.target.value)})}
                              className="border rounded p-2"
                          >
                              <option value={0}>Select a publisher</option>
                              {publishers.map(publisher => (
                                  <option key={publisher.id} value={publisher.id}>
                                      {publisher.name}
                                  </option>
                              ))}
                          </select>
                          <label>Cover image:</label>
                          <input type="file" accept="image/*"
                            onChange={(e) => setCoverFile(e.target.files?.[0] ?? null)} />
                          <label>Book PDF:</label>
                          <input type="file" accept=".pdf"
                            onChange={(e) => setBookFile(e.target.files?.[0] ?? null)} />
                          <button onClick={async () => {
                            if (!coverFile || !bookFile) return;
                            const cover = await uploadCover(coverFile);
                            const book = await uploadBook(bookFile);
                            const newBookData = await postBook({
                              ...newBook,
                              cover_url: cover.url,
                              content_url: book.url,
                            } as any);
                            await Promise.all([
                              ...selectedAuthors.map(aid => linkAuthorToBook(newBookData.data.id, aid)),
                              ...selectedGenres.map(gid => linkGenreToBook(newBookData.data.id, gid)),
                            ]);
                            getBooks().then(data => setBooks(data));
                            setNewBook({ title: "", isbn: "", description: "", pub_date: "", eid: 0 });
                            setCoverFile(null);
                            setBookFile(null);
                          }}>
                            Add Book
                          </button>
                        </div>
                        <div className="flex flex-col gap-2">
                          {books.map(book => (
                            <div key={book.id} className="flex flex-row justify-between items-center p-3 rounded-lg shadow">
                              <div>
                                <div className="font-semibold">{book.title}</div>
                                <div className="text-sm text-gray-500">{book.isbn}</div>
                              </div>
                              <button onClick={() => {
                                deleteBook(book.id).then(() => {
                                  getBooks().then(data => setBooks(data));
                                });
                              }}>
                                Delete
                              </button>
                            </div>
                          ))}
                        </div>
                  </div>
              )}
              {tab === "authors" && (
                  <div>
                      <div className="flex flex-row gap-2 mb-4">
                          <input
                            type="text"
                            placeholder="Author name"
                            value={newAuthor.name}
                            onChange={(e) => setNewAuthor({ ...newAuthor, name: e.target.value })}
                            className="border rounded p-2"
                          />
                          <input
                            type="text"
                            placeholder="Description"
                            value={newAuthor.description}
                            onChange={(e) => setNewAuthor({ ...newAuthor, description: e.target.value })}
                            className="border rounded p-2"
                          />
                          <button onClick={() => {
                            createAuthor(newAuthor).then(() => {
                              getAuthors().then(data => setAuthors(data));
                              setNewAuthor({ name: "", description: "" });
                            });
                          }}>
                            Add
                          </button>
                        </div>
                      <div className="flex flex-col gap-2">
                          {authors.map(author => (
                            <div key={author.id} className="flex flex-row justify-between items-center p-3 rounded-lg shadow">
                              <div>
                                <div className="font-semibold">{author.name}</div>
                                <div className="text-sm text-gray-500">{author.description}</div>
                              </div>
                              <button onClick={() => {
                                deleteAuthor(author.id).then(() => {
                                  getAuthors().then(data => setAuthors(data));
                                });
                              }}>
                                Delete
                              </button>
                            </div>
                          ))}
                        </div>
                  </div>
              )}
              {tab === "genres" && (
                  <div>
                      <div className="flex flex-row gap-2 mb-4">
                          <input
                              type="text"
                              placeholder="Genre name"
                              value={newGenre.name}
                              onChange={(e) => setNewGenre({name:e.target.value})}
                              className="border rounded p-2"
                          />
                          <button onClick={() => {
                              createGenre(newGenre.name).then(() => {
                                    getGenres().then(data => setGenres(data));
                                    setNewGenre({ name: "" });
                              });
                            }}>
                              Add
                            </button>
                      </div>
                      <div className="flex flex-col gap-2">
                        {genres.map(genre => (
                          <div key={genre.id} className="flex flex-row justify-between items-center p-3 rounded-lg shadow">
                            <span>{genre.name}</span>
                            <button onClick={() => {
                              deleteGenre(genre.id).then(() => {
                                getGenres().then(data => setGenres(data));
                              });
                            }}>
                              Delete
                            </button>
                          </div>
                        ))}
                      </div>
                  </div>
              )}
              {tab === "publishers" && (
                  <div>
                     <div className="flex flex-row gap-2 mb-4">
                          <input
                            type="text"
                            placeholder="Publisher name"
                            value={newPublisher.name}
                            onChange={(e) => setNewPublisher({ ...newPublisher, name: e.target.value })}
                            className="border rounded p-2"
                          />
                          <input
                            type="text"
                            placeholder="Description"
                            value={newPublisher.description}
                            onChange={(e) => setNewPublisher({ ...newPublisher, description: e.target.value })}
                            className="border rounded p-2"
                          />
                          <button onClick={() => {
                            createPublisher(newPublisher).then(() => {
                              getPublishers().then(data => setPublishers(data));
                              setNewPublisher({ name: "", description: "" });
                            });
                          }}>
                            Add
                          </button>
                        </div>
                        <div className="flex flex-col gap-2">
                          {publishers.map(publisher => (
                            <div key={publisher.id} className="flex flex-row justify-between items-center p-3 rounded-lg shadow">
                              <div>
                                <div className="font-semibold">{publisher.name}</div>
                                <div className="text-sm text-gray-500">{publisher.description}</div>
                              </div>
                              <button onClick={() => {
                                deletePublisher(publisher.id).then(() => {
                                  getPublishers().then(data => setPublishers(data));
                                });
                              }}>
                                Delete
                              </button>
                            </div>
                          ))}
                        </div>
                  </div>
              )}
            </div>
        )}
      </div>
    </div>
  );
}

export default Admin;
