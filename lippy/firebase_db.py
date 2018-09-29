from firebase.firebase import FirebaseAuthentication
from firebase.firebase import FirebaseApplication
from datetime import datetime
import operator


def no_of_parked_cars_daily(carData, carArray_Date_Key, latest_no_of_days = None):
    """
    """
    if latest_no_of_days is None:
        start = 0
        end = len(carArray_Date_Key)
    else:
        """
        TODO: Implement firstOccurenceBinarySearch and lastOccurenceBinarySearch to identify the range of data to compare
            - Requires the current date - latest_no_of_days to know which date to start performing computation
        """
        #start = firstOccurenceBinarySearch(carArray_Date_Key...)
        #end = lastOccurenceBinarySearch(carArray_Date_Key...) + 1
        pass

    curr_date = None
    no_of_cars_entry = 0
    car_data = []
    for i in range(start, end):
        #print(carArray_Date_Key[i])
        if curr_date is None:
            curr_date = split_date_time_format(carArray_Date_Key[i][0], get_data = 0)

        elif curr_date == split_date_time_format(carArray_Date_Key[i][0], get_data = 0):
            #If the car is entering the carpark zone
            if carData['carEvents'][carArray_Date_Key[i][1]]['Event'] == 'Entry':
                no_of_cars_entry += 1
                
        else:

            #car_data[curr_date] = no_of_cars_entry
            car_data.append([curr_date, no_of_cars_entry])

            if carData['carEvents'][carArray_Date_Key[i][1]]['Event'] == 'Entry':
                no_of_cars_entry = 1
            else:
                no_of_cars_entry = 0
            curr_date = split_date_time_format(carArray_Date_Key[i][0], get_data = 0)

        if i == len(carArray_Date_Key) - 1:
            car_data.append([curr_date, no_of_cars_entry])
            
    return car_data


def get_peak_number_cars_parked(carData, carArray_Date_Key, first_boundary = None):
    """
    Can selective set which date is the one it is looking for

    Can further improve to compare datetime object, instead of date string comparison

    In the future, can set a initial starting line (boundary) to prevent past calculation
    """
    curr_date = None
    no_of_cars_entry = 0
    peak_cars_entry = 0
    date_of_peak = None
    for i in range(len(carArray_Date_Key)):
        #print(carArray_Date_Key[i])
        if curr_date is None:
            curr_date = split_date_time_format(carArray_Date_Key[i][0], get_data = 0)

        elif curr_date == split_date_time_format(carArray_Date_Key[i][0], get_data = 0):
            #If the car is entering the carpark zone
            if carData['carEvents'][carArray_Date_Key[i][1]]['Event'] == 'Entry':
                no_of_cars_entry += 1
                
        else:

            if no_of_cars_entry > peak_cars_entry:
                date_of_peak = curr_date
                peak_cars_entry = no_of_cars_entry

            if carData['carEvents'][carArray_Date_Key[i][1]]['Event'] == 'Entry':
                no_of_cars_entry = 1
            else:
                no_of_cars_entry = 0
            curr_date = split_date_time_format(carArray_Date_Key[i][0], get_data = 0)

        if i == len(carArray_Date_Key) - 1:
            if no_of_cars_entry > peak_cars_entry:
                date_of_peak = curr_date
                peak_cars_entry = no_of_cars_entry
        
            
    return peak_cars_entry, date_of_peak

def split_date_time_format(date_time_input, get_data):
    """
    get_data = 0, returns date object only
    get_data = 1, returns both date-time object
    Returns datetime object, containing date data only
    """
    date = date_time_input.split(' ')
    if get_data == 0:
        return datetime.strptime(date[0], '%d-%m-%Y')
    elif get_data == 1:
        return datetime.strptime(date[0] + ' ' + date[1], '%d-%m-%Y %H:%M:%S')


def sort_car_data_in_order_timestamp(carData):
    """
    """
    carEvents = carData['carEvents']
    carEvents_keys = carEvents.keys()

    toBeSorted_data = []
    for key in carEvents_keys:
        #print(carEvents[key].keys())
        try:
            data = [carEvents[key]['Date'] + ' ' + carEvents[key]['Time'], key]
        except Exception:
            print("Error in car data")
            continue
        toBeSorted_data.append(data)

    sorted_data = sorted(toBeSorted_data)
    
    return sorted_data
    
def sort_light_data_in_order_timestamp(lightData):
    """
    """
    lightEvents = lightData['lightEvents']
    lightEvent_keys = lightEvents

    toBeSorted_data = []
    for key in lightEvent_keys:
        try:
            data = [lightEvents[key]['Date'] + ' ' + lightEvents[key]['Time'], key]
        except Exception:
            print("Error in light data")
            continue
        toBeSorted_data.append(data)

    sorted_data = sorted(toBeSorted_data)

    return sorted_data

def calculate_energy_saved_spent_theoretical(lightData, sortedLightData, NoOfLights):
    """
    This function doesn't work if it is the next day

    This is meant to calculate energy used per day - Future implementations can attempt to fix this issue by blocking computation if it hits the next day
    #TODO ^
    """

    if len(sortedLightData) == 0:
        return False

    #Used dictionary because the Light_ID could be randomly named
    light_tracker = {}

    results = []
    total_hours_100_percent = 0
    
    curr_date = sortedLightData[0][0].split(' ')[0]
    for timestamp_key in sortedLightData:
        light_id = lightData['lightEvents'][timestamp_key[1]]['Light_ID']
        curr_light_log_data = lightData['lightEvents'][timestamp_key[1]]
        #Since data is already sorted, if the compare_date finds a different date, then it must be in ascending order
        compare_date = timestamp_key[0].split(' ')[0]
        if compare_date == curr_date:
            #If the light_id was never registered
            if light_id not in light_tracker:
                if curr_light_log_data['Light_intensity'] == '100%':
                    light_tracker[light_id] = curr_light_log_data['Time']

            #If the light_id was registered before
            elif light_tracker[light_id] is None:
                if curr_light_log_data['Light_intensity'] == '100%':
                    light_tracker[light_id] = curr_light_log_data['Time']

            #If the light_id has data stored inside
            else:
                #Don't need to overwrite data, only overwrite when the light dims
                if curr_light_log_data['Light_intensity'] == '100%':
                    continue
                #Assume that dimming is only 50%
                elif curr_light_log_data['Light_intensity'] == '50%':
                    """
                    TODO: If want to make it work across days, will have to change implementation (CORE) here
                    """
                    stored_time = datetime.strptime(light_tracker[light_id], '%H:%M:%S')
                    curr_time = datetime.strptime(curr_light_log_data['Time'], '%H:%M:%S')
                    seconds = curr_time - stored_time
                    seconds = seconds.seconds
                    hours = (seconds/60)/60
                    total_hours_100_percent += hours
                    
                    light_tracker[light_id] = None
        else:
            results.append([curr_date, total_hours_100_percent])
            total_hours_100_percent = 0
            curr_date = timestamp_key[0].split(' ')[0]
            if compare_date == curr_date:
                #If the light_id was never registered
                if light_id not in light_tracker:
                    if curr_light_log_data['Light_intensity'] == '100%':
                        light_tracker[light_id] = curr_light_log_data['Time']

                #If the light_id was registered before
                elif light_tracker[light_id] is None:
                    if curr_light_log_data['Light_intensity'] == '100%':
                        light_tracker[light_id] = curr_light_log_data['Time']

                #If the light_id has data stored inside
                else:
                    #Don't need to overwrite data, only overwrite when the light dims
                    if curr_light_log_data['Light_intensity'] == '100%':
                        continue
                    #Assume that dimming is only 50%
                    elif curr_light_log_data['Light_intensity'] == '50%':
                        """
                        TODO: If want to make it work across days, will have to change implementation (CORE) here
                        """
                        stored_time = datetime.strptime(light_tracker[light_id], '%H:%M:%S')
                        curr_time = datetime.strptime(curr_light_log_data['Time'], '%H:%M:%S')
                        seconds = curr_time - stored_time
                        hours = (seconds/60)/60
                        total_hours_100_percent += hours
                        
                        light_tracker[light_id] = None

    results.append([curr_date, total_hours_100_percent])
                    
    return results
    


if __name__ == '__main__':
    energySavingApp = FirebaseApplication('https://mdec-5edc2.firebaseio.com/', None)
    #authentication = FirebaseAuthentication('nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCs1xNyg7FeRtHI\nKWfSRFDRAoo7N+rLH4y0U6PKzfi9hvOyS0Z9/VXrptQzsyQoh/l8PQdt/hxVA3Zj\nxQP33s4OwkEDc1BpF+8McxivcuvTkVbIegpOtoVm4wg1FHIVNHgSqZrXeYhiOHVW\nXkObFO/4SXbfBh0Ny470wJudcZVewDNLnyq/h0GJY+xSkR3XOCAg1TigYmO4PXIl\nRjZfYnbyHbRyxqiJRKD0lQtykWuIP8fudOmK0CmRoqfmK9q6kS6GSbLHVbUtESwI\nmyaKriFpUROSyOTMIOovo3TkH+EzluJrzmiTbujXTVK32PO9Kz17bf1rxOfKrCa0\nRn+S9103AgMBAAECggEABFbRi0S8HYCyQCl6v+AgL62CvxhylNvhzx5XoXFI7XUn\nknidhSJoveXhZ1TeTQT9rr1KsPVTf8NHY+gGM/q/eizG4tyW9OesnceyVtrc1pUy\nmqdAF/7KdZOwjCiYJQK9GvbWemwq9nayMQaXzhsyweB4rM7jlT0thX59lnCYdLL2\nHzG8xCIR5JiV/CCmpKoi5sjow8vHwH7xlFK1pED1gxiRBaTIimtwndyRwadSGxNn\ngCP/0K4hWNeebhU38c4kVIPWshIW49tCkyDAwjoxwy/5cmYpe2Leuh1JuQBKUAC1\n04Gsff0UPCjBvZpdg4QLELzR65fFgVi8YoL5Cx6NDQKBgQDt5XH2dxj05ZRuo+uR\neda4jC0quZGClmUfNqKL9IzrFxSbum9pN74WFhpYkvsQyuYCk3crWzcrNX1SSXXN\n3nh3NOJ24oAiiMKvE9bctBpI9gNc5p3ZODSyW0s3IQa+THMdS2NbZN0a7WHGNSbi\nuNNFHQDInP4tduI78Cac2KWLMwKBgQC5/j7izXVv5ye7T6qELZXAf/H0PkTKP3iP\nKwcAuz7Tt1xqLB41cA5m8ScgQL6FD9xpdEZ9hiHhsCgftsAI/09LD9cqyuYiW4by\n1igurKbsSqQUMGgefZozuWSy2UyuyJvGliwZGzfR/ABiDhOPPQSXBCceDsoK1EXA\nAFSrngyF7QKBgQCbhZBHK/zovN2YpxjtddVluF4evEngMSnSigkhrbIiTmhulicX\nhhWCoth+Zzgy9jIAJR+W/H7IhKN1FAkrmPDwHWafidtyuC1t/25LwoIciJgSN8Gh\nrBjnML+vPqwF5DytPgeqS/owDFgLF9xgA6w6VoeYnumcF0g3HvxfNVKj+QKBgHTg\nduYRFE4opQgI7O84shUQkZvZEWNCdWEKOdFU2Qsz+0fgx27vJq27tsmGxfJZ4DkI\nT0+L3Xi0ONKNBanhvhM+Ngj3DZzjhS7OMtv5tL9hvC/Pp24ZobAFPWlCMfTXrUQi\nlD2GpBI5WIhFrjbhsiOwAWDbDE23zMj1rD9YByiVAoGBAMsSe/V//91/gkKO3OKZ\ngYv3RIjfon2YORLRnxJzjErr5zUcnr6LH10ixg2Ufa86IhuL6yMBDQ/2mlyaXdlC\nwhrPdOxnleLdOxJZUXSdVKCcPTWCXbHil3aIAYfR+g3kD98BaHWH1HZRGmm1Z+R4\nY2MIVyzkKtCP8XgsslaYIWiS', 'gabrieltan19@gmail.com', extra = {'id':123})
    #app.authentication = authentication
    #user = authentication.get_user()

    #print(authentication.extra)
    #print(user.firebase_auth_token)

    carData = energySavingApp.get('/car', None)
    lightData = energySavingApp.get('/light', None)

    #result = no_of_parked_cars_average_daily(carData)
    car_date_key_timestamp_sorted = sort_car_data_in_order_timestamp(carData)
    light_date_key_timestamp_sorted = sort_light_data_in_order_timestamp(lightData)

    #Obtain peak number of cars entry
    info = get_peak_number_cars_parked(carData, car_date_key_timestamp_sorted)
    info2 = no_of_parked_cars_daily(carData, car_date_key_timestamp_sorted)

    #This part is hardcoded - It is known that the number of lights in the parking location is only 30
    no_of_LED = 30

    #calculate_energy_saved_spent_theoretical(lightData, light_date_key_timestamp_sorted, no_of_LED)
    a = calculate_energy_saved_spent_theoretical(lightData, light_date_key_timestamp_sorted, no_of_LED)
