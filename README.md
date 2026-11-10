# Module 10 – FastAPI User API with PostgreSQL

## Project Overview

This project extends a FastAPI calculator application by implementing user management functionality using Python, SQLAlchemy, PostgreSQL, and Pydantic.

The application supports user registration, secure password hashing, and retrieval of registered user information. Passwords are hashed using Argon2 before being stored in the PostgreSQL database. Pydantic schemas validate incoming user data and control the information returned through the API.

The project also demonstrates relational database management, Docker containerization, automated testing, and continuous integration and deployment (CI/CD) using GitHub Actions.

## Technologies Used

- **Python 3.14** – Programming language.
- **FastAPI** – Web framework used to build the API.
- **SQLAlchemy** – ORM used to interact with PostgreSQL.
- **PostgreSQL 16** – Relational database.
- **Pydantic** – Data validation and serialization.
- **Argon2** – Secure password hashing algorithm.
- **Docker** – Application containerization.
- **Docker Compose** – Container orchestration.
- **pgAdmin 4** – Database management interface.
- **Pytest** – Automated testing framework.
- **Playwright** – End-to-end browser testing.
- **GitHub Actions** – Continuous integration and deployment.
- **Trivy** – Docker image vulnerability scanning.
- **Docker Hub** – Container image repository.

## Application Features

### Calculator API

The original calculator application provides:

- Addition
- Subtraction
- Multiplication
- Division
- Division-by-zero error handling

### User Management API

The application includes user registration and retrieval endpoints.

| Method | Endpoint | Description |
|---|---|---|
| POST | `/users/register` | Register a new user |
| GET | `/users/` | Retrieve all users |
| GET | `/users/{user_id}` | Retrieve a user by ID |

### Password Security

User passwords are securely hashed using Argon2 before being stored in PostgreSQL.

The application uses the `pwdlib` library to generate and verify password hashes.

Plain-text passwords and password hashes are not included in API responses.

### Data Validation

Pydantic schemas validate user information before it is processed.

The `UserCreate` schema validates:

- Username length.
- Email format.
- Password length.

The `UserRead` schema controls the user information returned by the API and excludes password hashes.

## Database Design

The PostgreSQL database is named `fastapi_db`.

### Users Table

| Column | Data Type | Description |
|---|---|---|
| id | SERIAL PRIMARY KEY | Unique user identifier |
| username | VARCHAR(50) | Unique username |
| email | VARCHAR(100) | Unique email address |
| password_hash | VARCHAR(255) | Securely hashed password |
| created_at | TIMESTAMP | Account creation timestamp |

Both username and email have unique constraints to prevent duplicate registrations.

### Calculations Table

| Column | Data Type | Description |
|---|---|---|
| id | SERIAL PRIMARY KEY | Unique calculation identifier |
| operation | VARCHAR(20) | Calculator operation |
| operand_a | FLOAT | First operand |
| operand_b | FLOAT | Second operand |
| result | FLOAT | Calculation result |
| timestamp | TIMESTAMP | Calculation timestamp |
| user_id | INTEGER | References the associated user |

The calculations table has a foreign key referencing `users(id)`, establishing a one-to-many relationship between users and calculations.

The foreign key uses `ON DELETE CASCADE`.

## Running the Project with Docker Compose

### Prerequisites

Install the following before running the project:

- Docker Desktop
- Docker Compose
- Git

### 1. Clone the repository

```bash
git clone https://github.com/zca3-ui/Module-10-FastAPI-User-API.git
cd Module-10-FastAPI-User-API
```

### 2. Build and start the containers

```bash
docker compose up --build -d
```

This command builds the FastAPI application image and starts the three services.

| Service | Purpose | Port |
|---|---|---|
| web | FastAPI application | 8000 |
| db | PostgreSQL database | 5432 |
| pgadmin | Database management interface | 5050 |

### 3. Verify the containers

```bash
docker compose ps
```

Confirm that the application, PostgreSQL, and pgAdmin containers are running.

### 4. Access the application

- Calculator: http://localhost:8000
- FastAPI API documentation: http://localhost:8000/docs
- Health endpoint: http://localhost:8000/health
- pgAdmin: http://localhost:5050

## Connecting to PostgreSQL Through pgAdmin

Open pgAdmin at:

http://localhost:5050

Use the following default login credentials configured in Docker Compose:

- Email: `admin@example.com`
- Password: `admin`

Register a PostgreSQL server using the following connection information:

| Setting | Value |
|---|---|
| Server Name | FastAPI PostgreSQL |
| Host | db |
| Port | 5432 |
| Maintenance Database | fastapi_db |
| Username | postgres |
| Password | postgres |

The hostname is `db` because pgAdmin and PostgreSQL communicate through the Docker Compose network.

## Database Initialization and SQL Scripts

The SQL scripts are located in the `sql/` directory.

Execute the scripts in the following order when setting up a fresh database:

### 1. Create the database tables

File: `sql/01_schema.sql`

Creates the `users` and `calculations` tables, including their primary keys and foreign key relationship.

### 2. Insert sample data

File: `sql/02_sample_data.sql`

Inserts sample users Alice and Bob and three sample calculations associated with those users.

Run this script once on a fresh database. Running it again may create duplicate records or violate unique constraints.

### 3. Execute queries and CRUD operations

File: `sql/03_queries_and_crud.sql`

Demonstrates:

- SELECT statements to retrieve users and calculations.
- JOIN statements to connect calculations with their associated users.
- UPDATE statements to modify calculation records.
- DELETE statements to remove calculation records.

### 4. Add password hashing support

File: `sql/04_add_password_hash.sql`

Adds the `password_hash` column to the existing users table.

Existing users will have a NULL password hash until they register a password through the API.

## Running Automated Tests Locally

The project includes unit tests, integration tests, and end-to-end tests.

### 1. Navigate to the project directory

```bash
cd Module-10-FastAPI-User-API
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Start PostgreSQL

The integration tests require a running PostgreSQL database.

If using Docker Compose, start the database:

```bash
docker compose up -d db
```

The tests use the following default local database connection:

```text
postgresql+psycopg://postgres:postgres@localhost:5432/fastapi_db
```

### 5. Initialize the database

Run the following commands to create the database tables and add the password hash column:

```bash
docker exec -i postgres_db psql -U postgres -d fastapi_db < sql/01_schema.sql
```

```bash
docker exec -i postgres_db psql -U postgres -d fastapi_db < sql/04_add_password_hash.sql
```

### 6. Install the Playwright browser

```bash
playwright install chromium
```

###