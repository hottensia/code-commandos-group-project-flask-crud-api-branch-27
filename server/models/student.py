from extensions import db
from models.base import BaseModel

class Student(BaseModel):
    __tablename__ = "students"

    name = db.Column(db.String(50), nullable=False)
    course_id = db.Column(db.String(36), db.ForeignKey("courses.id"))
    course = db.relationship('Course', back_populates='students')
    fee_balance = db.Column(db.Integer, nullable=False, default=0)

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "name": self.name,
            "course": self.course_id,
            "fee_balance": self.fee_balance,
        })
        return data

