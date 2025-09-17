# Employee Management API with FastAPI and MongoDB

A RESTful API for managing employee data built with FastAPI, MongoDB, and featuring JWT-based authentication, pagination, search, and analytics.

## 🚀 Features

- **User Authentication**:  
  - **Register** with a username & password  
  - **Login** to obtain a JWT token  
  - **Protected Routes** for creating, updating, and deleting employees
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
- **Authentication**: JWT (JSON Web Token) with `python-jose` & password hashing with `passlib`
- **API Documentation**: Automatic Swagger UI

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




## 🔐 Authentication Flow

| Method   | Endpoint                   | Description              | Auth Required |
| -------- | -------------------------- | ------------------------ | ------------- |
| `POST`   | `/register`                | Register a new user      | No            |
| `POST`   | `/token`                   | Obtain JWT token (login) | No            |
| `POST`   | `/employees`               | Create a new employee    | **Yes**       |
| `PUT`    | `/employees/{employee_id}` | Update employee          | **Yes**       |
| `DELETE` | `/employees/{employee_id}` | Delete employee          | **Yes**       |

All read-only endpoints remain public.

### Example Workflow

1. **Register User**

   ```bash
   curl -X POST "http://localhost:8000/register?username=alice&password=strongpass"
   ```

2. **Login & Get Token**

   ```bash
   curl -X POST "http://localhost:8000/token" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "username=alice&password=strongpass"
   ```

   Response:

   ```json
   { "access_token": "<JWT_TOKEN>", "token_type": "bearer" }
   ```

3. **Use Token in Protected Request**

   ```bash
   curl -X POST "http://localhost:8000/employees" \
        -H "Authorization: Bearer <JWT_TOKEN>" \
        -H "Content-Type: application/json" \
        -d '{
              "employee_id": "E001",
              "name": "John Doe",
              "department": "Engineering",
              "salary": 75000,
              "joining_date": "2024-01-15",
              "skills": ["Python", "FastAPI"]
            }'
   ```

## 📋 Employee API Endpoints

| Method | Endpoint                         | Description                           | Auth Required |
| ------ | -------------------------------- | ------------------------------------- | ------------- |
| `GET`  | `/employees`                     | List employees with pagination/filter | No            |
| `GET`  | `/employees/{employee_id}`       | Get employee by ID                    | No            |
| `GET`  | `/employees/search?skill=Python` | Search by skill                       | No            |
| `GET`  | `/employees/avg-salary`          | Average salary by department          | No            |

## 📁 Project Structure

```
employee-management-api/
├── main.py          # FastAPI application and routes
├── auth.py          # JWT helpers and authentication logic
├── models.py        # Pydantic models and validation
├── db.py            # MongoDB connection and initialization
├── requirements.txt # Project dependencies
└── README.md        # Project documentation
```

## 🗃️ Database Schema

### Users Collection

```json
{
  "username": "string",
  "hashed_password": "string"
}
```

### Employees Collection


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

* `employee_id` (Unique) - Ensures unique employee IDs
* `username` (Unique) - Ensures unique user accounts

## 🌐 API Documentation

Once the server is running, access interactive docs:

* **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)





