from flask_restful import Resource, reqparse
from utils.cache_log import log_cache_access
from extensions import cache
from services.student_service import StudentService

student_service = StudentService()

class StudentResource(Resource):
    def __init__(self) -> None:
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, help="Name must be a string")
        self.reqparse.add_argument('course', type=str, help="Course must be a string")

    def get(self, student_id):
        cache_key = f"student_{student_id}"
        student = cache.get(cache_key)
        if student is not None:
            log_cache_access(cache_key, hit=True)
            return student.to_dict(), 200
        else:
            student = student_service.retrieve_student_by_id(student_id, include_deleted=True)
            if student:
                cache.set(cache_key, student, timeout=300)
                log_cache_access(cache_key, hit=False)
                return student.to_dict(), 200
            return {"error": "Student not found"}, 404
    
    def put(self, student_id):
        args = self.reqparse.parse_args()
        student = student_service.update_a_student(student_id, name=args["name"], course=args["course"])
        if student:
            return student.to_dict(), 200
        return {"error": "Student not found"}, 404
    
    def delete(self, student_id):
        if student_service.soft_delete_student(student_id):
            return {"message": "Student deleted successfully"}, 204
        return {"error": "Student not found"}, 404