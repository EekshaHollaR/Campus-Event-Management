# schemas.py
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# College schemas
class CollegeBase(BaseModel):
    name: str

class CollegeCreate(CollegeBase):
    pass

class College(CollegeBase):
    id: int
    
    class Config:
        orm_mode = True

# Student schemas
class StudentBase(BaseModel):
    name: str
    email: EmailStr
    college_id: int

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id: int
    
    class Config:
        orm_mode = True

# Event Manager schemas
class EventManagerBase(BaseModel):
    name: str
    email: EmailStr
    college_id: int

class EventManagerCreate(EventManagerBase):
    pass

class EventManager(EventManagerBase):
    id: int
    
    class Config:
        orm_mode = True

# Event schemas
class EventBase(BaseModel):
    title: str
    description: str
    type: str
    date: datetime
    capacity: int
    college_id: int
    manager_id: int

class EventCreate(EventBase):
    status: str = "active"

class Event(EventBase):
    id: int
    registrations_count: int
    status: str
    
    class Config:
        orm_mode = True

# Registration schemas
class RegistrationBase(BaseModel):
    student_id: int
    event_id: int

class RegistrationCreate(RegistrationBase):
    pass

class Registration(RegistrationBase):
    id: int
    timestamp: datetime
    
    class Config:
        orm_mode = True

# Attendance schemas
class AttendanceBase(BaseModel):
    registration_id: int

class AttendanceCreate(AttendanceBase):
    pass

class Attendance(AttendanceBase):
    id: int
    checkin_time: datetime
    status: str
    
    class Config:
        orm_mode = True

# Feedback schemas
class FeedbackBase(BaseModel):
    student_id: int
    event_id: int
    rating: int
    comment: Optional[str] = None

class FeedbackCreate(FeedbackBase):
    pass

class Feedback(FeedbackBase):
    id: int
    sentiment: str
    
    class Config:
        orm_mode = True