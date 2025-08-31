"""
doc
"""


class student:
    _id_counter=1
    
    def __init__(self,name):
        self.name=name
        student._id_counter+=1
        self.student_id=student._id_counter
        self.grades = {}
        self.enrolled_courses = []
    def __str__(self):
        return f"student id: {self.student_id}, name : {self.name}"
    def __repr__(self):
        return f"student id: {self.student_id}, name : {self.name}"
    def info(self):
        return self.name
    def add_grade(self,course_id, grade):
        self.grades[course_id]=grade
    def enrolled_in_course(self,course):
        self.enrolled_courses.append(course)
    