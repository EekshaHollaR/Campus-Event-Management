from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import qrcode
import io
import base64
from textblob import TextBlob
from datetime import datetime

from database import SessionLocal, engine, get_db
from models import Base, College, Student, EventManager, Event, Registration, Attendance, Feedback
from schemas import *

# Create tables
Base.metadata.create_all(bind=engine)

# FastAPI App
app = FastAPI(title="Campus Event Management Platform", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper functions
def analyze_sentiment(text: str) -> str:
    if not text:
        return "neutral"
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.1:
        return "positive"
    elif polarity < -0.1:
        return "negative"
    else:
        return "neutral"

def generate_qr_code(data: str) -> str:
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    
    return base64.b64encode(buffer.getvalue()).decode()

# API Endpoints
@app.get("/")
def read_root():
    return {"message": "Campus Event Management Platform API", "version": "1.0.0"}

# College endpoints
@app.post("/colleges/", response_model=College)
def create_college(college: CollegeCreate, db: Session = Depends(get_db)):
    db_college = College(name=college.name)
    db.add(db_college)
    db.commit()
    db.refresh(db_college)
    return db_college

@app.get("/colleges/", response_model=List[College])
def get_colleges(db: Session = Depends(get_db)):
    return db.query(College).all()

# Student endpoints
@app.post("/students/", response_model=Student)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    db_student = Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@app.get("/students/", response_model=List[Student])
def get_students(db: Session = Depends(get_db)):
    return db.query(Student).all()

# Event Manager endpoints
@app.post("/event-managers/", response_model=EventManager)
def create_event_manager(manager: EventManagerCreate, db: Session = Depends(get_db)):
    db_manager = EventManager(**manager.dict())
    db.add(db_manager)
    db.commit()
    db.refresh(db_manager)
    return db_manager

# Event endpoints
@app.post("/events/", response_model=Event)
def create_event(event: EventCreate, db: Session = Depends(get_db)):
    db_event = Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@app.get("/events/", response_model=List[Event])
def get_events(
    event_type: Optional[str] = Query(None),
    college_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Event)
    
    if event_type:
        query = query.filter(Event.type == event_type)
    if college_id:
        query = query.filter(Event.college_id == college_id)
    if status:
        query = query.filter(Event.status == status)
    
    return query.all()

@app.get("/events/{event_id}", response_model=Event)
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

# Registration endpoints
@app.post("/students/register/", response_model=Registration)
def register_student(registration: RegistrationCreate, db: Session = Depends(get_db)):
    # Check if event exists and is active
    event = db.query(Event).filter(Event.id == registration.event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    if event.status != "active":
        raise HTTPException(status_code=400, detail="Cannot register for inactive event")
    
    # Check capacity
    if event.registrations_count >= event.capacity:
        raise HTTPException(status_code=400, detail="Event is at full capacity")
    
    # Check for duplicate registration
    existing = db.query(Registration).filter(
        Registration.student_id == registration.student_id,
        Registration.event_id == registration.event_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Student already registered for this event")
    
    # Create registration
    db_registration = Registration(**registration.dict())
    db.add(db_registration)
    
    # Update event registration count
    event.registrations_count += 1
    
    db.commit()
    db.refresh(db_registration)
    return db_registration

@app.get("/registrations/qr/{registration_id}")
def get_registration_qr(registration_id: int, db: Session = Depends(get_db)):
    registration = db.query(Registration).filter(Registration.id == registration_id).first()
    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")
    
    qr_data = f"registration_{registration_id}"
    qr_code = generate_qr_code(qr_data)
    
    return {"qr_code": qr_code, "data": qr_data}

# Attendance endpoints
@app.post("/attendance/checkin/", response_model=Attendance)
def checkin_student(checkin: CheckinRequest, db: Session = Depends(get_db)):
    # Check if registration exists
    registration = db.query(Registration).filter(Registration.id == checkin.registration_id).first()
    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")
    
    # Check if already checked in
    existing_attendance = db.query(Attendance).filter(Attendance.registration_id == checkin.registration_id).first()
    if existing_attendance:
        raise HTTPException(status_code=400, detail="Student already checked in")
    
    # Create attendance record
    db_attendance = Attendance(
        registration_id=checkin.registration_id,
        status=checkin.status
    )
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return db_attendance

# Feedback endpoints
@app.post("/feedback/", response_model=Feedback)
def submit_feedback(feedback: FeedbackCreate, db: Session = Depends(get_db)):
    # Check if student attended the event
    registration = db.query(Registration).filter(
        Registration.student_id == feedback.student_id,
        Registration.event_id == feedback.event_id
    ).first()
    
    if not registration:
        raise HTTPException(status_code=400, detail="Student not registered for this event")
    
    attendance = db.query(Attendance).filter(Attendance.registration_id == registration.id).first()
    if not attendance:
        raise HTTPException(status_code=400, detail="Student did not attend this event")
    
    # Check for existing feedback
    existing_feedback = db.query(Feedback).filter(
        Feedback.student_id == feedback.student_id,
        Feedback.event_id == feedback.event_id
    ).first()
    
    if existing_feedback:
        raise HTTPException(status_code=400, detail="Feedback already submitted for this event")
    
    # Analyze sentiment
    sentiment = analyze_sentiment(feedback.comment)
    
    # Create feedback
    db_feedback = Feedback(
        **feedback.dict(),
        sentiment=sentiment
    )
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

# Report endpoints
@app.get("/reports/event-popularity")
def get_event_popularity(db: Session = Depends(get_db)):
    events = db.query(Event).order_by(Event.registrations_count.desc()).all()
    return [{"event_id": e.id, "title": e.title, "registrations": e.registrations_count} for e in events]

@app.get("/reports/attendance")
def get_attendance_report(db: Session = Depends(get_db)):
    results = []
    events = db.query(Event).all()
    
    for event in events:
        total_registrations = event.registrations_count
        attended = db.query(Attendance).join(Registration).filter(Registration.event_id == event.id).count()
        
        attendance_percentage = (attended / total_registrations * 100) if total_registrations > 0 else 0
        
        results.append({
            "event_id": event.id,
            "title": event.title,
            "total_registrations": total_registrations,
            "attended": attended,
            "attendance_percentage": round(attendance_percentage, 2)
        })
    
    return results

@app.get("/reports/feedback")
def get_feedback_report(db: Session = Depends(get_db)):
    results = []
    events = db.query(Event).all()
    
    for event in events:
        feedbacks = db.query(Feedback).filter(Feedback.event_id == event.id).all()
        
        if feedbacks:
            avg_rating = sum(f.rating for f in feedbacks) / len(feedbacks)
            sentiment_counts = {}
            for f in feedbacks:
                sentiment_counts[f.sentiment] = sentiment_counts.get(f.sentiment, 0) + 1
        else:
            avg_rating = 0
            sentiment_counts = {}
        
        results.append({
            "event_id": event.id,
            "title": event.title,
            "feedback_count": len(feedbacks),
            "average_rating": round(avg_rating, 2),
            "sentiment_analysis": sentiment_counts
        })
    
    return results

@app.get("/reports/student-participation")
def get_student_participation(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    results = []
    
    for student in students:
        attended_count = db.query(Attendance).join(Registration).filter(
            Registration.student_id == student.id
        ).count()
        
        results.append({
            "student_id": student.id,
            "name": student.name,
            "events_attended": attended_count
        })
    
    return sorted(results, key=lambda x: x["events_attended"], reverse=True)

@app.get("/reports/top-students")
def get_top_students(limit: int = Query(10), db: Session = Depends(get_db)):
    participation = get_student_participation(db)
    return participation[:limit]

@app.get("/reports/upcoming-events")
def get_upcoming_events(db: Session = Depends(get_db)):
    upcoming = db.query(Event).filter(
        Event.date > datetime.utcnow(),
        Event.status == "active"
    ).order_by(Event.date).all()
    
    return [{"event_id": e.id, "title": e.title, "date": e.date, "type": e.type} for e in upcoming]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)