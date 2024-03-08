# REST Contact Book API

This project provides a RESTful API for a contact book application, allowing users to manage their contact information through a web interface. Built using Flask and Flask_SQLAlchemy, it features a clean, straightforward design intended for educational purposes and small-scale personal use.

## Features

- **CRUD Operations**: Create, read, update, and delete contacts in your personal contact book.
- **Search Functionality**: Easily find contacts by name or email.
- **User Authentication**: Secure your contacts with basic authentication methods.
- **Docker Support**: Run your application within a Docker container for easy deployment.

## Tech Stack

- **Flask**: A lightweight WSGI web application framework.
- **Flask_SQLAlchemy**: An extension for Flask that adds support for SQLAlchemy.
- **Flask_Smorest**: Flask extension to build APIs with Flask and marshmallow.
- **Pipenv**: A tool for managing dependencies and virtual environments.
- **Docker**: A set of platform-as-a-service products that use OS-level virtualization to deliver software in packages called containers.

## Getting Started

### Prerequisites

- Python 3.7+
- Pipenv

### Installation

First, clone the repository to your local machine:

```bash
git clone https://github.com/amnotme/REST_ContactBookAPI.git
cd REST_ContactBookAPI
```
Use Pipenv to create a virtual environment and install the necessary dependencies:

```bash
pipenv install
```

Activate the virtual environment:

```bash
pipenv shell
```

### Setting Up the Database

Before running the application, you need to set up the database:

in `config/config.py` you can specify another `sqlite3` db name

```bash
SQLALCHEMY_DATABASE_URI = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
```

Alternatively you are able to provide the uri to your preferred db instance (beyond the scope of this README)

### Running the Application locally

Start the Flask application with the following command:

```bash
flask run
```
You can set up debug mode by adding a `.flaskenv` file at the root of the app directory and placing the debug option to true

```bash
FLASK_APP=app
FLASK_DEBUG=1
```
The API will be accessible at http://127.0.0.1:5000/.

### Usage

you are able to access the documentation via the include swagger endpoint http://127.0.0.1:5000/swagger-ui. 

### Docker Deployment
To containerize your Flask application, follow these steps:

1. Build the Docker image:

```bash
docker build -t rest_contact_book_api .
```
2. Run the Docker container:

```bash
docker container run --rm -v "$(pwd):/app" -p 5001:5000 rest_contact_book_api  # this will allow for hot-reloading
```
**NOTE** Now, the API should be available at http://localhost:5001/.

### Acknowledgments
Flask documentation for providing comprehensive guides and tutorials.
Contributors and maintainers of Flask_SQLAlchemy and Flask_Smorest for their invaluable tools.


