from datetime import datetime
from app import app
from extensions import db
from models.course import Course
from models.student import Student

class TestModels:
    '''Test suite for the models in the models directory.'''

    def setup_method(self):
        '''Set up test database.'''
        with app.app_context():
            db.create_all()

    def teardown_method(self):
        '''Tear down test database.'''
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_course_model(self):
        '''Test Course model columns and relationships.'''
        with app.app_context():
            course = Course(name="Mathematics")
            db.session.add(course)
            db.session.commit()

            assert course.id is not None
            assert isinstance(course.id, str)  
            assert course.name == "Mathematics"
            assert course.deleted is False
            assert isinstance(course.created_at, datetime)
            assert course.updated_at is None
            assert course.students == []

    def test_student_model(self):
        '''Test Student model columns and relationships.'''
        with app.app_context():
            course = Course(name="Physics")
            db.session.add(course)
            db.session.commit()

            student = Student(name="Alice", course=course, fee_balance=50000)
            db.session.add(student)
            db.session.commit()

            assert student.id is not None
            assert isinstance(student.id, str) 
            assert student.name == "Alice"
            assert student.course_id == course.id
            assert student.fee_balance == 50000
            assert student.deleted is False
            assert isinstance(student.created_at, datetime)
            assert student.updated_at is None

    def test_to_dict_methods(self):
        '''Test the to_dict method in Course and Student.'''
        with app.app_context():
            course = Course(name="Chemistry")
            db.session.add(course)
            db.session.commit()

            student = Student(name="Bob", course=course, fee_balance=100000)
            db.session.add(student)
            db.session.commit()

            course_dict = course.to_dict()
            student_dict = student.to_dict()

            assert course_dict['id'] == course.id
            assert course_dict['name'] == "Chemistry"

            assert student_dict['id'] == student.id
            assert student_dict['name'] == "Bob"
            assert student_dict['course'] == course.id
            assert student_dict['fee_balance'] == 100000
