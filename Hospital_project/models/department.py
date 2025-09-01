from .patient import Patient
from .staff import Staff
class Department:
    """Class representing a department in the hospital."""
    def __init__(self, name):
        self.name = name
        self.patients = []  # List to hold patients
        self.staff = []     # List to hold staff

    def add_patient(self, patient):
        """Add a patient to the department."""
        self.patients.append(patient)
        print(f"Patient '{patient.name}' added to {self.name} department.")

    def add_staff(self, staff_member):
        """Add staff member to the department."""
        self.staff.append(staff_member)
        print(f"Staff '{staff_member.name}' added to {self.name} department.")