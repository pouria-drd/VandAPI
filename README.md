# VandAPI - Django REST Project

VandAPI is a Django-based RESTful API project designed for managing an online menu platform. This project includes user authentication, product and category management, and more. It uses Django, Django REST Framework, and other modern tools to build a scalable backend.

## Features

-   **User Authentication:** JWT-based authentication for secure access.
-   **Category Management:** Create, update, delete, and manage product categories.
-   **Product Management:** Full CRUD for product management.
-   **Image Handling:** Automatic image resizing and format validation for uploads.
-   **Admin Panel:** Django's built-in admin panel for easy management.

## Prerequisites

-   Python 3.12.4+
-   Django 5.1+
-   PostgreSQL (or SQLite for local development)

## Installation

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/pouria-drd/VandAPI.git
    cd VandAPI
    ```

2. **Create and Activate a Virtual Environment:**

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up Environment Variables:**

    Create a `.env` file in the project root and add the following:

    ```ini
    DEBUG=True
    SECRET_KEY=your_secret_key
    TIME_ZONE=UTC # your_time_zone
    INTERNAL_IPS=localhost,127.0.0.1 # your_allowed_hosts separate with comma
    ALLOWED_HOSTS=localhost,127.0.0.1 # your_allowed_hosts separate with comma
    CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000# separate with comma
    Category_ICON_MAX_SIZE=1 # your_max_size_in_MB

    DB_NAME=your_database_name
    DB_USER=your_database_user
    DB_PASSWORD=your_database_password
    DB_HOST=localhost
    DB_PORT=5432
    ```

5. **Run Migrations:**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6. **Create a Superuser:**

    ```bash
    python manage.py createsuperuser
    ```

7. **Run the Development Server:**

    ```bash
    python manage.py runserver
    ```

    Your project should now be running at `http://127.0.0.1:8000/`.

## API Endpoints

-   **User Authentication:**
    -   `POST /auth/token/`: Obtain JWT token.
    -   `POST /auth/token/refresh/`: Refresh JWT token.
-   **Category Management:**
    -   `GET /categories/`: List all categories.
    -   `POST /categories/`: Create a new category.
    -   `GET /categories/{slug}/`: Retrieve a category by slug.
    -   `PUT /categories/{slug}/`: Update a category.
    -   `DELETE /categories/{slug}/`: Delete a category.
-   **Product Management:**
    -   Similar CRUD endpoints as categories.

## Deployment

To deploy this project to a production environment:

1. **Set Up a Production Environment:**

    - Set `DEBUG=False` in the `.env` file.
    - Configure a production database.
    - Set up a web server like Gunicorn with Nginx.

2. **Collect Static Files:**

    ```bash
    python manage.py collectstatic
    ```

3. **Apply Migrations:**

    ```bash
    python manage.py migrate
    ```

4. **Run the Application with Gunicorn:**

    ```bash
    gunicorn VandAPI.wsgi:application --bind 0.0.0.0:8000
    ```

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature/your-feature`).
6. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries, please contact [your-email@example.com](mailto:your-email@example.com).
