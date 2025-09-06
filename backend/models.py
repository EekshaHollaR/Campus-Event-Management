from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base

class College(Base):
    __tablename__ = "colleges"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    
    students = relationship("Student", back_populates="college")
    events = relationship("Event", back_populates="college")
    event_managers = relationship("EventManager", back_populates="college")

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
    type = Column(String, index=True)  # workshop, seminar, cultural, sports, etc.
    date = Column(DateTime, index=True)
    capacity = Column(Integer)
    registrations_count = Column(Integer, default=0)
    status = Column(String, default="active", index=True)  # active, cancelled, postponed
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
    timestamp = Column(DateTime)
    
    __table_args__ = (UniqueConstraint('student_id', 'event_id', name='unique_student_event'),)
    
    student = relationship("Student", back_populates="registrations")
    event = relationship("Event", back_populates="registrations")
    attendance = relationship("Attendance", back_populates="registration", uselist=False)

class Attendance(Base):
    __tablename__ = "attendance"
    
    id = Column(Integer, primary_key=True, index=True)
    registration_id = Column(Integer, ForeignKey("registrations.id"), unique=True)
    checkin_time = Column(DateTime)
    status = Column(String)  # on-time, late
    
    registration = relationship("Registration", back_populates="attendance")

class Feedback(Base):
    __tablename__ = "feedback"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    event_id = Column(Integer, ForeignKey("events.id"))
    rating = Column(Integer)  # 1-5 scale
    comment = Column(Text)
    sentiment = Column(String)  # positive, negative, neutral
    
    __table_args__ = (UniqueConstraint('student_id', 'event_id', name='unique_student_event_feedback'),)
    
    student = relationship("Student", back_populates="feedback")
    event = relationship("Event", back_populates="feedback")