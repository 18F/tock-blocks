"""Run the Tock Blocks Program"""
import csv
import json
from dateutil.parser import parse as date_parse


def read_json_to_list(time_entry_json_file):
    return json.load(open(time_entry_json_file))

# Import CSV File
def read_csv_to_list(csv_file):
    with open(csv_file, 'r') as file_in_memory:
        reader = csv.reader(file_in_memory)
        csv_list = list(reader)
    return csv_list

# Function for an array of people
def block_by_array(args):
    if args.file is not None:
        time_entries = read_json_to_list(args.file)
    for user in args.users:
        print_handler(user, args.display_format, 'header')
        if args.display_format:
            user_block = block_for_one_person(
                args.start_date, args.end_date, user, time_entries, args.exclude_leave)
            print_nice(user_block, args.display_format)
        else:
            print(block_for_one_person(args.start_date, args.end_date, user, time_entries, args.exclude_leave))

# Function for one person
def block_for_one_person(start, end, username, time_entries, exclude_leave):
    user_entries = get_user_entries(username, time_entries)
    time_period_entries = get_entries_in_month(start, user_entries)
    if exclude_leave:
        time_period_entries = remove_leave(time_period_entries)
    project_dict = create_project_dict(time_period_entries)
    total_hours = reduce_dict_to_hours(project_dict)
    perc_dict = calculate_projects_percentage(project_dict, total_hours)
    blocks = blockify_projects(perc_dict)
    return blocks

# Filter By User
def get_user_entries(username, entries):
    user_entries = []
    for entry in entries:
        if entry['user'] == username:
            user_entries.append(entry)
    return user_entries

# Filter By time
def get_entries_in_month(month_to_check, entries):
    time_periods_entries = []
    month_as_date = date_parse(month_to_check)
    for entry in entries:
        entry_start = date_parse(entry['start_date'])
        if month_as_date.month == entry_start.month and month_as_date.year == entry_start.year:
            time_periods_entries.append(entry)
    return time_periods_entries

LEAVE_TYPES = ['Out of Office - Sick Leave',
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
        if entry['project_name'] not in LEAVE_TYPES:
            filtered_entries.append(entry)
    return filtered_entries

#Get projects from entries and map hours spent
def create_project_dict(entries):
    project_dict = {}
    for entry in entries:
        if entry['project_name'] in project_dict:
            project_dict[entry['project_name']] = project_dict[entry['project_name']] + float(entry['hours_spent'])
        else:
            project_dict[entry['project_name']] = float(entry['hours_spent'])
    return project_dict

# Calculate project percentages
def calculate_projects_percentage(projects, total_hours):
    percentage_projects = {}
    if total_hours > 0:
        for project in projects:
            percentage_projects[project] = my_round(projects[project]/total_hours*100)
        return percentage_projects
    return projects

def my_round(num, base=5):
    return int(base * round(float(num)/base))

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

class Color:
    """
    List of command line colors
    """
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

def print_nice(user_block_list, nice_display):
    for activity in user_block_list:
        for i in activity:
            if i == 'Other':
                print_handler('Other', nice_display, 'bold')
                for oth in activity[i]:
                    print(oth)
                    if nice_display == 'markdown':
                        print("\n")
            else:
                print(i, activity[i])
                if nice_display == 'markdown':
                    print("\n")
    print("\n")

def print_handler(text, nice_display, level):
    if nice_display == 'pretty':
        if level == 'bold':
            return print(Color.BOLD+'Other'+Color.END)
        return print(Color.PURPLE+text+Color.END)
    if nice_display == 'markdown':
        if level == 'bold':
            return print('*'+text+'*')
        return print('## '+text)
    return print(text)
