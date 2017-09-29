import tock_blocks
import csv
from dateutil.parser import parse as date_parse

month_name_list = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def all_users_from_file(userfile, args):
    print(color.PURPLE+"TOCK BLOCKS:"+color.END+" Generating the utilization report from the data in "+args.file+".")
    users = tock_blocks.read_CSV_to_list(userfile)
    time_entries = tock_blocks.read_CSV_to_list(args.file)
    user_list = [0] * len(users)
    arr_ind = 0
    months = find_months(args.beginmonth, args.lastmonth)
    for user in users:
        user_list[arr_ind] = users[arr_ind] + util_csv(user[0], months, time_entries)
        arr_ind +=1
    with open(args.outfile, 'w') as outcsv:
        #configure writer to write standard csv file
        writer = csv.writer(outcsv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        header_row = ['Name', 'Position', 'Team', 'Project type']+month_name_list[(months[0]-1): months[1]-1]+['Average']
        writer.writerow(header_row )
        for item in user_list:
            toprow = [item[0], item[1], item[2], 'Billable']+monthly_and_average(item, 0)
            middlelist= ['', '', '', 'Internal projects'] + monthly_and_average(item, 1)
            bottom= ['', '', '', 'Utilization percentage'] + monthly_and_average(item, 2)
            writer.writerow(toprow)
            writer.writerow(middlelist)
            writer.writerow(bottom)
            writer.writerow(['']*(len(item)+1))
    print(color.PURPLE+"TOCK BLOCKS:"+color.END+" Completed generating the utilization summary. Please view the report in the file "+ args.outfile +".")

def util_csv(user, months, time_entries):
    # Grab user
    user_entries = tock_blocks.get_user_entries(user, time_entries)
    # Calculate each month billable/ utilization / total for that user
    user_values = [0] * (months[1]-months[0])
    array_ind = 0
    for x in range(months[0], months[1]):
        mStart = ""
        mEnd = ""
        lastDay = "01"
        if x < 9:
            mStart = "0"+str(x)
            mEnd = "0"+str(x+1)
        elif(x == 9):
            mStart = "0"+str(x)
            mEnd = "10"
        elif(x == 12):
            mStart = "12"
            mEnd = "12"
            lastDay = "31"
        else:
            mStart = str(x)
            mEnd = str(x+1)
        month_time_entries = tock_blocks.get_entries_in_time_period("2017-"+mStart+"-01", "2017-"+mEnd+"-"+lastDay, user_entries, 'util')
        billable_hours = calc_billable_hours(month_time_entries)
        internal_hours = calc_internal_hours(month_time_entries)
        total_hours = calc_total_hours(month_time_entries)
        billable_perc = 0.0
        internal_perc = 0.0
        if (total_hours > 0):
            billable_perc = round(billable_hours/total_hours*100, 1)
            internal_perc = round(internal_hours/total_hours*100, 1)
        utilizable_perc = round((billable_perc + internal_perc), 1)
        user_values[array_ind]=[billable_perc,internal_perc, utilizable_perc]
        array_ind += 1
    return user_values


#TODO convert to lamdas
def calc_hour_generator(calc_method):
    def nestedEntryIterator(entries):
        hour_count = 0
        for entry in entries:
            if(calc_method):
                hour_count += float(entry[5])
    return nestedEntryIterator

# calc_billable_hours = calc_billable_hours()

def calc_billable_hours(entries):
    billable_hours_count = 0.0
    for entry in entries:
        if(entry[6] == "True"):
            billable_hours_count = billable_hours_count + float(entry[5])
    return billable_hours_count

def calc_internal_hours(entries):
    internal_hours = 0.0
    for entry in entries:

        if(entry[0][:22] == "TTS Acq / Internal Acq" and entry[6]== "False"):
            internal_hours = internal_hours + float(entry[5])
    return internal_hours

def calc_total_hours(entries):
    total_hours = 0.0
    for entry in entries:
        total_hours = total_hours + float(entry[5])
    return total_hours

def monthly_and_average(user_list_row, sub_array_ind):
    filtered_list = [i[sub_array_ind] for i in user_list_row[3:]]
    filtered_list.append(round(mean(filtered_list), 1))
    return filtered_list

def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

def find_months(startingmonth, endingmonth):
    return [month_name_list.index(startingmonth)+1, month_name_list.index(endingmonth)+2]
