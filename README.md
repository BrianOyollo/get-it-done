# GET-IT-DONE KENYA

## Description
**GET-IT-DONE KENYA** is a Reporting and Management API designed to facilitate the submission of reports on various issues encountered in Kenya. This API enables users to report problems such as poor leadership, road damages, corruption,etc., providing detailed descriptions, locations, and optional coordinates. The system visualizes and maps issues across the country, allowing for filtering by issue type.

## Features
- **Issue Reporting:** Submit detailed reports on various issues with descriptions and locations.
- **Issue Mapping:** Visualize reported issues on a map of Kenya.
- **Filtering:** Filter issues by type for better management and resolution.
- **JWT Authentication:** Secure API access using JSON Web Tokens (JWT).

## Tools and Technologies
- **Django:** A high-level Python web framework for building the API.
- **Django Ninja:** A web framework for building APIs with Django and Python 3.6+ type hints.
- **Ninja JWT:** A library for adding JWT authentication to Django Ninja APIs.
- **Ninja Extra:** A set of extra utilities for Django Ninja, enhancing its capabilities.

## Usage
- Access the API endpoints at the base URL: [https://get-it-done-jp49.onrender.com/api](https://get-it-done-jp49.onrender.com/api)
- View API documentation at: [https://get-it-done-jp49.onrender.com/api/docs](https://get-it-done-jp49.onrender.com/api/docs)

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/BrianOyollo/get-it-done
    cd get-it-done
    ```

2. Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Apply the database migrations:
    ```bash
    python manage.py migrate
    ```

5. Start the development server:
    ```bash
    python manage.py runserver
    ```

## Configuration
- **ALLOWED_HOSTS:** Add your domain to the `ALLOWED_HOSTS` setting in `settings.py`.
- **CSRF_TRUSTED_ORIGINS:** Add your API client domains to the `CSRF_TRUSTED_ORIGINS` setting in `settings.py`.


## Contributing
Contributions are welcome! Please follow these steps to contribute:
1. Fork the repository.
2. Create a new branch:
    ```bash
    git checkout -b feature-name
    ```
3. Make your changes and commit them:
    ```bash
    git commit -m "Add new feature"
    ```
4. Push to the branch:
    ```bash
    git push origin feature-name
    ```
5. Create a pull request.
   

## Contact
For any inquiries or feedback, please contact us at [oyollobrian@gmail.com](mailto:oyollobrian@gmail.com).
