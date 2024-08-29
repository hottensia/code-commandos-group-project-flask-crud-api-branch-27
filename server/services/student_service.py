from extensions import db, cache
from models.course import Course
from models.student import Student
from itertools import combinations


# Business Logic - What controls the information input in the database and how to manipulate
class StudentService:
    def make_cache_key(self, student_id):
        """Generate a custom cache key based on student_id."""
        return f"student_{student_id}"

    @cache.cached(timeout=300, key_prefix="all_students")
    def retrieve_all_students(self, include_deleted=False):
        if include_deleted:
            return db.session.query(Student).all()
        return db.session.query(Student).filter_by(deleted=False).all()

    def retrieve_student_by_id(self, student_id, include_deleted=False):
        if include_deleted:
            return db.session.get(Student, student_id) 
        return db.session.query(Student).filter_by(id=student_id, deleted=False).first()

    def add_student(self, name, course_id):
        course = db.session.get(Course, course_id)  
        new_student = Student(name=name, course=course)
        db.session.add(new_student)
        db.session.commit()
        cache.delete("all_students")
        return new_student
    
    def update_a_student(self, student_id, name=None, course=None):
        student = self.retrieve_student_by_id(student_id, include_deleted=True)
        if student:
            if name:
                student.name = name
            if course:
                course_obj = db.session.get(Course, course)  
                if course_obj:
                    student.course = course_obj
            db.session.commit()
            cache.delete(self.make_cache_key(student_id))
            cache.delete("all_students")
            return student
        return None

    def soft_delete_student(self, student_id):
        student = self.retrieve_student_by_id(student_id, include_deleted=True)
        if student:
            student.deleted = True
            db.session.commit()
            cache.delete(self.make_cache_key(student_id))
            cache.delete("all_students")
            return True
        return False
    
    def restore_student(self, student_id):
        student = self.retrieve_student_by_id(student_id, include_deleted=True)
        if student:
            student.deleted = False
            db.session.commit()
            cache.delete(self.make_cache_key(student_id))
            cache.delete("all_students")
            return student
        return None
    
    def find_closest_subset(self, target_amount):
        if target_amount <= 0:
            raise ValueError("Target amount must be greater than zero")
        
        students = self.retrieve_all_students(include_deleted=False)
        fee_balances = [student.fee_balance for student in students]
        student_dict = {student.fee_balance: student for student in students}

        closest_sum = float('inf')
        closest_subset = []

        for r in range(1, len(students) + 1):
            for subset in combinations(fee_balances, r):
                current_sum = sum(subset)
                if abs(current_sum - target_amount) < abs(closest_sum - target_amount):
                    closest_sum = current_sum
                    closest_subset = subset

        closest_students = [student_dict[fee_balance] for fee_balance in closest_subset]

        return closest_students, closest_sum