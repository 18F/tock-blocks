import argparse
import tock_blocks

def main():
    parser = argparse.ArgumentParser(description='Calculate a users major time blocks')
    parser.add_argument('-p','--program',
                        help='choose between tock blocks and the full user program.',
                        default='tock-blocks',
                        dest='users')
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
    time_entries = tock_blocks.read_CSV_to_list(args.file)
    if(args.verbose):
        print("Printing Length and CSV Headers")
        print(len(time_entries))
        print(time_entries[0])
        print(time_entries[1])
    if(args.display_format == 'pretty'):
        print("Tock data from "+args.start_date + " to "+args.end_date)
    if(args.display_format == 'markdown'):
        print("# Tock data from "+args.start_date + " to "+args.end_date)
    tock_blocks.block_by_array(args.users, time_entries, args.start_date, args.end_date, args.display_format, args.exclude_leave)

if __name__ == "__main__":
    main()
