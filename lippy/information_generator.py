"""
Reads a text file to generate meaningful data
"""

def main(filename):
    results = []
    infile = open(filename, 'r')
    for line in infile:
        elems = []
        line = line.rstrip('\n')
        line = line.split(' - ')
        for elem in line:
            if elem[-1] == '"':
                elem = elem.split(': ')
                elem[1] = elem[1][1:-1]
                elems += elem
            else:
                elem = elem.split(': ')
                elems += elem
        results.append(elems)
    return results

if __name__ == '__main__':
    parsed_data = main("Wednesday.txt")

    secs = 0
    for i in range(len(parsed_data)):
        if '100%' in parsed_data[i]:
            secs += 15
        #if

    json_collection = []
    for i in range(len(parsed_data)):
        if "Light_ID" in parsed_data[i]:
            json_data = """
{
    "Date"              : "%s",
    "Time"              : "%s",
    "Log"               : "%s",
    "Light_ID"          : "%s",
    "Light_intensity"   : "%s",
    "Caused_by_motion"  : "%s",
    "Energy_type"       : "%s"
}
"""
            date = parsed_data[i][0]
            time = parsed_data[i][1]
            log = parsed_data[i][3]
            light_id = parsed_data[i][5]
            light_intensity = parsed_data[i][7]
            caused_by_motion = parsed_data[i][9]
            energy_type = parsed_data[i][11]
            
            json_data = json_data % (date, time, log, light_id, light_intensity, caused_by_motion, energy_type)
        elif "Carplate" in parsed_data[i]:
            json_data = """
{
    "Date"      : "%s",
    "Time"      : "%s",
    "Log"       : "%s",
    "Carplate"  : "%s",
    "Event"     : "%s"
}
"""
            date = parsed_data[i][0]
            time = parsed_data[i][1]
            log = parsed_data[i][3]
            carplate = parsed_data[i][5]
            event = parsed_data[i][7]
            
            json_data = json_data %(date, time, log, carplate, event)
            
        json_collection.append(json_data)
        #print(json_data)
        
            
    
