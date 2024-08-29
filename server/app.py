from flask import Flask
from flask_restful import Api
from extensions import db, cache
from resources.student import StudentResource
from resources.student_list import StudentListResource
from resources.restore_student import RestoreStudentResource
from resources.course_list import CourseListResource
from resources.closest_subset import FindClosestSubsetResource

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///students.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["CACHE_TYPE"] = "SimpleCache"
app.config["CACHE_DEFAULT_TIMEOUT"] = 300

db.init_app(app)
cache.init_app(app)

api = Api(app)

api.add_resource(StudentListResource, '/students')
api.add_resource(StudentResource, '/students/<string:student_id>')
api.add_resource(RestoreStudentResource, '/students/<string:student_id>/restore')
api.add_resource(CourseListResource, '/courses')
api.add_resource(FindClosestSubsetResource, '/find_closest_subset')

if __name__ == "__main__":
    app.run()
