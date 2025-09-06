from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, College, Student, EventManager, Event
from datetime import datetime, timedelta

# Create tables
Base.metadata.create_all(bind=engine)

def seed_database():
    db = SessionLocal()
    
    # Create colleges
    colleges = [
        College(name="Engineering College"),
        College(name="Arts & Science College"),
        College(name="Business College"),
        College(name="Medical College")
    ]
    
    for college in colleges:
        db.add(college)
    db.commit()
    
    # Create event managers
    managers = [
        EventManager(name="John Doe", email="john@engineering.edu", college_id=1),
        EventManager(name="Jane Smith", email="jane@arts.edu", college_id=2),
        EventManager(name="Bob Johnson", email="bob@business.edu", college_id=3),
        EventManager(name="Alice Brown", email="alice@medical.edu", college_id=4)
    ]
    
    for manager in managers:
        db.add(manager)
    db.commit()
    
    # Create students
    students = [
        Student(name="Alice Johnson", email="alice@student.edu", college_id=1),
        Student(name="Bob Smith", email="bob@student.edu", college_id=1),
        Student(name="Carol Brown", email="carol@student.edu", college_id=2),
        Student(name="David Wilson", email="david@student.edu", college_id=2),
        Student(name="Eve Davis", email="eve@student.edu", college_id=3),
        Student(name="Frank Miller", email="frank@student.edu", college_id=3),
        Student(name="Grace Lee", email="grace@student.edu", college_id=4),
        Student(name="Henry Taylor", email="henry@student.edu", college_id=4)
    ]
    
    for student in students:
        db.add(student)
    db.commit()
    
    # Create events
    events = [
        Event(
            title="Tech Conference 2024",
            description="Annual technology conference featuring latest innovations",
            type="Conference",
            date=datetime.now() + timedelta(days=30),
            capacity=100,
            college_id=1,
            manager_id=1
        ),
        Event(
            title="Art Exhibition",
            description="Student art exhibition showcasing creative works",
            type="Exhibition",
            date=datetime.now() + timedelta(days=15),
            capacity=50,
            college_id=2,
            manager_id=2
        ),
        Event(
            title="Business Workshop",
            description="Entrepreneurship workshop for business students",
            type="Workshop",
            date=datetime.now() + timedelta(days=45),
            capacity=75,
            college_id=3,
            manager_id=3
        ),
        Event(
            title="Medical Symposium",
            description="Medical research symposium with guest speakers",
            type="Symposium",
            date=datetime.now() + timedelta(days=60),
            capacity=200,
            college_id=4,
            manager_id=4
        ),
        Event(
            title="Cross-College Sports Day",
            description="Inter-college sports competition",
            type="Sports",
            date=datetime.now() + timedelta(days=20),
            capacity=300,
            college_id=1,
            manager_id=1
        )
    ]
    
    for event in events:
        db.add(event)
    db.commit()
    
    print("Database seeded successfully!")
    db.close()

if __name__ == "__main__":
    seed_database()