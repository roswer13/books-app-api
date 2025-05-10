# Books App API 📚

Books App API is a Django-based application that allows you to manage books, pages and users with specific roles. The API is designed to be scalable, secure and easy to use, using MySQL as database and following best development practices.

---

## **Características**

- **Book Management**: Create, update, list and delete books.
- **Page Management**: Associate pages to books, with uniqueness validation by page number within a book.
- **User Roles**:
    - **Reader**: Can read books and pages.
    - **Editor**: Can create, update and delete books and pages.
- **Pagination**: Support for pagination in book and page lists.
- **Validations**: Data validation such as uniqueness of pages per book.
- **Authentication**: Token-based to protect endpoints.

---

## **Technologies Used**

- **Backend**: Django and Django REST Framework.
- **Database**: MySQL.
- **Containers**: Docker and Docker Compose.
- **Testing**: Full coverage with `unittest` and API validations.
- **Documentation**: Automatically generated with `drf-spectacular`.

---

## **Prerequisites**
- Python 3.10 or higher.
- Docker and Docker Compose installed.
- MySQL 8.0 or higher (if not using Docker for the database).

---

## **Project Configuration** ⚙️

1. **Clone the Repository**
   ```bash
   git clone https://github.com/roswer13/books-app-api.git
   cd books-app-api
   ```

2. **Configure Environment Variables**

Create an .env file in the root directory with the following variables:

```bash
DB_NAME=devdb
DB_USER=devuser
DB_PASSWORD=devpassword
DB_HOST=db
DB_PORT=3306
```

3. **Build and Lift Containers**

Uses Docker Compose to build and lift services:

```bash
docker-compose up --build
```

4. **Apply Migrations**

Run the migrations to configure the database:
```bash
docker-compose run app sh -c "python manage.py migrate"
```

5. **Create Superuser (Optional)**

Si necesitas acceso administrativo, crea un superusuario:

```bash
docker-compose run app sh -c "python manage.py createsuperuser"
```

---

## **Principal Endpoints** 🚀
- **Books**:
  - `GET /api/book/books/`: List all books.
  - `POST /api/book/books/`: Create a new book.
  - `GET /api/book/books/{uuid}/`: Retrieve a specific book.
  - `PATCH /api/book/books/{uuid}/`: Update a specific book.
- **Pages**:
    - `GET /api/book/pages/`: List all pages.
    - `POST /api/book/pages/`: Create a new page.
    - `GET /api/book/pages/{uuid}/`: Retrieve a specific page.
    - `PATCH /api/book/pages/{uuid}/`: Update a specific page.
- **Authentication**:
    - `POST /api/user/tokern/`: Obtain a token for authentication.
    - `POST /api/user/refresh/`: Refresh the authentication token.
    - `GET /api/user/me/`: Retrieve the authenticated user's information.


## **API Documentation** 📖

The API documentation is automatically generated using `drf-spectacular`. You can access it at:

- **Swagger**: [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)


## **Testing** 🧪

To run the tests, execute the following command:

```bash
docker-compose run app sh -c "python manage.py test"
```
