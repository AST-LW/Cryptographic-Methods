from registering_the_patient import Patient
from datetime import date,datetime

def check_city(city):
    if city.lower()=='bangalore':
        return True
    else:
        return False

def convert_to_timestamp(date):
    return datetime.timestamp(datetime.strptime(date,'%Y-%m-%d'))

def number_of_patients(days=0):  # default gives that day registrations
    current_date=date.today()
    current_date=convert_to_timestamp(str(current_date))  # for comparing purposes
    number_of_days_in_seconds=days*86400
    if days!=0: # when number of days not equal to zero
        previous_date=current_date-number_of_days_in_seconds
    else:
        previous_date=current_date
    count=0
    patients_in_bangalore=0
    patients_out_of_bangalore=0
    for item in Patient.get_details():
        for key,value in item.items():
            if previous_date<=value[1]<=current_date:  # including the present day
                count+=1
                if check_city(value[0]):
                    patients_in_bangalore += 1
                else:
                    patients_out_of_bangalore += 1
    return [count,patients_in_bangalore,patients_out_of_bangalore]

def percentage_calculation(in_bangalore,out_bangalore):
    in_bangalore_percntage=(in_bangalore/(in_bangalore+out_bangalore))*100
    out_bangalore_percentage=100-in_bangalore_percntage
    return [in_bangalore_percntage,out_bangalore_percentage]
