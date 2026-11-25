# User Stories: Book Service

These user stories and acceptance criteria specifies the **Book Service 
REST API** at `http://localhost:9090/books` .

A **book** has these attributes:

| Attribute | Type | Description                    |
|-----------|------|--------------------------------|
| `oid`     | int  | Unique identifier of the book  |
| `author`  | str  | Name of the author             |
| `title`   | str  | Title of the book              |
| `isbn`    | str  | ISBN of the book               |

**Initial data set** (what the tests expect before they run):

| oid | author          | title               | isbn           |
|-----|-----------------|---------------------|----------------|
| 1   | Eric Matthes    | Python Crash Course | 978-1718502703 |
| 2   | Brett Slatkin   | Effective Python    | 978-0134853987 |
| 3   | Luciano Ramalho | Fluent Python       | 978-1492056355 |

---

## US-1: Find a book by its ID

**As a** user of the book service
**I want to** get a single book by its ID
**so that** I can see the details of that book.

### Acceptance Criteria

- **AC-1.1** Given a book with ID `1` exists,
  when I request the book with ID `1`,
  then I get a book with:
  - `oid` = `1`
  - `author` = `Eric Matthes`
  - `title` = `Python Crash Course`
  - `isbn` = `978-1718502703`
- **AC-1.2** The request finishes without an HTTP error.

### Manual Test

```bash
curl -i http://localhost:9090/books/1
```

Expected: `HTTP/1.1 200 OK` and a JSON body with `"id": 1`, `"author": "Eric Matthes"`,
`"title": "Python Crash Course"` and `"isbn": "978-1718502703"`.


## US-2: List all books

**As a** user of the book service
**I want to** get a list of all books
**so that** I can see every book that is available.

### Acceptance Criteria

- **AC-2.1** Given the initial data set,
  when I request all books,
  then I get exactly **3** books.
- **AC-2.2** The books come back in the order they were stored:
  the first book has `oid` = `1`, the second `oid` = `2`, the third `oid` = `3`.
- **AC-2.3** The request finishes without an HTTP error.

### Manual Test

```bash
curl -i http://localhost:9090/books
```

Expected: `HTTP/1.1 200 OK` and a JSON body `{"data": [...]}` with 3 books, ordered by
`id` 1, 2, 3.


## US-3: Add a new book

**As a** user of the book service
**I want to** add a new book
**so that** the collection includes it.

### Acceptance Criteria

- **AC-3.1** Given a new book with
  `oid` = `7`, `author` = `Wes McKinney`, `title` = `Python for Data Analysis`,
  `isbn` = `978-1098104030`,
  when I add the book,
  then the request finishes without an HTTP error (the service responds with `201 Created`).

### Manual Test

```bash
curl -i -X POST http://localhost:9090/books \
     -H "Content-Type: application/json" \
     -d '{"id": 7, "author": "Wes McKinney", "title": "Python for Data Analysis", "isbn": "978-1098104030"}'
```

Expected: `HTTP/1.1 201 Created` and the new book as JSON. To check that the book was stored,
run `curl -i http://localhost:9090/books/7`.


## US-4: Update an existing book

**As a** user of the book service
**I want to** change the details of an existing book
**so that** its data stays correct.

### Acceptance Criteria

- **AC-4.1** Given a book with ID `2` exists,
  when I update it with
  `author` = `Brett Slatkin`, `title` = `Effective Python`, `isbn` = `0134853989`,
  then the request finishes without an HTTP error (the service responds with `200 OK`).
- **AC-4.2** The book ID (`oid`) identifies which book is updated and does not change.

### Manual Test

```bash
curl -i -X PUT http://localhost:9090/books/2 \
     -H "Content-Type: application/json" \
     -d '{"author": "Brett Slatkin", "title": "Effective Python", "isbn": "0134853989"}'
```

Expected: `HTTP/1.1 200 OK` and the updated book as JSON, still with `"id": 2` and now with
`"isbn": "0134853989"`. To check the change, run `curl -i http://localhost:9090/books/2`.

_Egon Teiniker, 2025-2026, GPL v3.0_ 