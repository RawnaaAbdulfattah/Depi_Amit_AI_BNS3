from models.hospital import Hospital
from models.department import Department
from models.patient import Patient
from models.staff import Staff

if __name__ == "__main__":
    hospital = Hospital("City Hospital", "123 Main St")   
                 # Create a department
    department=input("Enter the department: ")
    department = Department(department)
    hospital.add_department(department)

                # Create a patient   
    patient_name=input("Enter the patient name: ")
    patient_age=float(input("enter the patient age: "))
    patient_allergies=input("Enter the patient allergies: ")
    patient1 = Patient(patient_name,patient_age, patient_allergies)
    department.add_patient(patient1)

                # Create a staff member
    staff_name=input("Enter staff name: ")
    staff_age=float(input("Enter staff age: "))
    staff_position=input("Enter your position: ")
    doctor1 = Staff(staff_name, staff_age, staff_position)
    department.add_staff(doctor1)

                # View patient and staff records
    print(patient1.view_record())
    print(doctor1.view_info())