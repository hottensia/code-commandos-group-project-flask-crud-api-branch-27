import pytest
from app import app
from extensions import db, cache
from models.course import Course
from models.student import Student
from services.student_service import StudentService
from flask import json

student_service = StudentService()

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

def test_course_list_resource(client):
    # Setup
    course1 = Course(name="Math")
    course2 = Course(name="Science")
    db.session.add_all([course1, course2])
    db.session.commit()

    # Test
    response = client.get('/courses')
    assert response.status_code == 200
    courses = json.loads(response.data)
    assert len(courses) == 2
    assert courses[0]["name"] == "Math"
    assert courses[1]["name"] == "Science"

def test_restore_student_resource(client):
    # Setup
    student = Student(name="John Doe", fee_balance=500)
    db.session.add(student)
    db.session.commit()
    student_service.soft_delete_student(student.id)

    # Test restore student
    response = client.post(f'/students/{student.id}/restore')
    assert response.status_code == 200
    restored_student = json.loads(response.data)
    assert restored_student["name"] == "John Doe"
    assert restored_student["deleted"] is False

def test_student_list_resource_get(client):
    # Setup
    student1 = Student(name="John Doe", fee_balance=500)
    student2 = Student(name="Jane Doe", fee_balance=300)
    db.session.add_all([student1, student2])
    db.session.commit()

    # Test GET all students
    response = client.get('/students')
    assert response.status_code == 200
    students = json.loads(response.data)
    assert len(students) == 2
    assert students[0]["name"] == "John Doe"
    assert students[1]["name"] == "Jane Doe"

def test_student_list_resource_post(client):
    # Test POST new student
    response = client.post('/students', json={"name": "John Doe", "course": "Math"})
    assert response.status_code == 201
    new_student = json.loads(response.data)
    assert new_student["name"] == "John Doe"

def test_student_resource_get(client):
    # Setup
    student = Student(name="John Doe", fee_balance=500)
    db.session.add(student)
    db.session.commit()

    # Test GET student by ID
    response = client.get(f'/students/{student.id}')
    assert response.status_code == 200
    retrieved_student = json.loads(response.data)
    assert retrieved_student["name"] == "John Doe"

def test_student_resource_put(client):
    # Setup
    student = Student(name="John Doe", fee_balance=500)
    db.session.add(student)
    db.session.commit()

    # Test PUT update student
    response = client.put(f'/students/{student.id}', json={"name": "John Updated", "course": "Science"})
    assert response.status_code == 200
    updated_student = json.loads(response.data)
    assert updated_student["name"] == "John Updated"

def test_student_resource_delete(client):
    # Setup
    student = Student(name="John Doe", fee_balance=500)
    db.session.add(student)
    db.session.commit()

    # Test DELETE student by ID
    response = client.delete(f'/students/{student.id}')
    assert response.status_code == 204

