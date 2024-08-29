from flask_restful import Resource, reqparse
from extensions import cache
from utils.cache_log import log_cache_access
from services.student_service import StudentService

student_service = StudentService()

class StudentListResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, required=True, help="Name must be a string")
        self.reqparse.add_argument('course', type=str, required=True, help="Course must be a string")
    
    def get(self):
        cache_key = "all_students"
        students = cache.get(cache_key)
        if students is not None:
           log_cache_access(cache_key, hit=True)
           return [student.to_dict() for student in students], 200
        else:
            students = student_service.retrieve_all_students()
            cache.set(cache_key, students, timeout=300)
            log_cache_access(cache_key, hit=False)
            return [student.to_dict() for student in students], 200
    
    def post(self):
        args = self.reqparse.parse_args()
        new_student = student_service.add_student(args['name'], args['course'])
        return new_student.to_dict(), 201