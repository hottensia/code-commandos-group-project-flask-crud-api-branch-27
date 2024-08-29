import pytest
from app import app
from extensions import db
from models.student import Student
from models.course import Course
from services.student_service import StudentService

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

def test_retrieve_all_students(client):
    # Setup
    course = Course(name="Math")
    student1 = Student(name="John Doe", course=course)
    student2 = Student(name="Jane Doe", course=course, deleted=True)
    db.session.add_all([course, student1, student2])
    db.session.commit()

    # Test retrieve all non-deleted students
    students = student_service.retrieve_all_students()
    assert len(students) == 1
    assert students[0].name == "John Doe"

def test_retrieve_student_by_id(client):
    # Setup
    course = Course(name="Math")
    student = Student(name="John Doe", course=course)
    db.session.add_all([course, student])
    db.session.commit()

    # Test retrieve existing student by ID
    retrieved_student = student_service.retrieve_student_by_id(student.id)
    assert retrieved_student is not None
    assert retrieved_student.name == "John Doe"

    # Test retrieve non-existing student by ID
    non_existing_student = student_service.retrieve_student_by_id(999)
    assert non_existing_student is None

def test_add_student(client):
    # Setup
    course = Course(name="Math")
    db.session.add(course)
    db.session.commit()

    # Test adding a new student
    new_student = student_service.add_student(name="John Doe", course_id=course.id)
    assert new_student is not None
    assert new_student.name == "John Doe"
    assert new_student.course.name == "Math"

def test_update_a_student(client):
    # Setup
    course1 = Course(name="Math")
    course2 = Course(name="Science")
    student = Student(name="John Doe", course=course1)
    db.session.add_all([course1, course2, student])
    db.session.commit()

    # Test updating a student's name and course
    updated_student = student_service.update_a_student(student.id, name="John Updated", course=course2.id)
    assert updated_student is not None
    assert updated_student.name == "John Updated"
    assert updated_student.course.name == "Science"

def test_soft_delete_student(client):
    # Setup
    course = Course(name="Math")
    student = Student(name="John Doe", course=course)
    db.session.add_all([course, student])
    db.session.commit()

    # Test soft deleting a student
    success = student_service.soft_delete_student(student.id)
    assert success is True

    # Verify that the student is marked as deleted
    deleted_student = student_service.retrieve_student_by_id(student.id, include_deleted=True)
    assert deleted_student.deleted is True

def test_restore_student(client):
    # Setup
    course = Course(name="Math")
    student = Student(name="John Doe", course=course, deleted=True)
    db.session.add_all([course, student])
    db.session.commit()

    # Test restoring a deleted student
    restored_student = student_service.restore_student(student.id)
    assert restored_student is not None
    assert restored_student.deleted is False
