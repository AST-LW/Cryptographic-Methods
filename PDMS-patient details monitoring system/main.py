from registering_the_patient import Patient
from metrics import number_of_patients,percentage_calculation

def register_the_patient():
    patient_name=input('Enter the Patient Name: ')
    patient_age=int(input('Enter the age: '))
    patient_health_problem=input('Enter the health problem: ')
    patient_location=input('Enter the location from where the patient came: ')
    date=input('Enter the Date: ') # 'yy-mm-dd' format
    Patient(patient_name,patient_age,patient_health_problem,patient_location,date)
    return

def register():
    flag=input(':::REGISTER::: ')  # yes or no response
    while flag!='No':
        register_the_patient()
        flag=input(':::REGISTER ANOTHER PATIENT::: ')
    return 'The Details of the patients location are as follows: {0}'.format(Patient.get_details())

def main():
    register()
    days=int(input('Enter the number of days to check the record: '))
    count,in_bangalore,out_bangalore=number_of_patients(days)
    try:
        in_bangalore_percentage,out_bangalore_percentage=percentage_calculation(in_bangalore,out_bangalore)
        return 'Total patients {0}, {1}% are from Bangalore and {2}% are out-of-station'.format(count,in_bangalore_percentage,
                                                                                            out_bangalore_percentage)
    except:
        return 'No patient on this day' # this happens when there are no patients on the particular day
                                        # technically this condition leads to divison-by-zero condition while calculating
                                        # percentage


# actual execution starts in main.py
print(main())