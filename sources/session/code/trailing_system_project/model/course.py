class course:
    _id_counter =1
    def __init__(self,name):
        self.course_id =course._id_counter
        course._id_counter+=1
        
        self.name = name
        self.enrolled_student=[]
        
    def __str__(self):
        return f"course id: {self.course_id}, , name:{self.name}, enrolled: {len(self.enrolled_student)}"
    def enroll_student(self,student):
        if student not in self.enrolled_student:
            self.enrolled_student.append(student)
            print("student enrolled sucssesfully")
        else:
            print("student already enrolled")
            
    def remove_student(self, student):
        for course in self.courses.values():
            if student in course.enroll_student:
                course.enrolled_student.remove(student)