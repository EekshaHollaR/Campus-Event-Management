from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean, Float, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class College(Base):
    __tablename__ = "colleges"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    
    students = relationship("Student", back_populates="college")
    event_managers = relationship("EventManager", back_populates="college")
    events = relationship("Event", back_populates="college")

class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    college_id = Column(Integer, ForeignKey("colleges.id"))
    
    college = relationship("College", back_populates="students")
    registrations = relationship("Registration", back_populates="student")
    feedback = relationship("Feedback", back_populates="student")

class EventManager(Base):
    __tablename__ = "event_managers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    college_id = Column(Integer, ForeignKey("colleges.id"))
    
    college = relationship("College", back_populates="event_managers")
    events = relationship("Event", back_populates="manager")

class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    type = Column(String, index=True)
    date = Column(DateTime)
    capacity = Column(Integer)
    registrations_count = Column(Integer, default=0)
    status = Column(String, default="active")
    college_id = Column(Integer, ForeignKey("colleges.id"))
    manager_id = Column(Integer, ForeignKey("event_managers.id"))
    
    college = relationship("College", back_populates="events")
    manager = relationship("EventManager", back_populates="events")
    registrations = relationship("Registration", back_populates="event")
    feedback = relationship("Feedback", back_populates="event")

class Registration(Base):
    __tablename__ = "registrations"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    event_id = Column(Integer, ForeignKey("events.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    student = relationship("Student", back_populates="registrations")
    event = relationship("Event", back_populates="registrations")
    attendance = relationship("Attendance", back_populates="registration", uselist=False)
    
    __table_args__ = (UniqueConstraint('student_id', 'event_id', name='unique_registration'),)

class Attendance(Base):
    __tablename__ = "attendance"
    
    id = Column(Integer, primary_key=True, index=True)
    registration_id = Column(Integer, ForeignKey("registrations.id"), unique=True)
    checkin_time = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="present")
    
    registration = relationship("Registration", back_populates="attendance")

class Feedback(Base):
    __tablename__ = "feedback"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    event_id = Column(Integer, ForeignKey("events.id"))
    rating = Column(Integer)
    comment = Column(Text, nullable=True)
    sentiment = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    student = relationship("Student", back_populates="feedback")
    event = relationship("Event", back_populates="feedback")
    
    __table_args__ = (UniqueConstraint('student_id', 'event_id', name='unique_feedback'),)