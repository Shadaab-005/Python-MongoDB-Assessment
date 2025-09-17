from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import List, Optional, AsyncIterator
from contextlib import asynccontextmanager
from datetime import date, timedelta

from models import Employee, UpdateEmployee
from db import employees_collection, users_collection, init_db
from auth import (
    authenticate_user, create_access_token,
    get_current_user, get_password_hash
)

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    await init_db()
    yield

app = FastAPI(title="Employee API with JWT + User Registration", lifespan=lifespan)

#  User Registration 
@app.post("/register")
async def register_user(username: str, password: str):
    if await users_collection.find_one({"username": username}):
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_pw = get_password_hash(password)
    await users_collection.insert_one({"username": username, "hashed_password": hashed_pw})
    return {"message": "User registered successfully"}

# Token Generation 
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    token = create_access_token({"sub": form_data.username},
                                expires_delta=timedelta(minutes=30))
    return {"access_token": token, "token_type": "bearer"}

#  Utility Functions -> Date Normalization
def normalize_employee_dates_for_storage(data: dict) -> dict:
    if "joining_date" in data and isinstance(data["joining_date"], date):
        data["joining_date"] = data["joining_date"].isoformat()
    return data

def normalize_employee_dates_for_response(data: dict) -> dict:
    if "joining_date" in data and isinstance(data["joining_date"], str):
        data["joining_date"] = date.fromisoformat(data["joining_date"])
    return data

@app.get("/")
def start():
    return {"message": "Employee API with JWT + Registration"}

# Create employee (Protected)
@app.post("/employees", response_model=Employee)
async def create_employee(emp: Employee, user: str = Depends(get_current_user)):
    if await employees_collection.find_one({"employee_id": emp.employee_id}):
        raise HTTPException(status_code=400, detail="employee_id must be unique")
    emp_dict = normalize_employee_dates_for_storage(emp.model_dump())
    result = await employees_collection.insert_one(emp_dict)
    new_employee = await employees_collection.find_one({"_id": result.inserted_id})
    return Employee(**normalize_employee_dates_for_response(new_employee))


# List employees (Public)
@app.get("/employees", response_model=dict)
async def list_employees(
    department: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100)
):
    query = {"department": department} if department else {}
    skip = (page - 1) * limit
    total_count = await employees_collection.count_documents(query)
    total_pages = (total_count + limit - 1) // limit
    cursor = employees_collection.find(query).sort("joining_date", -1).skip(skip).limit(limit)
    employees = []
    async for doc in cursor:
        doc = normalize_employee_dates_for_response(doc)
        employees.append(Employee(**doc))
    return {
        "data": employees,
        "pagination": {
            "page": page, "limit": limit,
            "total_items": total_count, "total_pages": total_pages,
            "has_next": page < total_pages, "has_prev": page > 1
        }
    }

# Average salary (Public)
@app.get("/employees/avg-salary")
async def avg_salary():
    pipeline = [
        {"$group": {"_id": "$department", "avg_salary": {"$avg": "$salary"}}},
        {"$project": {"_id": 0, "department": "$_id", "avg_salary": {"$round": ["$avg_salary", 2]}}}
    ]
    return [doc async for doc in employees_collection.aggregate(pipeline)]

# Search by skill (Public)
@app.get("/employees/search", response_model=List[Employee])
async def search_by_skill(skill: str = Query(...)):
    cursor = employees_collection.find({"skills": skill})
    employees = []
    async for doc in cursor:
        doc = normalize_employee_dates_for_response(doc)
        employees.append(Employee(**doc))
    return employees

# Get employee (Public)
@app.get("/employees/{employee_id}", response_model=Employee)
async def get_employee(employee_id: str):
    doc = await employees_collection.find_one({"employee_id": employee_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Employee not found")
    return Employee(**normalize_employee_dates_for_response(doc))

# Update (Protected)
@app.put("/employees/{employee_id}", response_model=Employee)
async def update_employee(employee_id: str, updates: UpdateEmployee,
                          user: str = Depends(get_current_user)):
    update_data = normalize_employee_dates_for_storage(
        updates.model_dump(exclude_unset=True))
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    result = await employees_collection.find_one_and_update(
        {"employee_id": employee_id},
        {"$set": update_data},
        return_document=True
    )
    if not result:
        raise HTTPException(status_code=404, detail="Employee not found")
    return Employee(**normalize_employee_dates_for_response(result))

# Delete (Protected)
@app.delete("/employees/{employee_id}")
async def delete_employee(employee_id: str, user: str = Depends(get_current_user)):
    res = await employees_collection.delete_one({"employee_id": employee_id})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee deleted successfully"}
