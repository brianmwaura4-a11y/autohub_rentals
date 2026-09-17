# AutoHub Car Rental Management System

##  Project Description

AutoHub is a Python-based Command-Line Interface (CLI) application for managing a car rental business.

The system allows customers to register, log in, view available cars, rent cars, view their rental history, cancel rentals, and return cars.

Administrators can manage users, cars, and rentals through an administrator menu.

The project uses JSON files for persistent data storage and follows a modular structure separating models, services, CLI commands, utilities, and data.


##  Project Objectives

The main objectives of AutoHub are to:

* Provide a simple car rental management system.
* Implement user authentication and login.
* Allow customers to rent and return vehicles.
* Allow administrators to manage users and vehicles.
* Store application data persistently using JSON files.
* Validate user, car, and rental information.
* Provide automated tests using pytest.
* Measure test coverage using pytest-cov.
* Demonstrate object-oriented programming and modular Python development.


##  Features

### Authentication

* Customer registration
* Administrator registration
* User login
* Password hashing
* Logout
* Case-insensitive username lookup
* Duplicate username prevention
* Role-based access

### Customer Features

Customers can:

* View available cars
* Rent a car
* View their rentals
* View individual rental details
* Cancel an active rental
* Return a rented car
* Log out

### Administrator Features

Administrators can:

* View all users
* View individual users
* Change user roles
* Delete users
* View all cars
* Add cars
* Delete cars
* View all rentals
* Log out

### Car Management

Each car contains:

* Car ID
* Make
* Model
* Year
* Registration number
* Daily rental rate
* Status

Supported car statuses:

* `Available`
* `Rented`
* `Maintenance`

### Rental Management

Each rental contains:

* Rental ID
* User ID
* Car ID
* Start date
* End date
* Total cost
* Rental status

Supported rental statuses:

* `Active`
* `Completed`
* `Cancelled`


##  Technologies Used

* Python 3
* Object-Oriented Programming
* `argparse`
* JSON
* Pytest
* Pytest-Cov
* Werkzeug
* Git
* GitHub

### External Packages

| Package    | Purpose                                    |
| ---------- | ------------------------------------------ |
| Werkzeug   | Password hashing and password verification |
| pytest     | Automated testing                          |
| pytest-cov | Test coverage                              |

---

## Project Structure

```text
autohub_rentals/
│
├── README.md
├── requirements.txt
├── pyproject.toml
├── .gitignore
│
├── car_rental/
│   ├── __init__.py
│   ├── __main__.py
│   │
│   ├── cli/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── auth_commands.py
│   │   ├── car_commands.py
│   │   ├── rental_commands.py
│   │   ├── admin_commands.py
│   │   └── menu.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── car.py
│   │   └── rental.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── car_service.py
│   │   └── rental_service.py
│   │
│   ├── data/
│   │   ├── __init__.py
│   │   ├── users.json
│   │   ├── cars.json
│   │   └── rentals.json
│   │
│   └── utils/
│       ├── __init__.py
│       ├── json_handler.py
│       ├── validation.py
│       └── helpers.py
│
└── tests/
    ├── __init__.py
    ├── test_auth.py
    ├── test_auth_commands.py
    ├── test_auth_service.py
    ├── test_user.py
    ├── test_cars.py
    ├── test_car_commands.py
    ├── test_rentals.py
    ├── test_rental_commands.py
    ├── test_json_handler.py
    ├── test_validation.py
    ├── test_helpers.py
    ├── test_admin_commands.py
    ├── test_main.py
    ├── test_menu.py
    └── test_main_module.py
```

---

##  Installation

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
```

Navigate into the project:

```bash
cd autohub_rentals
```

### 2. Create and activate a virtual environment

You can use Python's built-in virtual environment:

```bash
python -m venv .venv
```

Activate it on Linux/WSL:

```bash
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

---

##  Running the Application

AutoHub is run as a Python module.

### Display help

```bash
python -m car_rental --help
```

### Register a customer

```bash
python -m car_rental register brian password123
```

### Register an administrator

```bash
python -m car_rental register-admin admin password123
```

### Login

```bash
python -m car_rental login admin password123
```

After a successful login, the appropriate menu will be displayed based on the user's role.


##  User Roles

The system supports four roles:

| Role          | Description                     |
| ------------- | ------------------------------- |
| Customer      | Rent and manage cars            |
| Rental Staff  | Rental-related operational role |
| Administrator | Manage users, cars, and rentals |
| Maintenance   | Vehicle maintenance role        |

Administrators have access to the administrator menu.

Customers are directed to the customer menu after logging in.


##  Rental Process

The basic rental workflow is:

```text
Customer Login
      ↓
View Available Cars
      ↓
Select Car
      ↓
Enter Rental Dates
      ↓
System Validates Information
      ↓
Calculate Rental Cost
      ↓
Create Rental
      ↓
Car Status → Rented
```

When a car is returned:

```text
Return Car
    ↓
Rental Status → Completed
    ↓
Car Status → Available
```

If a rental is cancelled:

```text
Cancel Rental
      ↓
Rental Status → Cancelled
      ↓
Car Status → Available
```


##  Data Persistence

AutoHub uses JSON files to store application data.

### Users

```text
car_rental/data/users.json
```

### Cars

```text
car_rental/data/cars.json
```

### Rentals

```text
car_rental/data/rentals.json
```

The application uses a reusable JSON handler that provides:

* Reading JSON data
* Writing JSON data
* Adding records
* Updating records
* Deleting records

This keeps file operations separate from the business logic.


##  Authentication

Passwords are not stored as plain text.

AutoHub uses Werkzeug password hashing:

```python
generate_password_hash()
check_password_hash()
```

When a user registers, their password is converted into a secure password hash before being stored in `users.json`.

During login, the entered password is checked against the stored hash.


##  Validation

The system validates:

* Usernames
* Passwords
* User roles
* Car information
* Car year
* Registration numbers
* Daily rental rates
* Rental dates
* Rental status
* Car status

Examples of validation rules include:

* Username must be at least 3 characters.
* Password must be at least 6 characters.
* Daily rental rate must be greater than zero.
* Car registration numbers must be unique.
* Rental end date cannot be before the start date.
* A rented car cannot be deleted.
* A car must be available before it can be rented.


##  Testing

The project uses **pytest** for automated testing.

Run the complete test suite:

```bash
pytest -v
```

Tests cover major parts of the application, including:

* Authentication
* User model
* Car model
* Rental model
* Authentication commands
* Car commands
* Rental commands
* Administrator commands
* Menus
* JSON handling
* Validation
* Helper functions
* Main CLI
* Application entry point


##  Test Coverage

Test coverage can be measured using `pytest-cov`.

Run:

```bash
pytest --cov=car_rental --cov-report=term-missing
```

This displays:

* Number of statements
* Number of missed statements
* Coverage percentage
* Lines that are not covered by tests

### Generate an HTML coverage report

```bash
pytest --cov=car_rental --cov-report=html
```

The report will be created in:

```text
htmlcov/
```

Open the report with:

```bash
xdg-open htmlcov/index.html
```


##  Resetting Application Data

For development or testing purposes, the JSON data can be reset.

**Warning:** This deletes the current application data stored in the three JSON files.

```bash
echo "[]" > car_rental/data/users.json
echo "[]" > car_rental/data/cars.json
echo "[]" > car_rental/data/rentals.json
```


##  Development Workflow

The project was developed using Git and GitHub.

Typical workflow:

```bash
git status
git add .
git commit -m "Describe your changes"
git push
```

Feature development can be done using separate branches:

```bash
git checkout -b feature-name
```

After completing the feature, tests should be run before creating a pull request.



##  Learning Outcomes

This project demonstrates practical understanding of:

* Python programming
* Object-oriented programming
* Classes and objects
* Functions
* Modules and packages
* Exception handling
* Input validation
* JSON file handling
* CRUD operations
* Authentication
* Password hashing
* Command-line interfaces
* `argparse`
* Automated testing
* Test coverage
* Git and GitHub
* Modular software design


##  Team

**AutoHub Car Rental Management System**

Developed as a Python end-of-module group project.

### Team Members

* Member 1 — [Name]
* Member 2 — [Name]
* Member 3 — [Name]
* Member 4 — [Name]


##  License

This project was developed for educational purposes as part of a Python software development course.

