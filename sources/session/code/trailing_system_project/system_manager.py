from course import course
from student import student

class SystemManager:
    def __init__(self):
        self.students={}
        self.courses={}
        
    def add_student(self,name):
        student=student(name)
        self.students[student.student_id]=student
        print("student added sucssesfully")
        return student.student_id
    def remove_student(self,student_id):
        if student_id in self.students:
            student = self.students[student_id]
            if not student.enrolled_courses:
                del self.students[student_id]
                print("student removed sussesfully")
            else:
                print("student has enrolled courses. cannot removed")
        else:
            print("invaid student id")
    def enroll_course(self,student_id,course_id):
        if student_id in self.students and course_id in self.courses:
            student=self.students[student_id]
            course=self.courses[course_id]
            
            if course.name not in student.enrolled_courses:
                student.enrolled_in_course(course.name)
                course.enroll_student(student.name)
                print("student enrolled in course sucssesfully.")
            else:
                print("student is already enrolled in the course")
        else:
            print("invalid student or course id")
            
    def record_grade(self, student_id, course_id,grade):
        if student_id in self.students and course_id in self.courses:
            student = self.students[student_id]
            course= self.courses[course_id]
            student.add_grades(course.name, grade)
            print("grade recorded")
        else:
            print("invalid student or course id")
            
    def get_all_students(self):
        return list(self.students.values)
    def get_all_courses(self):
        return list(self.courses.values)