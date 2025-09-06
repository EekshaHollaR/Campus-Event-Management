from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, desc
from typing import List, Optional
import uvicorn
from datetime import datetime, timedelta
import re

from database import SessionLocal, engine
import models
import schemas

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Campus Event Management API", version="1.0.0")

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Simple sentiment analysis function
def analyze_sentiment(comment: str) -> str:
    if not comment:
        return "neutral"
    
    positive_words = ["good", "great", "excellent", "amazing", "fantastic", "love", "awesome", "perfect", "wonderful"]
    negative_words = ["bad", "terrible", "awful", "hate", "worst", "horrible", "disappointing", "poor"]
    
    comment_lower = comment.lower()
    positive_score = sum(1 for word in positive_words if word in comment_lower)
    negative_score = sum(1 for word in negative_words if word in comment_lower)
    
    if positive_score > negative_score:
        return "positive"
    elif negative_score > positive_score:
        return "negative"
    else:
        return "neutral"

# Event endpoints
@app.post("/events", response_model=schemas.Event)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    # Verify college exists
    college = db.query(models.College).filter(models.College.id == event.college_id).first()
    if not college:
        raise HTTPException(status_code=404, detail="College not found")
    
    # Verify manager exists
    manager = db.query(models.EventManager).filter(models.EventManager.id == event.manager_id).first()
    if not manager:
        raise HTTPException(status_code=404, detail="Event manager not found")
    
    db_event = models.Event(**event.dict(), registrations_count=0)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@app.get("/events", response_model=List[schemas.Event])
def list_events(
    college_id: Optional[int] = Query(None),
    event_type: Optional[str] = Query(None),
    status: Optional[str] = Query("active"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(models.Event)
    
    if college_id:
        query = query.filter(models.Event.college_id == college_id)
    if event_type:
        query = query.filter(models.Event.type == event_type)
    if status:
        query = query.filter(models.Event.status == status)
    
    events = query.offset(skip).limit(limit).all()
    return events

@app.get("/events/{event_id}", response_model=schemas.Event)
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

# Student registration endpoints
@app.post("/students/register", response_model=schemas.Registration)
def register_student(registration: schemas.RegistrationCreate, db: Session = Depends(get_db)):
    # Check if event exists and is active
    event = db.query(models.Event).filter(models.Event.id == registration.event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    if event.status != "active":
        raise HTTPException(status_code=400, detail="Cannot register for inactive events")
    
    # Check if student exists
    student = db.query(models.Student).filter(models.Student.id == registration.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Check capacity
    if event.registrations_count >= event.capacity:
        raise HTTPException(status_code=400, detail="Event is at full capacity")
    
    # Check for duplicate registration (handled by unique constraint, but let's be explicit)
    existing = db.query(models.Registration).filter(
        and_(models.Registration.student_id == registration.student_id,
             models.Registration.event_id == registration.event_id)
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Student already registered for this event")
    
    # Create registration
    db_registration = models.Registration(**registration.dict(), timestamp=datetime.utcnow())
    db.add(db_registration)
    
    # Update event registration count
    event.registrations_count += 1
    db.commit()
    db.refresh(db_registration)
    return db_registration

# Attendance check-in endpoints
@app.post("/attendance/checkin", response_model=schemas.Attendance)
def checkin_student(checkin: schemas.AttendanceCreate, db: Session = Depends(get_db)):
    # Get registration
    registration = db.query(models.Registration).filter(models.Registration.id == checkin.registration_id).first()
    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")
    
    # Check if already checked in
    existing_checkin = db.query(models.Attendance).filter(
        models.Attendance.registration_id == checkin.registration_id
    ).first()
    if existing_checkin:
        raise HTTPException(status_code=400, detail="Student already checked in")
    
    # Get event to check timing
    event = db.query(models.Event).filter(models.Event.id == registration.event_id).first()
    current_time = datetime.utcnow()
    
    # Determine status (on-time vs late)
    status = "on-time" if current_time <= event.date + timedelta(minutes=15) else "late"
    
    db_attendance = models.Attendance(
        registration_id=checkin.registration_id,
        checkin_time=current_time,
        status=status
    )
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return db_attendance

# Feedback endpoints
@app.post("/feedback", response_model=schemas.Feedback)
def submit_feedback(feedback: schemas.FeedbackCreate, db: Session = Depends(get_db)):
    # Check if student attended the event
    attendance = db.query(models.Attendance).join(models.Registration).filter(
        and_(models.Registration.student_id == feedback.student_id,
             models.Registration.event_id == feedback.event_id)
    ).first()
    
    if not attendance:
        raise HTTPException(status_code=400, detail="Can only provide feedback for attended events")
    
    # Check for duplicate feedback
    existing = db.query(models.Feedback).filter(
        and_(models.Feedback.student_id == feedback.student_id,
             models.Feedback.event_id == feedback.event_id)
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Feedback already submitted for this event")
    
    # Analyze sentiment
    sentiment = analyze_sentiment(feedback.comment)
    
    db_feedback = models.Feedback(**feedback.dict(), sentiment=sentiment)
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

# Reports endpoints
@app.get("/reports/event-popularity")
def get_event_popularity(
    college_id: Optional[int] = Query(None),
    event_type: Optional[str] = Query(None),
    limit: int = Query(10),
    db: Session = Depends(get_db)
):
    query = db.query(models.Event).order_by(desc(models.Event.registrations_count))
    
    if college_id:
        query = query.filter(models.Event.college_id == college_id)
    if event_type:
        query = query.filter(models.Event.type == event_type)
    
    events = query.limit(limit).all()
    return [{"event_id": e.id, "title": e.title, "registrations": e.registrations_count} for e in events]

@app.get("/reports/attendance")
def get_attendance_report(
    college_id: Optional[int] = Query(None),
    event_type: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(
        models.Event.id,
        models.Event.title,
        models.Event.registrations_count,
        func.count(models.Attendance.id).label('attended_count')
    ).outerjoin(models.Registration).outerjoin(models.Attendance).group_by(models.Event.id)
    
    if college_id:
        query = query.filter(models.Event.college_id == college_id)
    if event_type:
        query = query.filter(models.Event.type == event_type)
    
    results = query.all()
    return [
        {
            "event_id": r.id,
            "title": r.title,
            "registered": r.registrations_count,
            "attended": r.attended_count,
            "attendance_percentage": round((r.attended_count / r.registrations_count * 100) if r.registrations_count > 0 else 0, 2)
        }
        for r in results
    ]

@app.get("/reports/feedback")
def get_feedback_report(
    college_id: Optional[int] = Query(None),
    event_type: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(
        models.Event.id,
        models.Event.title,
        func.avg(models.Feedback.rating).label('avg_rating'),
        func.count(models.Feedback.id).label('feedback_count'),
        func.sum(func.case([(models.Feedback.sentiment == 'positive', 1)], else_=0)).label('positive_count'),
        func.sum(func.case([(models.Feedback.sentiment == 'negative', 1)], else_=0)).label('negative_count'),
        func.sum(func.case([(models.Feedback.sentiment == 'neutral', 1)], else_=0)).label('neutral_count')
    ).outerjoin(models.Feedback).group_by(models.Event.id)
    
    if college_id:
        query = query.filter(models.Event.college_id == college_id)
    if event_type:
        query = query.filter(models.Event.type == event_type)
    
    results = query.all()
    return [
        {
            "event_id": r.id,
            "title": r.title,
            "average_rating": round(float(r.avg_rating), 2) if r.avg_rating else 0,
            "feedback_count": r.feedback_count,
            "sentiment_distribution": {
                "positive": r.positive_count,
                "negative": r.negative_count,
                "neutral": r.neutral_count
            }
        }
        for r in results
    ]

@app.get("/reports/student-participation")
def get_student_participation(
    college_id: Optional[int] = Query(None),
    limit: int = Query(50),
    db: Session = Depends(get_db)
):
    query = db.query(
        models.Student.id,
        models.Student.name,
        models.Student.email,
        func.count(models.Attendance.id).label('events_attended')
    ).outerjoin(models.Registration).outerjoin(models.Attendance).group_by(models.Student.id)
    
    if college_id:
        query = query.filter(models.Student.college_id == college_id)
    
    results = query.order_by(desc('events_attended')).limit(limit).all()
    return [
        {
            "student_id": r.id,
            "name": r.name,
            "email": r.email,
            "events_attended": r.events_attended
        }
        for r in results
    ]

@app.get("/reports/top-students")
def get_top_students(limit: int = Query(10), db: Session = Depends(get_db)):
    results = db.query(
        models.Student.id,
        models.Student.name,
        models.Student.email,
        func.count(models.Attendance.id).label('events_attended')
    ).outerjoin(models.Registration).outerjoin(models.Attendance).group_by(models.Student.id).order_by(desc('events_attended')).limit(limit).all()
    
    return [
        {
            "student_id": r.id,
            "name": r.name,
            "email": r.email,
            "events_attended": r.events_attended
        }
        for r in results
    ]

@app.get("/reports/upcoming-events")
def get_upcoming_events(
    college_id: Optional[int] = Query(None),
    days_ahead: int = Query(30),
    db: Session = Depends(get_db)
):
    future_date = datetime.utcnow() + timedelta(days=days_ahead)
    
    query = db.query(models.Event).filter(
        and_(models.Event.date >= datetime.utcnow(),
             models.Event.date <= future_date,
             models.Event.status == "active")
    ).order_by(models.Event.date)
    
    if college_id:
        query = query.filter(models.Event.college_id == college_id)
    
    events = query.all()
    return events

# Utility endpoints
@app.get("/colleges", response_model=List[schemas.College])
def list_colleges(db: Session = Depends(get_db)):
    return db.query(models.College).all()

@app.get("/students", response_model=List[schemas.Student])
def list_students(college_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    query = db.query(models.Student)
    if college_id:
        query = query.filter(models.Student.college_id == college_id)
    return query.all()

@app.get("/event-managers", response_model=List[schemas.EventManager])
def list_event_managers(db: Session = Depends(get_db)):
    return db.query(models.EventManager).all()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)