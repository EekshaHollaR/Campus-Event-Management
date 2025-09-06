from sqlalchemy.orm import Session
from database import SessionLocal, engine
from datetime import datetime, timedelta
import models

# Create all tables
models.Base.metadata.create_all(bind=engine)

def init_sample_data():
    db = SessionLocal()
    
    try:
        # Create colleges
        colleges_data = [
            {"id": 1, "name": "Engineering College"},
            {"id": 2, "name": "Business School"},
            {"id": 3, "name": "Arts & Science College"},
            {"id": 4, "name": "Medical College"}
        ]
        
        for college_data in colleges_data:
            college = models.College(**college_data)
            db.add(college)
        
        # Create event managers
        event_managers_data = [
            {"id": 1, "name": "Dr. Smith", "email": "smith@engineering.edu", "college_id": 1},
            {"id": 2, "name": "Prof. Johnson", "email": "johnson@business.edu", "college_id": 2},
            {"id": 3, "name": "Ms. Wilson", "email": "wilson@arts.edu", "college_id": 3},
            {"id": 4, "name": "Dr. Brown", "email": "brown@medical.edu", "college_id": 4}
        ]
        
        for manager_data in event_managers_data:
            manager = models.EventManager(**manager_data)
            db.add(manager)
        
        # Create sample students
        students_data = [
            {"id": 1, "name": "Alice Cooper", "email": "alice@student.edu", "college_id": 1},
            {"id": 2, "name": "Bob Smith", "email": "bob@student.edu", "college_id": 1},
            {"id": 3, "name": "Carol Johnson", "email": "carol@student.edu", "college_id": 2},
            {"id": 4, "name": "David Wilson", "email": "david@student.edu", "college_id": 2},
            {"id": 5, "name": "Eve Brown", "email": "eve@student.edu", "college_id": 3},
            {"id": 6, "name": "Frank Davis", "email": "frank@student.edu", "college_id": 3},
            {"id": 7, "name": "Grace Miller", "email": "grace@student.edu", "college_id": 4},
            {"id": 8, "name": "Henry Taylor", "email": "henry@student.edu", "college_id": 4},
            {"id": 9, "name": "Ivy Anderson", "email": "ivy@student.edu", "college_id": 1},
            {"id": 10, "name": "Jack Thomas", "email": "jack@student.edu", "college_id": 2}
        ]
        
        for student_data in students_data:
            student = models.Student(**student_data)
            db.add(student)
        
        # Create sample events
        base_date = datetime.utcnow()
        events_data = [
            {
                "id": 1,
                "title": "AI Workshop",
                "description": "Introduction to Artificial Intelligence and Machine Learning",
                "type": "workshop",
                "date": base_date + timedelta(days=7),
                "capacity": 50,
                "college_id": 1,
                "manager_id": 1,
                "registrations_count": 35
            },
            {
                "id": 2,
                "title": "Business Strategy Seminar",
                "description": "Modern approaches to business strategy and planning",
                "type": "seminar",
                "date": base_date + timedelta(days=14),
                "capacity": 100,
                "college_id": 2,
                "manager_id": 2,
                "registrations_count": 75
            },
            {
                "id": 3,
                "title": "Cultural Festival",
                "description": "Annual inter-college cultural festival",
                "type": "cultural",
                "date": base_date + timedelta(days=21),
                "capacity": 200,
                "college_id": 3,
                "manager_id": 3,
                "registrations_count": 150
            },
            {
                "id": 4,
                "title": "Medical Conference",
                "description": "Latest developments in medical research",
                "type": "conference",
                "date": base_date + timedelta(days=28),
                "capacity": 80,
                "college_id": 4,
                "manager_id": 4,
                "registrations_count": 60
            },
            {
                "id": 5,
                "title": "Sports Day",
                "description": "Inter-college sports competition",
                "type": "sports",
                "date": base_date - timedelta(days=7),
                "capacity": 300,
                "college_id": 1,
                "manager_id": 1,
                "registrations_count": 250
            }
        ]
        
        for event_data in events_data:
            event = models.Event(**event_data)
            db.add(event)
        
        # Create sample registrations
        registrations_data = [
            {"id": 1, "student_id": 1, "event_id": 1, "timestamp": base_date - timedelta(days=5)},
            {"id": 2, "student_id": 2, "event_id": 1, "timestamp": base_date - timedelta(days=4)},
            {"id": 3, "student_id": 3, "event_id": 2, "timestamp": base_date - timedelta(days=6)},
            {"id": 4, "student_id": 4, "event_id": 2, "timestamp": base_date - timedelta(days=3)},
            {"id": 5, "student_id": 5, "event_id": 3, "timestamp": base_date - timedelta(days=8)},
            {"id": 6, "student_id": 6, "event_id": 3, "timestamp": base_date - timedelta(days=2)},
            {"id": 7, "student_id": 7, "event_id": 4, "timestamp": base_date - timedelta(days=9)},
            {"id": 8, "student_id": 8, "event_id": 4, "timestamp": base_date - timedelta(days=1)},
            {"id": 9, "student_id": 1, "event_id": 5, "timestamp": base_date - timedelta(days=10)},
            {"id": 10, "student_id": 3, "event_id": 5, "timestamp": base_date - timedelta(days=9)}
        ]
        
        for reg_data in registrations_data:
            registration = models.Registration(**reg_data)
            db.add(registration)
        
        # Create sample attendance (for past event)
        attendance_data = [
            {"id": 1, "registration_id": 9, "checkin_time": base_date - timedelta(days=7), "status": "on-time"},
            {"id": 2, "registration_id": 10, "checkin_time": base_date - timedelta(days=7, minutes=-20), "status": "late"}
        ]
        
        for att_data in attendance_data:
            attendance = models.Attendance(**att_data)
            db.add(attendance)
        
        # Create sample feedback (for attended events)
        feedback_data = [
            {"id": 1, "student_id": 1, "event_id": 5, "rating": 5, "comment": "Great event! Very well organized.", "sentiment": "positive"},
            {"id": 2, "student_id": 3, "event_id": 5, "rating": 4, "comment": "Good experience, could be improved.", "sentiment": "positive"}
        ]
        
        for feedback in feedback_data:
            db_feedback = models.Feedback(**feedback)
            db.add(db_feedback)
        
        db.commit()
        print("Sample data initialized successfully!")
        
    except Exception as e:
        print(f"Error initializing data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_sample_data()