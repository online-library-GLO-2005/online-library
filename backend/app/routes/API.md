This is the imagined APIs endpoints needed.
Update this if there's a smarter and better way:

> Also every Get all should have queries with params.

```md
/auth
    POST /login
    POST /signup
    POST /logout
    POST /refresh

/users
    GET /:id
    PUT /:id
    DELETE /:id
    GET /:id/books   # optional if you want user-specific libraries

/library
    /books
        GET /            # list books
        GET /:id         # single book
        POST /           # create book
        PUT /:id
        DELETE /:id
        /comments/:id    # nested or separate comments endpoint

    /genres
        GET /, POST /, etc.

    /authors
        GET /, POST /, etc.

    /publishers
        GET /, POST /, etc.

/search
    GET /?q=...          # search across books, authors, genres, publishers, users
```