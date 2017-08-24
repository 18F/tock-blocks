import tock_blocks
import csv


def all_users_from_file(userfile, args, months):
    users = tock_blocks.read_CSV_to_list(userfile)
    time_entries = tock_blocks.read_CSV_to_list(args.file)
    user_list = [0] * len(users)
    arr_ind = 0
    for user in users:
        user_list[arr_ind] = users[arr_ind] + util_csv(user[0], months, time_entries)
        arr_ind +=1
    with open(args.outfile, 'a') as outcsv:
        #configure writer to write standard csv file
        writer = csv.writer(outcsv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        writer.writerow(['Name', 'Position', 'Team', 'Project type']+list(range(months[0],months[1])))
        for item in user_list:
            #Write item to outcsv
            billable_list= [i[0] for i in item[3:]]
            internal_list= [i[1] for i in item[3:]]
            util_list= [i[2] for i in item[3:]]
            toprow = [item[0], item[1], item[2], 'Billable']+billable_list
            middlelist= ['', '', '', 'Internal projects'] + internal_list
            bottom= ['', '', '', 'Utilization percentage'] + util_list
            writer.writerow(toprow)
            writer.writerow(middlelist)
            writer.writerow(bottom)
            writer.writerow(['']*(len(item)+1))

def util_csv(user, months, time_entries):
    # Grab user
    user_entries = tock_blocks.get_user_entries(user, time_entries)
    # Calculate each month billable/ utilization / total for that user
    user_values = [0] * (months[1]-months[0])
    array_ind = 0
    for x in range(months[0], months[1]):
        mStart = ""
        mEnd = ""
        if x < 9:
            mStart = "0"+str(x)
            mEnd = "0"+str(x+1)
        elif(x == 9):
            mStart = "0"+str(x)
            mEnd = "10"
        else:
            mStart = str(x)
            mEnd = str(x+1)
        month_time_entries = tock_blocks.get_entries_in_time_period("2017-"+mStart+"-01", "2017-"+mEnd+"-01", user_entries)
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
