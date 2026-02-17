# Database Console Project

A Python console application for managing and interacting with a MySQL database.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [Project Structure](#project-structure)

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **MySQL Server 8.0+** - [Download MySQL](https://dev.mysql.com/downloads/mysql/)
- **pip** (Python package manager, usually comes with Python)

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd db-console-project
```

### 2. Create a Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the example environment file and configure your database credentials:

```bash
# Copy the example file
copy .env.example .env   # Windows
cp .env.example .env     # macOS/Linux
```

Edit the `.env` file with your MySQL credentials:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=your_database_name
```

## Database Setup

### Option 1: Using the Setup Script (Recommended)

Run the database setup script to automatically create the schema and seed data:

```bash
python src/setup_db.py
```

### Option 2: Manual Setup

If you prefer to set up the database manually:

1. **Create the database:**
   ```sql
   CREATE DATABASE your_database_name;
   ```

2. **Run the schema script:**
   ```bash
   mysql -u your_username -p your_database_name < sql/schema.sql
   ```

3. **Run the seed script:**
   ```bash
   mysql -u your_username -p your_database_name < sql/seed.sql
   ```

## Running the Application

Start the console application:

```bash
python src/app.py
```

## Project Structure

```
db-console-project/
  README.md               # This file - installation and setup guide
  requirements.txt        # Python dependencies
  .gitignore             # Files/folders Git should ignore
  .env.example           # Template for environment variables
  .env                   # Your local environment variables (not committed)

  sql/                   # SQL scripts
    schema.sql           # CREATE TABLE statements, constraints, triggers, procedures
    seed.sql             # INSERT statements for test/demo data

  src/                   # Python source code
    app.py               # Console UI entry point (menu, user input, output)
    db.py                # Database connection helper
    setup_db.py          # Script to initialize database (schema + seed)
    queries.py           # All SQL queries used by the application
```

## Troubleshooting

### Connection Issues

- Verify MySQL server is running
- Check your credentials in `.env`
- Ensure the database exists
- Verify the user has necessary permissions

### Import Errors

- Make sure you've activated your virtual environment
- Run `pip install -r requirements.txt` again

## License

This project is for educational purposes.