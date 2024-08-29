from extensions import db
from models.base import BaseModel

class Course(BaseModel):
    __tablename__ = "courses"

    name = db.Column(db.String(50), nullable=False)
    students = db.relationship('Student', back_populates='course')

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "name": self.name,
        })
        return data
    