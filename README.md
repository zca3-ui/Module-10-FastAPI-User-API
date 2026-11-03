# FastAPI Calculator with PostgreSQL and pgAdmin

## Project Overview

This project is a web-based calculator application built with FastAPI and Python. It extends a basic calculator application by using Docker Compose to manage the application, PostgreSQL database, and pgAdmin database management interface.

The project demonstrates how a web application and relational database environment can be organized using containers. It also demonstrates fundamental SQL operations, including creating tables, inserting records, retrieving data, joining tables, updating records, and deleting records.

## Technologies Used

- **Python 3.14** – Programming language used for the application.
- **FastAPI** – Web framework used to build the calculator API.
- **PostgreSQL 16** – Relational database used to store users and calculations.
- **pgAdmin 4** – Web-based interface for managing PostgreSQL databases.
- **Docker** – Used to package and run the application in containers.
- **Docker Compose** – Used to manage the application, database, and pgAdmin services.
- **Pytest** – Used for automated testing.
- **Playwright** – Used for end-to-end browser testing.
- **GitHub Actions** – Used for continuous integration and automated testing.


## Application Features

### Calculator Application

The FastAPI application provides the following calculator operations:

- Addition
- Subtraction
- Multiplication
- Division
- Division-by-zero error handling

The application also includes a web interface built with HTML and JavaScript.

### Database Design

The PostgreSQL database is named `fastapi_db` and contains two relational tables.

**Users Table**

| Column | Data Type | Description |
|---|---|---|
| id | SERIAL PRIMARY KEY | Unique user identifier |
| username | VARCHAR(50) | User's username |
| email | VARCHAR(100) | User's email address |
| created_at | TIMESTAMP | Date and time the user was created |

**Calculations Table**

| Column | Data Type | Description |
|---|---|---|
| id | SERIAL PRIMARY KEY | Unique calculation identifier |
| operation | VARCHAR(20) | Calculator operation |
| operand_a | FLOAT | First operand |
| operand_b | FLOAT | Second operand |
| result | FLOAT | Calculation result |
| timestamp | TIMESTAMP | Date and time of calculation |
| user_id | INTEGER | References the associated user |

The `calculations` table contains a foreign key referencing `users(id)`. This establishes a one-to-many relationship because one user can have multiple calculations.

The foreign key uses `ON DELETE CASCADE`, meaning calculations associated with a deleted user are automatically deleted as well.

## Running the Project with Docker Compose

### Prerequisites

Install the following before running the project:

- Docker Desktop
- Docker Compose
- Git (if cloning the repository)

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd fastapi-postgresql-assignment
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with the actual URL of your GitHub repository.

### 2. Build and start the containers

Run:

```bash
docker compose up --build -d
```

This command builds the FastAPI application image and starts the three services:

| Service | Purpose | Port |
|---|---|---|
| web | FastAPI calculator application | 8000 |
| db | PostgreSQL database | 5432 |
| pgadmin | Database management interface | 5050 |

### 3. Verify the containers

Run:

```bash
docker compose ps
```

Confirm that the application, PostgreSQL, and pgAdmin containers are running.

### 4. Access the application

- Calculator application: http://localhost:8000
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

## Running the SQL Scripts

The SQL scripts are located in the `sql/` directory.

Execute them through the pgAdmin Query Tool in the following order:

### 1. Create the database tables

File: `sql/01_schema.sql`

Creates the `users` and `calculations` tables, including the primary key and foreign key relationships.

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

These scripts demonstrate the database operations performed for the assignment.

## Running Automated Tests

The project includes unit, integration, and end-to-end tests.

### Install dependencies

Create and activate a Python virtual environment, then run:

```bash
pip install -r requirements.txt
```

### Install the Playwright browser

```bash
playwright install chromium
```

### Run unit tests

```bash
pytest tests/unit/ -v
```

### Run integration tests

```bash
pytest tests/integration/ -v
```

### Run end-to-end tests

```bash
pytest tests/e2e/ -v
```

### Run the complete test suite

```bash
pytest -v
```

## Continuous Integration

The project includes a GitHub Actions workflow located at:

`.github/workflows/test.yml`

The workflow is configured to run automated tests when changes are pushed to the main branch or when a pull request targets the main branch. It also includes a Docker image security scanning job.

## Stopping the Containers

To stop the running services while preserving the database volumes, run:

```bash
docker compose down
```

To stop the services and remove the database and pgAdmin volumes, run:

```bash
docker compose down -v
```



## Conclusion

This project demonstrates the use of FastAPI, PostgreSQL, pgAdmin, Docker, and Docker Compose in a containerized application environment. It provides practical experience with relational database design, primary and foreign keys, one-to-many relationships, SQL CRUD operations, API development, and automated software testing.