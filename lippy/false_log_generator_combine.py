import random
import string
from random import randint


def force_leave_carpark_weekday(carplate_list, car_parking_status, date_exit, log_number, toWriteTo_Data, day):
    hour = 22
    minute = 12
    second = 32
    
    for i in range(len(car_parking_status)):
        if car_parking_status[i] == False:
            continue
        else:
            time_exit = str(hour).zfill(2) + ':'+ str(minute).zfill(2) + ':' + str(second).zfill(2)
            #Need to generate a list such that they all leave the carpark at night
            #print('{} - {} - Log: {} - Carplate: "{}" - Event: "{}"'.format(date_array[j], time_exit, log_number, carplate_list[i], "Exit"), end='\n')
            toWriteTo_Data[day].append('{} - {} - Log: {} - Carplate: "{}" - Event: "{}"'.format(date_exit, time_exit, log_number, carplate_list[i], "Exit"))
            car_parking_status[i] = False
            minute += randint(0, 2)
            second += randint(0, 59)

            if second >= 60:
                minute += 1
                second -= 60

            if minute >= 60:
                hour += 1
                minute -= 60
        log_number += 1

def force_leave_carpark_weekend(carplate_list, car_parking_status, date_exit, log_number, toWriteTo_Data, day):
    hour = 20
    minute = 6
    second = 21
    
    for i in range(len(car_parking_status)):
        if car_parking_status[i] == False:
            continue
        else:
            time_exit = str(hour).zfill(2) + ':'+ str(minute).zfill(2) + ':' + str(second).zfill(2)
            #Need to generate a list such that they all leave the carpark at night
            #print('{} - {} - Log: {} - Carplate: "{}" - Event: "{}"'.format(date_array[j], time_exit, log_number, carplate_list[i], "Exit"), end='\n')
            toWriteTo_Data[day].append('{} - {} - Log: {} - Carplate: "{}" - Event: "{}"'.format(date_exit, time_exit, log_number, carplate_list[i], "Exit"))
            car_parking_status[i] = False
            minute += randint(0, 2)
            second += randint(0, 59)

            if second >= 60:
                minute += 1
                second -= 60

            if minute >= 60:
                hour += 1
                minute -= 60
        log_number += 1


def sequential_time_in_weekday_generator(no_of_time_entries):
    """
    Time is based on the 24hr system
    """
    return_list = []
    hour_sections = int(no_of_time_entries/3)
    sub_hour_sections = int(no_of_time_entries/4)
    hour = 6
    minute = 0
    second = 1

    for i in range(no_of_time_entries):
        #increment_sec = randint(30,59)
        #increment_min = randint(0,30)
        increment_sec = randint(0, 30)
        increment_min = randint(3, 5)

        minute += increment_min
        second += increment_sec

        if second >= 60:
            second -= 60
            minute += 1

        if minute >= 60:
            minute -= 60
            hour += 1

        if hour >= 22:
            break

        return_list.append(str(hour).zfill(2) + ':'+ str(minute).zfill(2) + ':' + str(second).zfill(2))
    return return_list


def sequential_time_in_weekend_generator(no_of_time_entries):
    """
    Time is based on the 24hr system
    """
    return_list = []
    hour_sections = int(no_of_time_entries/3)
    sub_hour_sections = int(no_of_time_entries/4)
    hour = 10
    minute = 0
    second = 1

    for i in range(no_of_time_entries):
        increment_sec = randint(30, 59)
        increment_min = randint(10,30)

        minute += increment_min
        second += increment_sec

        if second >= 60:
            second -= 60
            minute += 1

        if minute >= 60:
            minute -= 60
            hour += 1

        if hour >= 20:
            break

        return_list.append(str(hour).zfill(2) + ':'+ str(minute).zfill(2) + ':' + str(second).zfill(2))
    return return_list
     


def car_plates_generator(no_of_plates):
    return_list = []
    for i in range(no_of_plates):
        return_list.append("W" + random_char_string_generator(2) + random_num_string_generator(4))
    return return_list
                                                                                    

def random_char_string_generator(no_of_char):
    return_string = ""
    for i in range(no_of_char):
        return_string += random.choice(string.ascii_uppercase)
    return return_string


def random_num_string_generator(no_of_num):
    return_string = ''
    for i in range(no_of_num):
        return_string += str(randint(0,9))
    return return_string


def lights_generator(no_of_lights):
    return [None]*no_of_lights


def lightUp_randomLights(list_of_lights, log_num, date_entry, time_input, toWriteTo_Data, day):
    hour, minute, second = time_input.split(':')
    hour, minute, second = int(hour), int(minute), int(second)

    second += 1
    if second >= 60:
        minute += 1
        second -= 60
    if minute >= 60:
        hour += 1
        minute -= 60

    time_entry = str(hour).zfill(2) + ':'+ str(minute).zfill(2) + ':' + str(second).zfill(2)
    
    lights_selected = randint(0, len(list_of_lights)-3)
    light_1 = list_of_lights[lights_selected]
    light_2 = list_of_lights[lights_selected+1]
    light_3 = list_of_lights[lights_selected+2]

    for i in range(3):
        #print('{} - {} - Log: {} - Light_ID: {} - Light intensity: {} - Caused by motion: {} - Energy type: {}'.format(date_entry, time_entry, log_num, "L"+str(lights_selected+i), "100%", "Vehicle", "Brown"), end = '\n')
        toWriteTo_Data[day].append('{} - {} - Log: {} - Light_ID: {} - Light intensity: {} - Caused by motion: {} - Energy type: {}'.format(date_entry, time_entry, log_num, "L"+str(lights_selected+i), "100%", "Vehicle", "Brown"))
        log_num += 1

    second += 20
    if second >= 60:
        minute += 1
        second -= 60
    if minute >= 60:
        hour += 1
        minute -= 60

    time_entry = str(hour).zfill(2) + ':'+ str(minute).zfill(2) + ':' + str(second).zfill(2)

    for i in range(3):
        #print('{} - {} - Log: {} - Light_ID: {} - Light intensity: {} - Caused by motion: {} - Energy type: {}'.format(date_entry, time_entry, log_num, "L"+str(lights_selected+i), "70%", "null", "Brown"), end = '\n')
        toWriteTo_Data[day].append('{} - {} - Log: {} - Light_ID: {} - Light intensity: {} - Caused by motion: {} - Energy type: {}'.format(date_entry, time_entry, log_num, "L"+str(lights_selected+i), "50%", "null", "Brown"))
        log_num += 1


if __name__ == "__main__":
    log_number = 0
    date_array = ['12-02-2018', '13-02-2018', '14-02-2018', '15-02-2018', '16-02-2018']
    car_plates = car_plates_generator(50)
    #car_parking_status determines whether a car is parked in the carpark or not
    #car_parking_status = [False]*len(car_plates)
    #time_entries = sequential_time_in_weekday_generator(100)
    lightList = lights_generator(30)
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    weekends = ['Saturday', 'Sunday']

    toWriteTo = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    toWriteTo_Data = [[],[],[],[],[]]

    """
    Generate for weekdays 
    """
    for j in range(5):
        #print('\n' + weekdays[j] + '\n')
        time_entries = sequential_time_in_weekday_generator(1000000)
        car_parking_status = [False]*len(car_plates)
        for i in range(len(time_entries)):
            car_selector = randint(0, len(car_plates)-1)
            car_plate_selected = car_plates[car_selector]
            car_parking_status_selected = car_parking_status[car_selector]

            if car_parking_status_selected is True: #If it is currently in the carpark, then it will want to leave
                #Set log to exit the carpark
                #print('{} - {} - Log: {} - Carplate: "{}" - Event: "{}"'.format(date_array[j], time_entries[i], log_number, car_plate_selected, "Exit"), end='\n')
                toWriteTo_Data[j].append('{} - {} - Log: {} - Carplate: "{}" - Event: "{}"'.format(date_array[j], time_entries[i], log_number, car_plate_selected, "Exit"))
                car_parking_status[car_selector] = False
                log_number += 1
            else:
                #Entering the carpark
                #print('{} - {} - Log: {} - Carplate: "{}" - Event: "{}"'.format(date_array[j], time_entries[i], log_number, car_plate_selected, "Entry"), end='\n')
                toWriteTo_Data[j].append('{} - {} - Log: {} - Carplate: "{}" - Event: "{}"'.format(date_array[j], time_entries[i], log_number, car_plate_selected, "Entry"))
                car_parking_status[car_selector] = True
                log_number += 1
                lightUp_randomLights(lightList, log_number, date_array[j], time_entries[i], toWriteTo_Data, j)
                log_number += 6

        #Will need to force leave carpark at the end
        force_leave_carpark_weekday(car_plates, car_parking_status, date_array[j], log_number, toWriteTo_Data, j)

    for j in range(len(weekdays)):
        outfile_name = weekdays[j] + '.txt'
        output_file = open(outfile_name, 'w')
        for i in range(len(toWriteTo_Data[j])):
            output_file.write(toWriteTo_Data[j][i] + '\n')
        output_file.close()

    """
    Generate for weekends
    """
    toWriteTo_Data = [[],[]]
    for j in range(2):
        time_entries = sequential_time_in_weekend_generator(45)
        car_parking_status = [False]*len(car_plates)
        for i in range(len(time_entries)):
            car_selector = randint(0, len(car_plates)-1)
            car_plate_selected = car_plates[car_selector]
            car_parking_status_selected = car_parking_status[car_selector]
            if car_parking_status_selected is True: #If it is currently in the carpark, then it will want to leave
                #Set log to exit the carpark
                #print('{} - {} - Log: {} - Carplate: "{}" - Event: "{}"'.format(date_array[j], time_entries[i], log_number, car_plate_selected, "Exit"), end='\n')
                toWriteTo_Data[j].append('{} - {} - Log: {} - Carplate: "{}" - Event: "{}"'.format(date_array[j], time_entries[i], log_number, car_plate_selected, "Exit"))
                car_parking_status[car_selector] = False
                log_number += 1
            else:
                #Entering the carpark
                #print('{} - {} - Log: {} - Carplate: "{}" - Event: "{}"'.format(date_array[j], time_entries[i], log_number, car_plate_selected, "Entry"), end='\n')
                toWriteTo_Data[j].append('{} - {} - Log: {} - Carplate: "{}" - Event: "{}"'.format(date_array[j], time_entries[i], log_number, car_plate_selected, "Entry"))
                car_parking_status[car_selector] = True
                log_number += 1
                lightUp_randomLights(lightList, log_number, date_array[j], time_entries[i], toWriteTo_Data, j)
                log_number += 6

        #Will need to force leave carpark at the end
        force_leave_carpark_weekend(car_plates, car_parking_status, date_array[j], log_number, toWriteTo_Data, j)

    for j in range(len(weekends)):
        outfile_name = weekends[j] + '.txt'
        output_file = open(outfile_name, 'w')
        for i in range(len(toWriteTo_Data[j])):
            output_file.write(toWriteTo_Data[j][i] + '\n')
        output_file.close()
