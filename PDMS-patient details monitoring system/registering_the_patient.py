
from datetime import datetime

class Patient:
    patient_location_date=[] # this is the class variable that has info about the patient_name and location
    def __init__(self,person_name,age,health_problem,location,date):
        self.person_name=person_name
        self.age=age
        self.health_problem=health_problem
        self.location=location
        self.date=datetime.timestamp(datetime.strptime(date,'%Y-%m-%d')) # storing the timestamp of the date
        Patient.patient_location_date.append({self.person_name: [self.location,self.date]})

    @classmethod
    def get_details(self):
        print(Patient.patient_location_date)
        return Patient.patient_location_date

