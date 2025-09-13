from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional, AsyncIterator
from contextlib import asynccontextmanager
from models import Employee, UpdateEmployee
from db import employees_collection, init_db
from datetime import date

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # Startup event - to initialize database (indexes are created here)
    await init_db()
    yield
    # Shutdown event (can add optional cleanup here if needed)

app = FastAPI(title="Employee API with MongoDB", lifespan=lifespan)

# Utility function: To convert date to ISO string for MongoDB storage
def normalize_employee_dates_for_storage(data: dict) -> dict:
    if "joining_date" in data and isinstance(data["joining_date"], date):
        data["joining_date"] = data["joining_date"].isoformat()
    return data

# Utility function: To convert ISO string back to date for response
def normalize_employee_dates_for_response(data: dict) -> dict:
    if "joining_date" in data and isinstance(data["joining_date"], str):
        data["joining_date"] = date.fromisoformat(data["joining_date"])
    return data


@app.get("/")
def start():
    return {'message':'Employee API with MongoDB'}

# 1. Creating Employee
@app.post("/employees", response_model=Employee)
async def create_employee(emp: Employee):
    if await employees_collection.find_one({"employee_id": emp.employee_id}):
        raise HTTPException(status_code=400, detail="employee_id must be unique")
    
    emp_dict = emp.model_dump()
    emp_dict = normalize_employee_dates_for_storage(emp_dict)
    
    result = await employees_collection.insert_one(emp_dict)
    new_employee = await employees_collection.find_one({"_id": result.inserted_id})
    new_employee = normalize_employee_dates_for_response(new_employee)
    return Employee(**new_employee)

# 5. Listing employees with optional department filter and pagination
@app.get("/employees", response_model=dict)
async def list_employees(
    department: Optional[str] = Query(None),
    page: int = Query(1, ge=1, description="Page number starting from 1"),
    limit: int = Query(10, ge=1, le=100, description="Number of items per page (1-100)")
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
            "page": page,
            "limit": limit,
            "total_items": total_count,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_prev": page > 1
        }
    }

# 6. Calculating average Salary by Department
@app.get("/employees/avg-salary")
async def avg_salary():
    pipeline = [
        {
            "$group": {
                "_id": "$department",
                "avg_salary": {"$avg": "$salary"}
            }
        },
        {
            "$project": {
                "_id": 0,
                "department": "$_id",
                "avg_salary": {"$round": ["$avg_salary", 2]}
            }
        }
    ]
    
    result = []
    async for doc in employees_collection.aggregate(pipeline):
        result.append(doc)
    return result

# 7. Searching by Skill
@app.get("/employees/search", response_model=List[Employee])
async def search_by_skill(skill: str = Query(...)):
    cursor = employees_collection.find({"skills": skill})
    employees = []
    async for doc in cursor:
        doc = normalize_employee_dates_for_response(doc)
        employees.append(Employee(**doc))
    return employees

# 2. Getting Employee by ID
@app.get("/employees/{employee_id}", response_model=Employee)
async def get_employee(employee_id: str):
    doc = await employees_collection.find_one({"employee_id": employee_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Employee not found")
    doc = normalize_employee_dates_for_response(doc)
    return Employee(**doc)

# 3. Updating Employee
@app.put("/employees/{employee_id}", response_model=Employee)
async def update_employee(employee_id: str, updates: UpdateEmployee):
    update_data = updates.model_dump(exclude_unset=True)
    update_data = normalize_employee_dates_for_storage(update_data)
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    result = await employees_collection.find_one_and_update(
        {"employee_id": employee_id},
        {"$set": update_data},
        return_document=True
    )
    if not result:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    result = normalize_employee_dates_for_response(result)
    return Employee(**result)

# 4. Deleting Employee
@app.delete("/employees/{employee_id}")
async def delete_employee(employee_id: str):
    res = await employees_collection.delete_one({"employee_id": employee_id})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee deleted successfully"}