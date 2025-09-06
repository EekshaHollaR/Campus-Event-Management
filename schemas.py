from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional

class CollegeBase(BaseModel):
    name: str

class CollegeCreate(CollegeBase):
    pass

class College(CollegeBase):
    id: int
    class Config:
        from_attributes = True

class StudentBase(BaseModel):
    name: str
    email: str
    college_id: int

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id: int
    class Config:
        from_attributes = True

class EventManagerBase(BaseModel):
    name: str
    email: str
    college_id: int

class EventManagerCreate(EventManagerBase):
    pass

class EventManager(EventManagerBase):
    id: int
    class Config:
        from_attributes = True

class EventBase(BaseModel):
    title: str
    description: str
    type: str
    date: datetime
    capacity: int
    college_id: int
    manager_id: int

class EventCreate(EventBase):
    pass

class Event(EventBase):
    id: int
    registrations_count: int
    status: str
    class Config:
        from_attributes = True

class RegistrationCreate(BaseModel):
    student_id: int
    event_id: int

class Registration(BaseModel):
    id: int
    student_id: int
    event_id: int
    timestamp: datetime
    class Config:
        from_attributes = True

class CheckinRequest(BaseModel):
    registration_id: int
    status: Optional[str] = "present"

class Attendance(BaseModel):
    id: int
    registration_id: int
    checkin_time: datetime
    status: str
    class Config:
        from_attributes = True

class FeedbackCreate(BaseModel):
    student_id: int
    event_id: int
    rating: int
    comment: Optional[str] = None

class Feedback(BaseModel):
    id: int
    student_id: int
    event_id: int
    rating: int
    comment: Optional[str]
    sentiment: Optional[str]
    timestamp: datetime
    class Config:
        from_attributes = True