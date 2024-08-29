from flask_restful import Resource
from services.student_service import StudentService

student_service = StudentService()

class RestoreStudentResource(Resource):
    def post(self, student_id):
        restored_student = student_service.restore_student(student_id)
        if restored_student:
            return restored_student.to_dict(), 200
        return {"error": "Student not found or not deleted"}, 404