#!/usr/bin/env python3
from app import app
from extensions import db
from models.student import Student
from models.course import Course 
from faker import Faker

def seed_data():
    with app.app_context():
        db.drop_all()
        db.create_all()
 
        fake = Faker()

        courses = []
        for _ in range(5):
            course = Course(name=fake.sentence(nb_words=3))
            db.session.add(course)
            courses.append(course)

        db.session.commit()

        for _ in range(10):
            random_course = fake.random_element(courses)
            fee_balance = fake.random_int(min=0, max=100000)
            student = Student(name=fake.name(), course=random_course, fee_balance=fee_balance)
            db.session.add(student)

        db.session.commit()
        print("Successfully seeded the data.") 

if __name__ == "__main__":
    seed_data()
