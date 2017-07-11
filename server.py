import csv
import datetime
from dateutil.parser import parse as date_parse
import argparse

# Import CSV File
def read_CSV_to_list(csv_file):
    with open(csv_file, 'r') as f:
      reader = csv.reader(f)
      csv_list = list(reader)

    return csv_list

# TODO convert to api pull

# Function for one person
def block_for_one_person(start, end, username, time_entries, exclude_leave):
    user_entries = get_user_entries(username, time_entries)
    time_period_entries = get_entries_in_time_period(start, end, user_entries)
    if(exclude_leave):
        time_period_entries = remove_leave(time_period_entries)
    project_dict = create_project_dict(time_period_entries)
    total_hours = reduce_dict_to_hours(project_dict)
    perc_dict = calculate_projects_percentage(project_dict, total_hours)
    blocks = blockify_projects(perc_dict)
    return blocks

leave_types = ['Out of Office - Sick Leave',
 'Out of Office - Administrative/Holiday Leave',
 'Out of Office - Annual Leave', 'Out of Office - Award Time',
 'Out of Office - Compensatory Time',
 'Out of Office - Court Leave (Jury Duty)',
 'Out of Office - Donated Leave',
 'Out of Office - Leave Without Pay',
 'Out of Office - Other'
 ]

def remove_leave(entries):
    filtered_entries = []
    for entry in entries:
        if (entry[0] not in leave_types):
            filtered_entries.append(entry)
    return filtered_entries

# Filter By User
def get_user_entries(username, entries):
    user_entries = []
    for entry in entries:
        if entry[2] == username:
            user_entries.append(entry)
    return user_entries

# Filter By time
#TODO Filter by time
def get_entries_in_time_period(start, end, entries):
    time_periods_entries = []
    start_date = date_parse(start)
    end_date = date_parse(end)
    for entry in entries:
        entry_start = date_parse(entry[3])
        entry_end = date_parse(entry[4])
        start_diff = (entry_start-start_date).days
        end_diff = (entry_end-end_date).days
        if(start_diff >= 0 and end_diff <= 0):
            time_periods_entries.append(entry)
    return time_periods_entries

#Get projects from entries and map hours spent
def create_project_dict(entries):
    project_dict = {}
    for entry in entries:
        if entry[0] in project_dict:
            project_dict[entry[0]] = project_dict[entry[0]] + float(entry[5])
        else:
            project_dict[entry[0]] = float(entry[5])
    return project_dict

# Calculate project percentages
def calculate_projects_percentage(projects, total_hours):
    percentage_projects = {}
    if total_hours > 0:
        for p in projects:
            percentage_projects[p] = myround(projects[p]/total_hours*100)
        return percentage_projects
    else:
        return projects

def myround(x, base=5):
    return int(base * round(float(x)/base))

# Reduce Project dict to total hours
def reduce_dict_to_hours(proj_dict):
    total_hours = 0
    for proj in proj_dict:
        total_hours = total_hours + proj_dict[proj]
    return total_hours

# Convert projects into 20% blocks
def blockify_projects(perc_dict):
    blocks = []
    other = {"Other": []}
    for project in perc_dict:
        proj_block = {}
        proj_block[project] = perc_dict[project]
        if perc_dict[project] >= 20.0:
            blocks.append(proj_block)
        elif perc_dict[project] > 0:
            other['Other'].append(proj_block)
    blocks.append(other)
    return blocks

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

# Function for an array of person
def block_by_array(users, entries, start, end, nice_display, exclude_leave):
    for u in users:
        print_handler(u, nice_display, 'header')
        if (nice_display):
            user_block = block_for_one_person(start, end, u, entries, exclude_leave)
            print_nice(user_block, nice_display)
        else:
            print (block_for_one_person(start, end, u, entries, exclude_leave))

def print_nice(user_block_list, nice_display):
    for activity in user_block_list:
        for i in activity:
            if (i == 'Other'):
                print_handler('Other', nice_display, 'bold')
                for oth in activity[i]:
                    print(oth)
            else:
                print(i, activity[i])
    print("\n")

def print_handler(text, nice_display, level):
    if(nice_display == 'pretty'):
        if(level == 'bold'):
            return print(color.BOLD+'Other'+color.END)
        return print(color.PURPLE+text+color.END)
    if(nice_display == 'markdown'):
        if (level == 'bold'):
            return print('*'+text+'*')
        return print('## '+text)
    return print(text)

def main():
    parser = argparse.ArgumentParser(description='Calculate a users major time blocks')
    parser.add_argument('-u','--users', nargs='+',
                        help='user or users list',
                        required=True,
                        default='darren.divens',
                        dest='users')
    parser.add_argument('-f', action='store', default='timecards_bulk.csv',
                        dest='file',
                        help='The csv file for the tock entries')
    parser.add_argument('-s', action='store', default='2016-01-01',
                        dest='start_date',
                        help='YYYY-MM-DD The start date of the tock entries you would like to search through.')
    parser.add_argument('-e', action='store', default='2016-06-01',
                        dest='end_date',
                        help='YYYY-MM-DD The end date of the tock entries you would like to search through.')
    parser.add_argument('-v', action='store_true', default=False,
                        dest='verbose',
                        help='print out csv headers')
    parser.add_argument('-d', '--display_format',
                        dest='display_format',
                        help='print display in pretty colors on standard out, or in markdown')
    parser.add_argument('-l','--exclude-leave', action='store_true',
                        default=False,
                        dest='exclude_leave',
                        help='exclude annual leave and holidays from the report')


    args = parser.parse_args()
    time_entries = read_CSV_to_list(args.file)
    if(args.verbose):
        print("Printing Length and CSV Headers")
        print(len(time_entries))
        print(time_entries[0])
        print(time_entries[1])
    if(args.display_format == 'pretty'):
        print("Tock data from "+args.start_date + " to "+args.end_date)
    if(args.display_format == 'markdown'):
        print("# Tock data from "+args.start_date + " to "+args.end_date)
    block_by_array(args.users, time_entries, args.start_date, args.end_date, args.display_format, args.exclude_leave)

if __name__ == "__main__":
    main()
