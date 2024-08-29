from flask_restful import Resource
from models.course import Course

class CourseListResource(Resource):
    def get(self):
        return [course.to_dict() for course in Course.query.all()], 200
    