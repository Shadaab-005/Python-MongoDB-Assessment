from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import date
import re

class Employee(BaseModel):
    employee_id: str = Field(
        ...,
        min_length=3,
        max_length=20,
        pattern=r"^[A-Za-z0-9_-]+$",
        example="E123",
        description="Unique employee identifier (alphanumeric, hyphens, underscores only)"
    )
    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        pattern=r"^[A-Za-z\s\.'-]+$",
        example="John Doe",
        description="Employee full name (letters, spaces, apostrophes, hyphens, and dots only)"
    )
    department: str = Field(
        ...,
        min_length=2,
        max_length=50,
        pattern=r"^[A-Za-z\s&-]+$",
        example="Engineering",
        description="Department name (letters, spaces, ampersands, and hyphens only)"
    )
    salary: float = Field(
        ...,
        gt=0,
        le=1000000,
        example=50000.0,
        description="Annual salary (must be positive and reasonable)"
    )
    joining_date: date = Field(
        ...,
        example="2024-01-15",
        description="Date when employee joined the company"
    )
    skills: List[str] = Field(
        ...,
        min_items=1,
        max_items=20,
        example=["Python", "FastAPI", "MongoDB"],
        description="List of employee skills (1-20 items)"
    )
    
    @field_validator('joining_date')
    @classmethod
    def validate_joining_date(cls, v):
        if v > date.today():
            raise ValueError("Joining date cannot be in the future")
        # Optional: Add minimum date constraint (e.g., company founding date)
        if v < date(2000, 1, 1):
            raise ValueError("Joining date cannot be before the year 2000")
        return v
    
    @field_validator('skills')
    @classmethod
    def validate_skills(cls, v):
        if not v:
            raise ValueError("At least one skill is required")
        
        # Validate each skill
        for skill in v:
            if not skill.strip():
                raise ValueError("Skill cannot be empty or whitespace")
            if len(skill) > 50:
                raise ValueError("Skill name cannot exceed 50 characters")
            if not re.match(r"^[A-Za-z0-9\s\+#\.&/-]+$", skill):
                raise ValueError("Skill contains invalid characters")
        
        # Remove duplicates and sort alphabetically
        unique_skills = list(set(skill.strip() for skill in v))
        unique_skills.sort()
        return unique_skills

class UpdateEmployee(BaseModel):
    name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100,
        pattern=r"^[A-Za-z\s\.'-]+$",
        example="John Doe",
        description="Employee full name (letters, spaces, apostrophes, hyphens, and dots only)"
    )
    department: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=50,
        pattern=r"^[A-Za-z\s&-]+$",
        example="Engineering",
        description="Department name (letters, spaces, ampersands, and hyphens only)"
    )
    salary: Optional[float] = Field(
        default=None,
        gt=0,
        le=1000000,
        example=50000.0,
        description="Annual salary (must be positive and reasonable)"
    )
    joining_date: Optional[date] = Field(
        default=None,
        example="2024-01-15",
        description="Date when employee joined the company"
    )
    skills: Optional[List[str]] = Field(
        default=None,
        min_items=1,
        max_items=20,
        example=["Python", "FastAPI", "MongoDB"],
        description="List of employee skills (1-20 items)"
    )
    
    @field_validator('joining_date')
    @classmethod
    def validate_joining_date(cls, v):
        if v and v > date.today():
            raise ValueError("Joining date cannot be in the future")
        if v and v < date(2000, 1, 1):
            raise ValueError("Joining date cannot be before the year 2000")
        return v
    
    @field_validator('skills')
    @classmethod
    def validate_skills(cls, v):
        if v is not None:
            if not v:
                raise ValueError("At least one skill is required")
            
            # Validate each skill
            for skill in v:
                if not skill.strip():
                    raise ValueError("Skill cannot be empty or whitespace")
                if len(skill) > 50:
                    raise ValueError("Skill name cannot exceed 50 characters")
                if not re.match(r"^[A-Za-z0-9\s\+#\.&/-]+$", skill):
                    raise ValueError("Skill contains invalid characters")
            
            # Remove duplicates and sort alphabetically
            unique_skills = list(set(skill.strip() for skill in v))
            unique_skills.sort()
            return unique_skills
        return v