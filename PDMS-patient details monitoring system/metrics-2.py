# this code may be useful when days are stored instead of timestamp
# Eg: monday, tuesday ...

from registering_the_patient import Patient

# global variable

enumerating_days={'sunday':0,'monday':1,'tuesday':2,'wednesday':3,'thrusday':4,'friday':5,'saturday':6}

def check_city(city):
    if city.lower()=='bangalore':
        return True
    return False

def number_of_patients(day):  # day = monday and range of days = monday-sunday
    count=0
    patients_in_bangalore=0
    patients_out_of_bangalore=0
    day_or_days_list=day.split('-')
    if len(day_or_days_list)==1:
        for item in Patient.get_details():
            for key,values in item.items():
                if check_city(values[0]):
                    patients_in_bangalore+=1
                else:
                    patients_out_of_bangalore+=1
                if values[1]==day:
                    count+=1
        return ['Number of Patients registered on {0}: {1}'.format(day,count),
                'Number of patients from Bangalore {0}: '.format(patients_in_bangalore),
                'Number of patients out of Bangalore {0}: ]'.format(patients_out_of_bangalore),
                patients_in_bangalore,patients_out_of_bangalore]
    lower_bound=enumerating_days[day_or_days_list[0]]
    upper_bound=enumerating_days[day_or_days_list[1]]
    if lower_bound>upper_bound:   # swapping the lowest with largest
        lower_bound,upper_bound=upper_bound,lower_bound
    for item in Patient.get_details():
        for key,values in item.items():
            if check_city(values[0]):
                patients_in_bangalore += 1
            else:
                patients_out_of_bangalore += 1
            if lower_bound<=enumerating_days[values[1]]<=upper_bound:
                count+=1
    return ['Number of Patients registered on {0}-{1}: {2}'.format(day_or_days_list[0],day_or_days_list[1],count),
            'Number of patients from Bangalore {0}: '.format(patients_in_bangalore),
            'Number of patients out of Bangalore {0}: ]'.format(patients_out_of_bangalore),
            patients_in_bangalore,patients_out_of_bangalore]