# Employee Management API with FastAPI and MongoDB

A RESTful API for managing employee data built with FastAPI, MongoDB, and featuring pagination, search, and analytics capabilities.

## 🚀 Features

- **CRUD Operations**: Create, read, update, and delete employee records
- **Pagination**: Efficient listing with pagination support
- **Search & Filter**: Filter by department and search by skills
- **Analytics**: Average salary calculation by department
- **Data Validation**: Comprehensive Pydantic schema validation
- **Database Indexing**: Optimized MongoDB queries with proper indexing
- **Date Handling**: Proper date storage and retrieval
- **Error Handling**: Comprehensive HTTP error responses

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **Database**: MongoDB with Motor async driver
- **Validation**: Pydantic with custom validators
- **API Documentation**: Automatic Swagger UI and ReDoc

## 📦 Installation

1. **Clone the repository**
```bash
   git clone https://github.com/Shadaab-005/Python-MongoDB-Assessment
   cd Python-MongoDB-Assessment
```



2\. **Create a virtual environment**
```bash
python -m venv venv
source venv\Scripts\activate
```

3\. **Install dependencies**
```bash

   pip install -r requirements.txt

```

4\. **Set up MongoDB**

   - Install MongoDB locally or use MongoDB Atlas

   - Update the connection string in `db.py` if needed

5\. **Run the application**
```bash

   uvicorn main:app --reload
```

## 📋 API Endpoints

### Employees Management

| Method | Endpoint | Description | Auth Required |

|--------|----------|-------------|---------------|

| `POST` | `/employees` | Create a new employee | No |

| `GET` | `/employees` | List employees with pagination | No |

| `GET` | `/employees/{employee_id}` | Get employee by ID | No |

| `PUT` | `/employees/{employee_id}` | Update employee | No |

| `DELETE` | `/employees/{employee_id}` | Delete employee | No |

### Search & Analytics

| Method | Endpoint | Description | Auth Required |

|--------|----------|-------------|---------------|

| `GET` | `/employees/search` | Search employees by skill | No |

| `GET` | `/employees/avg-salary` | Get average salary by department | No |

## 🔧 Usage Examples

### Create an Employee

```bash

curl -X POST "http://localhost:8000/employees"

  -H "Content-Type: application/json"

  -d '{

    "employee_id": "E001",

    "name": "John Doe",

    "department": "Engineering",

    "salary": 75000,

    "joining_date": "2024-01-15",

    "skills": ["Python", "FastAPI", "MongoDB"]

  }'

```

### List Employees with Pagination

```bash

curl "http://localhost:8000/employees?page=1&limit=10&department=Engineering"

```

### Search by Skill

```bash

curl "http://localhost:8000/employees/search?skill=Python"

```

### Get Average Salary by Department

```bash

curl "http://localhost:8000/employees/avg-salary"

```

## 📁 Project Structure

```

employee-management-api/

├── main.py              # FastAPI application and routes

├── models.py            # Pydantic models and validation

├── db.py               # MongoDB connection and initialization

├── requirements.txt    # Project dependencies

└── README.md          # Project documentation

```

## 🗃️ Database Schema

```python

{

  "employee_id": str,      # Unique identifier

  "name": str,            # Employee name

  "department": str,      # Department name

  "salary": float,        # Annual salary

  "joining_date": date,   # Date of joining

  "skills": List[str]     # List of skills

}

```

## 🔐 Indexes Created

- `employee_id` (Unique) - Ensures unique employee IDs


## 🚦 Validation Rules

- **Employee ID**: Alphanumeric, 3-20 characters, unique

- **Name**: 2-100 characters, letters and spaces only

- **Department**: 2-50 characters, valid department names

- **Salary**: Positive value, reasonable maximum

- **Skills**: 1-20 items, each skill validated

- **Joining Date**: Cannot be in the future

## 🌐 API Documentation

Once the server is running, access the interactive documentation:

- **Swagger UI**: http://localhost:8000/docs




