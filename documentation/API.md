This is the imagined APIs endpoints needed.
Update this if there's a smarter and better way:

```md
/auth
    POST /login
    POST /signup
    POST /logout
    POST /refresh   # protected, For access token generation

/users
    GET /                           # Get all users, query params
    GET /:id
    GET /me                         # JWT required
    GET /me/comments                # protected, get all user comments, allow query as well (like search by book id or book name)
    GET /me/books                   # protected, my saved books
    POST /me/books                  # protected, save a book
    DELETE /me/books/:id            # protected,remove a saved book
    PUT /:id                        # protected, admin and ownership checked in service layer
    DELETE /:id                     # protected, admin and ownership checked in service layer

/books
    GET /                           # Get all books, query params (like searching for genre names). Also return bookmarks if user logged in
    GET /:id                        # Also returns info about bookmark if user logged in.
    POST /                          # Admin required
    PUT /:id                        # Admin required
    DELETE /:id                     # Admin required
    GET /:id/comments               # get comments for a book
    POST /:id/comments              # create a comment

/comments
    PUT /:id                        # protected, admin and ownership checked in sesrvice layer
    DELETE /:id                     # protected, admin and ownership checked in service layer

/genres
    GET /                           # Get all genres, queries with params (Like unique name)
    GET /:id                        # Get genre by id
    POST /                          # Admin required, Create genre
    PUT /:id                        # Admin required, update
    DELETE /:id                     # Admin required

/authors
    GET /                           # Get all author, queries with params
    GET /:id                        # Get author by id
    POST /                          # Admin required, Create author
    PUT /:id                        # Admin required
    DELETE /:id                     # Admin required
    
/publishers
    GET /                           # Get all publishers, queries with params
    GET /:id                        # Get publishers by id
    POST /                          # Admin required, Create publishers
    PUT /:id                        # Admin required, update publishers
    DELETE /:id                     # Admin required

/search
    GET /?q=...          # search across books, authors, genres, publishers, users

/media
    GET /books/:filename    # Serves uploaded book files (PDF, etc.)
    GET /covers/:filename   # Serves uploaded cover images
    POST /books/            # Upload a book file (admin only)
    POST /covers/           # Upload a cover image (admin only)
```

Frontend flow:
```
1. Admin uploads PDF    → POST /media/books   → gets back url_contenu
2. Admin uploads cover  → POST /media/covers  → gets back url_couverture
3. Admin creates book   → POST /books         → sends all fields including both urls
```